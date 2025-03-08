// Student Management System JavaScript
class StudentManager {
    constructor() {
        this.students = [];
        this.currentPage = 1;
        this.itemsPerPage = 10;
        this.initializeTooltips();
        this.bindSearchEvent();
        this.bindFilterEvents();
        this.bindPaginationEvents();
        this.bindStudentActionEvents();
        this.loadStudents();
    }

    initializeTooltips() {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    bindSearchEvent() {
        const searchInput = document.querySelector('.search-container input');
        if (searchInput) {
            searchInput.addEventListener('keyup', (e) => {
                this.filterStudents(e.target.value);
            });
        }
    }

    bindFilterEvents() {
        // Filter dropdown items
        document.querySelectorAll('.dropdown-item').forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                const filterType = e.target.textContent;
                this.applyFilter(filterType);
            });
        });

        // Evaluation level filter
        const evalSelect = document.querySelector('select.form-select');
        if (evalSelect) {
            evalSelect.addEventListener('change', (e) => {
                this.filterByEvaluation(e.target.value);
            });
        }
    }

    bindPaginationEvents() {
        document.querySelectorAll('.pagination .page-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const pageText = e.target.textContent;

                if (pageText === '«') {
                    this.changePage(this.currentPage - 1);
                } else if (pageText === '»') {
                    this.changePage(this.currentPage + 1);
                } else {
                    this.changePage(parseInt(pageText));
                }
            });
        });
    }

    bindStudentActionEvents() {
        // View details buttons
        document.querySelectorAll('.btn-view-details').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const studentId = this.getStudentIdFromButton(e.target);
                this.viewStudentDetails(studentId);
            });
        });

        // Edit buttons
        document.querySelectorAll('.btn-edit-student').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const studentId = this.getStudentIdFromButton(e.target);
                window.location.href = `edit-student.html?id=${studentId}`;
            });
        });

        // Delete buttons
        document.querySelectorAll('.btn-delete-student').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const studentId = this.getStudentIdFromButton(e.target);
                this.confirmDeleteStudent(studentId);
            });
        });

        // Add student button
        const addStudentBtn = document.getElementById('addStudentBtn');
        if (addStudentBtn) {
            addStudentBtn.addEventListener('click', () => {
                window.location.href = 'add-Student.html';
            });
        }
    }

    getStudentIdFromButton(element) {
        // Navigate up to the row and get the student ID from the first cell
        const button = element.closest('button') || element;
        const row = button.closest('tr');
        return row.querySelector('td:first-child').textContent;
    }

    loadStudents() {
        // Show loading spinner
        const spinner = document.querySelector('.loading-spinner');
        if (spinner) spinner.style.display = 'block';

        // In a real application, this would be an API call
        // For now, we'll use the existing table data
        const tableRows = document.querySelectorAll('tbody tr');

        this.students = Array.from(tableRows).map(row => {
            const cells = row.querySelectorAll('td');
            return {
                id: cells[0].textContent,
                name: cells[1].textContent,
                age: cells[2].textContent,
                memorizedParts: cells[3].querySelector('.progress-info').textContent.split('(')[0].trim(),
                percentage: cells[3].querySelector('.progress-info').textContent.split('(')[1].replace(')', ''),
                lastUpdate: cells[4].textContent,
                evaluation: cells[5].querySelector('.badge').textContent
            };
        });

        // Hide loading spinner
        if (spinner) spinner.style.display = 'none';

        // Update stats
        this.updateStats();
    }

    updateStats() {
        const totalStudents = this.students.length;
        const totalStudentsElement = document.querySelector('.stats-card:nth-child(1) h2');
        if (totalStudentsElement) totalStudentsElement.textContent = totalStudents;

        // Calculate average memorization
        const totalParts = this.students.reduce((sum, student) => {
            const parts = parseFloat(student.memorizedParts);
            return sum + (isNaN(parts) ? 0 : parts);
        }, 0);

        const averageParts = totalStudents > 0 ? totalParts / totalStudents : 0;
        const averagePartsElement = document.querySelector('.stats-card:nth-child(2) h2');
        if (averagePartsElement) averagePartsElement.textContent = `${averageParts.toFixed(1)} أجزاء`;

        // Count excellent evaluations
        const excellentCount = this.students.filter(student => student.evaluation === 'ممتاز').length;
        const excellentCountElement = document.querySelector('.stats-card:nth-child(3) h2');
        if (excellentCountElement) excellentCountElement.textContent = `${excellentCount} طالب`;
    }

    filterStudents(searchTerm) {
        searchTerm = searchTerm.toLowerCase();
        const tableRows = document.querySelectorAll('tbody tr');

        tableRows.forEach(row => {
            const studentName = row.querySelector('td:nth-child(2)').textContent.toLowerCase();
            if (studentName.includes(searchTerm)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }

    applyFilter(filterType) {
        const tableRows = Array.from(document.querySelectorAll('tbody tr'));
        const tbody = document.querySelector('tbody');

        if (!tbody) return;

        // Clear the table
        tbody.innerHTML = '';

        // Sort based on filter type
        if (filterType === 'أعلى تقييم') {
            tableRows.sort((a, b) => {
                const evalA = a.querySelector('td:nth-child(6) .badge').textContent;
                const evalB = b.querySelector('td:nth-child(6) .badge').textContent;
                return evalA === 'ممتاز' ? -1 : 1;
            });
        } else if (filterType === 'الأكثر حفظًا') {
            tableRows.sort((a, b) => {
                const partsA = parseFloat(a.querySelector('td:nth-child(4) .progress-info').textContent);
                const partsB = parseFloat(b.querySelector('td:nth-child(4) .progress-info').textContent);
                return partsB - partsA;
            });
        } else if (filterType === 'الأحدث') {
            tableRows.sort((a, b) => {
                const dateA = new Date(a.querySelector('td:nth-child(5)').textContent);
                const dateB = new Date(b.querySelector('td:nth-child(5)').textContent);
                return dateB - dateA;
            });
        } else if (filterType === 'إعادة ضبط') {
            tableRows.sort((a, b) => {
                const idA = parseInt(a.querySelector('td:first-child').textContent);
                const idB = parseInt(b.querySelector('td:first-child').textContent);
                return idA - idB;
            });
        }

        // Re-add the sorted rows
        tableRows.forEach(row => tbody.appendChild(row));
    }

    filterByEvaluation(evaluation) {
        if (evaluation === 'مستوى التقييم') {
            // Show all rows
            document.querySelectorAll('tbody tr').forEach(row => {
                row.style.display = '';
            });
            return;
        }

        document.querySelectorAll('tbody tr').forEach(row => {
            const studentEval = row.querySelector('td:nth-child(6) .badge').textContent;
            if (studentEval === evaluation) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }

    changePage(pageNumber) {
        const totalPages = Math.ceil(this.students.length / this.itemsPerPage);

        // Validate page number
        if (pageNumber < 1 || pageNumber > totalPages) {
            return;
        }

        // Update current page
        this.currentPage = pageNumber;

        // Update active page in pagination
        document.querySelectorAll('.pagination .page-item').forEach(item => {
            item.classList.remove('active');
        });

        const pageItems = document.querySelectorAll('.pagination .page-item');
        // Skip first and last items (prev/next buttons)
        pageItems[pageNumber].classList.add('active');

        // In a real app, this would load the appropriate page of students
        // For now, we'll just log the page change
        console.log(`Changed to page ${pageNumber}`);
    }

    viewStudentDetails(studentId) {
        // Find the student in our array
        const student = this.students.find(s => s.id === studentId);

        if (!student) return;

        // Create and show modal
        const modalHtml = `
      <div class="modal fade" id="studentDetailsModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-lg">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">تفاصيل الطالب: ${student.name}</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <div class="student-details-card">
                <div class="student-details-header">
                  <h4>${student.name}</h4>
                  <p class="mb-0">العمر: ${student.age} | التقييم: <span class="badge bg-success">${student.evaluation}</span></p>
                </div>
                <div class="student-details-body">
                  <div class="row">
                    <div class="col-md-6">
                      <p><strong>الأجزاء المحفوظة:</strong> ${student.memorizedParts}</p>
                      <p><strong>آخر متابعة:</strong> ${student.lastUpdate}</p>
                    </div>
                    <div class="col-md-6">
                      <p><strong>نسبة الإنجاز:</strong> ${student.percentage}</p>
                      <div class="progress" style="height: 10px;">
                        <div class="progress-bar" style="width: ${student.percentage}"></div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">إغلاق</button>
              <a href="student-plan.html?id=${student.id}" class="btn btn-primary">عرض خطة الحفظ</a>
            </div>
          </div>
        </div>
      </div>
    `;

        // Add modal to body
        document.body.insertAdjacentHTML('beforeend', modalHtml);

        // Show modal
        const modal = new bootstrap.Modal(document.getElementById('studentDetailsModal'));
        modal.show();

        // Remove modal from DOM when hidden
        document.getElementById('studentDetailsModal').addEventListener('hidden.bs.modal', function () {
            this.remove();
        });
    }

    confirmDeleteStudent(studentId) {
        if (confirm(`هل أنت متأكد من حذف الطالب رقم ${studentId}؟`)) {
            // In a real app, this would be an API call
            console.log(`Deleting student ${studentId}`);

            // Remove from DOM
            const row = document.querySelector(`tbody tr td:first-child:contains('${studentId}')`).closest('tr');
            if (row) row.remove();

            // Remove from array
            this.students = this.students.filter(s => s.id !== studentId);

            // Update stats
            this.updateStats();
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new StudentManager();
});