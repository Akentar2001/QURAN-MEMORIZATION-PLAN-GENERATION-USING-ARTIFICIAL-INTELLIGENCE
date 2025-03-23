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
        
        this.fetchStudents();
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
                const pageItem = e.target.closest('.page-item');
                if (pageItem.classList.contains('disabled')) return;

                const pageText = e.target.textContent.trim();
                const isPrevious = pageItem.querySelector('[aria-label="Previous"]');
                const isNext = pageItem.querySelector('[aria-label="Next"]');

                if (isPrevious) {
                    this.changePage(this.currentPage - 1);
                } else if (isNext) {
                    this.changePage(this.currentPage + 1);
                } else {
                    this.changePage(parseInt(pageText));
                }
            });
        });
    }

    bindStudentActionEvents() {
        document.querySelector('tbody').addEventListener('click', (e) => {
            const button = e.target.closest('.btn-view-details');
            if (button) {
                const studentId = this.getStudentIdFromButton(button);
                window.location.href = `student-plan.html?id=${studentId}`;
            }
        });

        document.querySelector('tbody').addEventListener('click', (e) => {
            const button = e.target.closest('.btn-edit-student');
            if (button) {
                const studentId = this.getStudentIdFromButton(button);
                window.location.href = `edit-Student.html`;
            }
        });

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
        const button = element.closest('button') || element;
        const row = button.closest('tr');
        const firstCell = row.querySelector('td:first-child');
        return firstCell.getAttribute('data-student-id');
    }

    async fetchStudents() {
        const spinner = document.querySelector('.loading-spinner');
        if (spinner) spinner.style.display = 'block';

        try {
            const response = await fetch('http://localhost:5000/api/getAll', {
                method: 'GET',
                headers: {
                    'Accept': 'application/json'
                },
                mode: 'cors',
                credentials: 'include'
            });

            if (!response.ok) {
                throw new Error('Failed to fetch students');
            }
            
            const data = await response.json();

            const studentsArray = Array.isArray(data) ? data : (data.students || data.data || []);
            
            this.students = studentsArray.map((student, index) => ({
                seqNumber: index + 1,
                id: student.student_id,
                name: student.name,
                age: student.age,
                memorizedParts: student.plan_info ? Math.round(student.plan_info.memorized_parts) : 0,
                percentage: student.plan_info ? `${Math.round(student.plan_info.memorized_parts / 0.3)}%` : '0%',
                lastUpdate: student.plan_info ? new Date(student.plan_info.updated_at).toLocaleDateString('ar-SA') : new Date(student.updated_at).toLocaleDateString('ar-SA'),
                evaluation: this.calculateEvaluation(student.recitations)
            }));
            this.updateStats(); 
            this.initializeTooltips();
            this.loadStudents();

            this.initializeTooltips();
            this.bindSearchEvent();
            this.bindFilterEvents();
            this.bindPaginationEvents();
            this.bindStudentActionEvents();

        } catch (error) {
            console.error('Error fetching students:', error);
            const tbody = document.querySelector('tbody');
            tbody.innerHTML = `
                <tr>
                    <td colspan="7" class="text-center text-danger">
                        <i class="fas fa-exclamation-circle me-2"></i>
                        حدث خطأ أثناء تحميل بيانات الطلاب
                    </td>
                </tr>
            `;
        } finally {
            if (spinner) spinner.style.display = 'none';
        }
    }

    calculateEvaluation(recitations) {
        if (!recitations || recitations.length === 0) return 'جديد';
        
        // Calculate average rating from last 5 recitations
        const recentRecitations = recitations.slice(-5);
        const avgRating = recentRecitations.reduce((sum, rec) => sum + (rec.rating || 0), 0) / recentRecitations.length;
        
        if (avgRating >= 90) return 'ممتاز';
        if (avgRating >= 80) return 'جيد جداً';
        if (avgRating >= 70) return 'جيد';
        if (avgRating >= 60) return 'مقبول';
        return 'ضعيف';
    }

    loadStudents() {
        const tbody = document.querySelector('tbody');
        tbody.innerHTML = '';
        const startIndex = (this.currentPage - 1) * this.itemsPerPage;

        if (this.students.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="7" class="text-center">
                        <i class="fas fa-info-circle me-2"></i>
                        لا يوجد طلاب مسجلين حالياً
                    </td>
                </tr>
            `;
            return;
        }

        const endIndex = startIndex + this.itemsPerPage;
        const paginatedStudents = this.students.slice(startIndex, endIndex);

        paginatedStudents.forEach((student, index) => {
            const row = document.createElement('tr');
            const memorizedParts = typeof student.memorizedParts === 'number' ? 
                `${student.memorizedParts} أجزاء` : student.memorizedParts;
            
            row.innerHTML = `
                <td data-student-id="${student.id}">${startIndex + index + 1}</td>
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

        // Update pagination UI
        this.updatePagination();
        this.updateStats();
        this.initializeTooltips();
    }

    updatePagination() {
        const totalPages = Math.ceil(this.students.length / this.itemsPerPage);
        const paginationContainer = document.querySelector('.pagination');
        
        if (!paginationContainer) return;

        let paginationHTML = `
            <li class="page-item ${this.currentPage === 1 ? 'disabled' : ''}">
                <a class="page-link" href="#" aria-label="Previous">
                    <span aria-hidden="true">&laquo;</span>
                </a>
            </li>`;

        for (let i = 1; i <= totalPages; i++) {
            paginationHTML += `
                <li class="page-item ${i === this.currentPage ? 'active' : ''}">
                    <a class="page-link" href="#">${i}</a>
                </li>`;
        }

        paginationHTML += `
            <li class="page-item ${this.currentPage === totalPages ? 'disabled' : ''}">
                <a class="page-link" href="#" aria-label="Next">
                    <span aria-hidden="true">&raquo;</span>
                </a>
            </li>`;

        paginationContainer.innerHTML = paginationHTML;
        this.bindPaginationEvents();
    }

    bindPaginationEvents() {
        document.querySelectorAll('.pagination .page-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const pageText = e.target.textContent.trim();
                const arrowClicked = e.target.closest('.page-link').getAttribute('aria-label');
    
                if (arrowClicked === 'Previous' || pageText === '«') {
                    this.changePage(this.currentPage - 1);
                } else if (arrowClicked === 'Next' || pageText === '»') {
                    this.changePage(this.currentPage + 1);
                } else {
                    const pageNumber = parseInt(pageText);
                    if (!isNaN(pageNumber)) {
                        this.changePage(pageNumber);
                    }
                }
            });
        });
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
        this.loadStudents();

    }

    viewStudentDetails(studentId) {
        const student = this.students.find(s => s.id === parseInt(studentId));
        if (!student) return;
        window.location.href = `student-plan.html?id=${student.id}`;
    }

    confirmDeleteStudent(studentId) {
        const student = this.students.find(s => s.id === studentId);
        if (!student) {
            this.showToast('الطالب غير موجود', 'error');
            return;
        }

        let deleteModal = document.getElementById('deleteStudentModal');
        if (!deleteModal) {
            const modalHtml = `
                <div class="modal fade" id="deleteStudentModal" tabindex="-1" aria-labelledby="deleteStudentModalLabel" aria-hidden="true">
                    <div class="modal-dialog modal-dialog-centered">
                        <div class="modal-content">
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

        deleteModal.querySelector('.student-name').textContent = `"${student.name}"`;

        const modal = new bootstrap.Modal(deleteModal);
        modal.show();

        // Remove any existing event listeners
        const confirmBtn = deleteModal.querySelector('.confirm-delete');
        const newConfirmBtn = confirmBtn.cloneNode(true);
        confirmBtn.parentNode.replaceChild(newConfirmBtn, confirmBtn);

        newConfirmBtn.addEventListener('click', async () => {
            try {
                const response = await fetch(`http://localhost:5000/api/deleteStudent/${studentId}`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    credentials: 'include'
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.error || 'فشل في حذف الطالب من قاعدة البيانات');
                }

                // Show success notification
                this.showToast('تم حذف الطالب بنجاح', 'success');
                
                // Close the modal and refresh the page
                modal.hide();
                setTimeout(() => {
                    window.location.reload();
                }, 1000); // Wait 1 second for the toast to be visible

            } catch (error) {
                console.error('Delete error:', error);
                this.showToast(error.message || 'حدث خطأ أثناء محاولة الحذف', 'error');
            }
        });
    }

    // Add this new method
    showToast(message, type) {
        const toast = new bootstrap.Toast(document.createElement('div'));
        toast._element.className = `toast align-items-center text-white bg-${type === 'success' ? 'success' : 'danger'} border-0 position-fixed bottom-0 end-0 m-3`;
        toast._element.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-times-circle'} me-2"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>`;
        document.body.appendChild(toast._element);
        toast.show();
        
        // Auto-remove toast after 5 seconds
        setTimeout(() => toast._element.remove(), 5000);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new StudentManager();
});