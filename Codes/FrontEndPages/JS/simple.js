class StudentManager {
    constructor() {
        this.students = this.generateSampleStudents(20);
        this.currentPage = 1;
        this.itemsPerPage = 10;
        this.initializeTooltips();
        this.bindSearchEvent();
        this.bindFilterEvents();
        this.bindPaginationEvents();
        this.bindStudentActionEvents();
        this.loadStudents();
    }

    generateSampleStudents(count) {
        const students = [];
        const evaluations = ['ممتاز', 'جيد جدًا', 'جيد', 'مقبول', 'ضعيف'];
        const lastUpdates = ['2023-06-15', '2023-06-14', '2023-06-13', '2023-06-12', '2023-06-11'];

        for (let i = 1; i <= count; i++) {
            const parts = Math.floor(Math.random() * 30) + 1;
            const percentage = ((parts / 30) * 100).toFixed(0);

            students.push({
                id: i,
                name: `طالب ${i}`,
                age: Math.floor(Math.random() * 5) + 12,
                memorizedParts: `${parts} أجزاء`,
                percentage: `${percentage}%`,
                lastUpdate: lastUpdates[Math.floor(Math.random() * lastUpdates.length)],
                evaluation: evaluations[Math.floor(Math.random() * evaluations.length)]
            });
        }
        return students;
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
        document.querySelectorAll('.btn-view-details').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const studentId = this.getStudentIdFromButton(e.target);
                this.viewStudentDetails(studentId);
            });
        });

        document.querySelectorAll('.btn-edit-student').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const studentId = this.getStudentIdFromButton(e.target);
                window.location.href = `edit-student.html?id=${studentId}`;
            });
        });

        document.querySelectorAll('.btn-delete-student').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const studentId = this.getStudentIdFromButton(e.target);
                this.confirmDeleteStudent(studentId);
            });
        });

        const addStudentBtn = document.getElementById('addStudentBtn');
        if (addStudentBtn) {
            addStudentBtn.addEventListener('click', () => {
                window.location.href = 'add-Student.html';
            });
        }
    }

    getStudentIdFromButton(element) {
        const button = element.closest('button') || element;
        const row = button.closest('tr');
        return row.querySelector('td:first-child').textContent;
    }

    loadStudents() {
        const spinner = document.querySelector('.loading-spinner');
        const tbody = document.querySelector('tbody');
        if (spinner) spinner.style.display = 'block';

        tbody.innerHTML = '';

        this.students.forEach(student => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${student.id}</td>
                <td>${student.name}</td>
                <td>${student.age}</td>
                <td>
                    <div class="progress" style="height: 5px;">
                        <div class="progress-bar" style="width: ${student.percentage}"></div>
                    </div>
                    <small class="progress-info">${student.memorizedParts} (${student.percentage})</small>
                </td>
                <td>${student.lastUpdate}</td>
                <td><span class="badge ${this.getEvaluationBadgeClass(student.evaluation)}">${student.evaluation}</span></td>
                <td>
                    <button class="btn btn-sm btn-outline-primary btn-view-details" data-bs-toggle="tooltip" title="عرض التفاصيل">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-warning btn-edit-student" data-bs-toggle="tooltip" title="تعديل">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger btn-delete-student" data-bs-toggle="tooltip" title="حذف">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            `;
            tbody.appendChild(row);
        });

        if (spinner) spinner.style.display = 'none';
        this.updateStats();
        this.initializeTooltips();
    }

    getEvaluationBadgeClass(evaluation) {
        switch (evaluation) {
            case 'ممتاز': return 'bg-success';
            case 'جيد جدًا': return 'bg-primary';
            case 'جيد': return 'bg-warning text-dark';
            case 'مقبول': return 'bg-info';
            case 'ضعيف': return 'bg-danger';
            default: return 'bg-secondary';
        }
    }

    updateStats() {
        const totalStudents = this.students.length;
        const totalStudentsElement = document.querySelector('.stats-card:nth-child(1) h2');
        if (totalStudentsElement) totalStudentsElement.textContent = totalStudents;

        const totalParts = this.students.reduce((sum, student) => {
            const parts = parseFloat(student.memorizedParts);
            return sum + (isNaN(parts) ? 0 : parts);
        }, 0);

        const averageParts = totalStudents > 0 ? totalParts / totalStudents : 0;
        const averagePartsElement = document.querySelector('.stats-card:nth-child(2) h2');
        if (averagePartsElement) averagePartsElement.textContent = `${averageParts.toFixed(1)} أجزاء`;

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

        tbody.innerHTML = '';

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

        tableRows.forEach(row => tbody.appendChild(row));
    }

    filterByEvaluation(evaluation) {
        if (evaluation === 'مستوى التقييم') {
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

        if (pageNumber < 1 || pageNumber > totalPages) {
            return;
        }

        this.currentPage = pageNumber;

        document.querySelectorAll('.pagination .page-item').forEach(item => {
            item.classList.remove('active');
        });

        const pageItems = document.querySelectorAll('.pagination .page-item');
        pageItems[pageNumber].classList.add('active');

        console.log(`Changed to page ${pageNumber}`);
    }

    viewStudentDetails(studentId) {
        const student = this.students.find(s => s.id == studentId);

        if (!student) return;

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

        document.body.insertAdjacentHTML('beforeend', modalHtml);

        const modal = new bootstrap.Modal(document.getElementById('studentDetailsModal'));
        modal.show();

        document.getElementById('studentDetailsModal').addEventListener('hidden.bs.modal', function () {
            this.remove();
        });
    }

    confirmDeleteStudent(studentId) {
        if (confirm(`هل أنت متأكد من حذف الطالب رقم ${studentId}؟`)) {
            console.log(`Deleting student ${studentId}`);

            const row = document.querySelector(`tbody tr td:first-child:contains('${studentId}')`).closest('tr');
            if (row) row.remove();

            this.students = this.students.filter(s => s.id != studentId);

            this.updateStats();
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new StudentManager();
});