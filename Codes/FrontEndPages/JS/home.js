class StudentManager {
    constructor() {
        this.students = students;
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
        // Use event delegation for dynamically created buttons
        document.querySelector('tbody').addEventListener('click', (e) => {
            const button = e.target.closest('.btn-view-details');
            if (button) {
                const studentId = this.getStudentIdFromButton(button);
                window.location.href = `student-plan2.html?id=${studentId}`;
            }
        });

        document.querySelector('tbody').addEventListener('click', (e) => {
            const button = e.target.closest('.btn-edit-student');
            if (button) {
                const studentId = this.getStudentIdFromButton(button);
                window.location.href = `edit-Student.html`;
            }
        });

        // Update delete button event listener to use event delegation
        document.querySelector('tbody').addEventListener('click', (e) => {
            const button = e.target.closest('.btn-delete-student');
            if (button) {
                const studentId = parseInt(this.getStudentIdFromButton(button));
                this.confirmDeleteStudent(studentId);
            }
        });

        const addStudentBtn = document.getElementById('addStudentBtn');
        if (addStudentBtn) {
            addStudentBtn.addEventListener('click', () => {
                window.location.href = '../HTML/add-Student.html';
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
        const spinner = document.querySelector('.loading-spinner');
        const tbody = document.querySelector('tbody');
        if (spinner) spinner.style.display = 'block';

        tbody.innerHTML = '';

        this.students.forEach(student => {
            const row = document.createElement('tr');
            const memorizedParts = typeof student.memorizedParts === 'number' ? 
                `${student.memorizedParts} أجزاء` : student.memorizedParts;
            
            row.innerHTML = `
                <td>${student.id}</td>
                <td>${student.name}</td>
                <td>${student.age}</td>
                <td>
                    <div class="progress" style="height: 5px;">
                        <div class="progress-bar" style="width: ${student.percentage}"></div>
                    </div>
                    <small class="progress-info">${memorizedParts} (${student.percentage})</small>
                </td>
                <td>${student.lastUpdate}</td>
                <td><span class="badge ${this.getEvaluationBadgeClass(student.evaluation)}">${student.evaluation}</span></td>
                <td>
                    <button class="btn btn-sm btn-outline-primary btn-view-details" data-bs-toggle="tooltip" title="عرض الخطة">
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
            case 'جيد جدا': return 'bg-primary';
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
            const parts = typeof student.memorizedParts === 'number' ? 
                student.memorizedParts : 
                parseInt(student.memorizedParts);
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
        const student = this.students.find(s => s.id === parseInt(studentId));
        if (!student) return;
        window.location.href = `student-plan2.html?id=${student.id}`;
    }

    confirmDeleteStudent(studentId) {
        const student = this.students.find(s => s.id === studentId);
        if (!student) return;

        // Create modal if it doesn't exist
        let deleteModal = document.getElementById('deleteStudentModal');
        if (!deleteModal) {
            const modalHtml = `
                <div class="modal fade" id="deleteStudentModal" tabindex="-1" aria-labelledby="deleteStudentModalLabel" aria-hidden="true">
                    <div class="modal-dialog modal-dialog-centered">
                        <div class="modal-content">
                        <!-- 
                            <div class="modal-header bg-danger text-white">
                                <h5 class="modal-title" id="deleteStudentModalLabel">
                                    <i class="fas fa-exclamation-triangle me-2"></i>تأكيد الحذف
                                </h5>
                                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            -->
                            <div class="modal-body text-center">
                                <i class="fas fa-user-times fa-4x text-danger mb-3"></i>
                                <p class="fs-5">هل أنت متأكد من حذف الطالب</p>
                                <p class="fs-4 fw-bold text-danger student-name"></p>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">إلغاء</button>
                                <button type="button" class="btn btn-danger confirm-delete">
                                    <i class="fas fa-trash me-2"></i>حذف
                                </button>
                            </div>
                        </div>
                    </div>
                </div>`;
            document.body.insertAdjacentHTML('beforeend', modalHtml);
            deleteModal = document.getElementById('deleteStudentModal');
        }

        // Set student name in modal
        deleteModal.querySelector('.student-name').textContent = `"${student.name}"`;

        // Initialize modal
        const modal = new bootstrap.Modal(deleteModal);
        modal.show();

        // Handle delete confirmation
        const confirmBtn = deleteModal.querySelector('.confirm-delete');
        const handleDelete = () => {
            // Remove event listener
            confirmBtn.removeEventListener('click', handleDelete);

            // Hide modal
            modal.hide();

            // Find and remove the row with animation
            const row = document.querySelector(`tbody tr td:first-child[textContent="${studentId}"]`).parentElement;
            row.style.transition = 'all 0.3s ease-out';
            row.style.backgroundColor = '#ffebee';
            row.style.opacity = '0';

            setTimeout(() => {
                // Remove from data and UI
                this.students = this.students.filter(s => s.id !== studentId);
                row.remove();
                this.updateStats();

                // Show success toast
                const toast = new bootstrap.Toast(document.createElement('div'));
                toast._element.className = 'toast align-items-center text-white bg-success border-0 position-fixed bottom-0 end-0 m-3';
                toast._element.style.zIndex = '1050';
                toast._element.innerHTML = `
                    <div class="d-flex">
                        <div class="toast-body">
                            <i class="fas fa-check-circle me-2"></i>
                            تم حذف الطالب "${student.name}" بنجاح
                        </div>
                        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
                    </div>`;
                document.body.appendChild(toast._element);
                toast.show();

                // Remove toast element after it's hidden
                toast._element.addEventListener('hidden.bs.toast', () => {
                    toast._element.remove();
                });
            }, 300);
        };

        confirmBtn.addEventListener('click', handleDelete);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new StudentManager();
});