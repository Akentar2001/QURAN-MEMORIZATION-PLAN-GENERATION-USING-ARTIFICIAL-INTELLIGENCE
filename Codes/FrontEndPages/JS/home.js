class StudentManager {
    constructor() {
        this.students = [];
        this.originalStudents = [];
        this.currentPage = 1;
        this.itemsPerPage = 10;
        this.initializeTooltips();
        this.bindSearchEvent();
        this.bindFilterEvents();
        this.bindStudentActionEvents();
        
        const paginationNav = document.querySelector('nav[aria-label="Page navigation"]');
        if (paginationNav) {
            paginationNav.style.display = 'none';
        }

        this.fetchStudents();
    }

    static EVALUATION = {
        NEW: 'جديد',
        EXCELLENT: 'ممتاز',
        VERY_GOOD: 'جيد جداً',
        GOOD: 'جيد',
        FAIR: 'مقبول',
        WEAK: 'ضعيف'
    };

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
                window.location.href = `edit-Student.html?id=${studentId}`;
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
            const response = await fetch('http://localhost:5000/api/students/getAll', {
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
                rawDate: student.plan_info ? new Date(student.plan_info.updated_at) : new Date(student.updated_at),
                lastUpdate: student.plan_info ? new Date(student.plan_info.updated_at).toLocaleDateString('ar-SA') : new Date(student.updated_at).toLocaleDateString('ar-SA'),
                overall_rating: student.plan_info ? student.plan_info.overall_rating : null,
                evaluation: this.calculateEvaluation(student.plan_info ? student.plan_info.overall_rating : null)
            }));
            
            this.originalStudents = [...this.students];
            this.updateStats(); 
            this.loadStudents();
            
            this.initializeTooltips();
            

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

    calculateEvaluation(overall_rating) {
        if (!overall_rating) return StudentManager.EVALUATION.NEW;
        
        if (overall_rating > 4) return StudentManager.EVALUATION.EXCELLENT;
        if (overall_rating > 3) return StudentManager.EVALUATION.VERY_GOOD;
        if (overall_rating > 2) return StudentManager.EVALUATION.GOOD;
        if (overall_rating > 1) return StudentManager.EVALUATION.FAIR;
        return StudentManager.EVALUATION.WEAK;
    }

    loadStudents() {
        const tbody = document.querySelector('tbody');
        tbody.innerHTML = '';
        const startIndex = (this.currentPage - 1) * this.itemsPerPage;
        const paginationNav = document.querySelector('nav[aria-label="Page navigation"]');  

        if (this.students.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="7" class="text-center">
                        <i class="fas fa-info-circle me-2"></i>
                        لا يوجد طلاب حالياً
                    </td>
                </tr>
            `;
            if (paginationNav) paginationNav.style.display = 'none';
            return;
        }   

        if (paginationNav) paginationNav.style.display = 'block';
    
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

        this.updatePagination();
        this.initializeTooltips();
    }

    updatePagination() {
        const totalPages = Math.ceil(this.students.length / this.itemsPerPage);
        const paginationContainer = document.querySelector('.pagination');
        
        if (!paginationContainer) return;

        if (totalPages <= 1) {
            paginationContainer.innerHTML = '';
            return;
        }

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
            case StudentManager.EVALUATION.EXCELLENT: return 'bg-success';
            case StudentManager.EVALUATION.VERY_GOOD: return 'bg-primary';
            case StudentManager.EVALUATION.GOOD: return 'bg-warning text-dark';
            case StudentManager.EVALUATION.FAIR: return 'bg-info';
            case StudentManager.EVALUATION.WEAK: return 'bg-danger';
            default: return 'bg-secondary';
        }
    }
    
    updateStats() {
        const statsCards = {
            totalStudents: document.querySelector('.col-md-4:nth-child(1) .card-body h2'),
            averageParts: document.querySelector('.col-md-4:nth-child(2) .card-body h2'),
            excellentStudents: document.querySelector('.col-md-4:nth-child(3) .card-body h2')
        };

        const totalStudents = this.students.length;
        if (statsCards.totalStudents) {
            if(totalStudents === 0)
                statsCards.totalStudents.textContent = 'لا يوجد طلاب';
            else if(totalStudents === 1)
                statsCards.totalStudents.textContent = `طالب واحد`;
            else if(totalStudents === 2)
                statsCards.totalStudents.textContent = `طالبان`;
            else if(totalStudents >= 3 && totalStudents <= 10)
                statsCards.totalStudents.textContent = `${totalStudents} طلاب`;
            else
                statsCards.totalStudents.textContent = `${totalStudents} طالب`;
        }

        const totalParts = this.students.reduce((sum, student) => sum + student.memorizedParts, 0);
        const averageParts = totalStudents > 0 ? (totalParts / totalStudents).toFixed(1) : 0;
        
        if (statsCards.averageParts) {
            statsCards.averageParts.textContent = `${averageParts} أجزاء`;
        }

        const excellentCount = this.students.filter(student => student.evaluation === StudentManager.EVALUATION.EXCELLENT).length;
        if (statsCards.excellentStudents) {
            if(excellentCount === 0)
                statsCards.excellentStudents.textContent = 'لا يوجد';
            else if(excellentCount === 1)
                statsCards.excellentStudents.textContent = `طالب واحد`;
            else if(excellentCount === 2)
                statsCards.excellentStudents.textContent = `طالبان`;
            else if(excellentCount >= 3 && excellentCount <= 10)
                statsCards.excellentStudents.textContent = `${excellentCount} طلاب`;
            else
                statsCards.excellentStudents.textContent = `${excellentCount} طالب`;
        }
    }

    filterStudents(searchTerm) {
        searchTerm = searchTerm.toLowerCase();
        
        const filteredStudents = this.originalStudents.filter(student => 
            student.name.toLowerCase().includes(searchTerm)
        );

        this.students = filteredStudents;
        
        this.currentPage = 1;
        this.loadStudents();
        
    }

    applyFilter(filterType) {
        if (!this.students || !this.students.length) return;

        if (filterType === 'أعلى تقييم') {
            this.students.sort((a, b) => {
                const evalOrder = [
                    StudentManager.EVALUATION.EXCELLENT,
                    StudentManager.EVALUATION.VERY_GOOD,
                    StudentManager.EVALUATION.GOOD,
                    StudentManager.EVALUATION.FAIR,
                    StudentManager.EVALUATION.WEAK,
                    StudentManager.EVALUATION.NEW
                ];
                const indexA = evalOrder.indexOf(a.evaluation);
                const indexB = evalOrder.indexOf(b.evaluation);
                
                return indexA - indexB;
            });
        } else if (filterType === 'الأكثر حفظًا') {
            this.students.sort((a, b) => b.memorizedParts - a.memorizedParts);
        } else if (filterType === 'الأحدث') {
            this.students.sort((a, b) => b.rawDate - a.rawDate); 
        } else if (filterType === 'إعادة ضبط') {
            this.students.sort((a, b) => a.id - b.id);
        }

        this.currentPage = 1;
        this.loadStudents();
    }

    filterByEvaluation(evaluation) {
        if (evaluation === 'الكل') {
            this.students = [...this.originalStudents];
            this.loadStudents();
            return;
        }

        const filteredStudents = this.originalStudents.filter(student => student.evaluation === evaluation);
        this.students = filteredStudents;
        
        this.currentPage = 1;
        this.loadStudents();
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

    async confirmDeleteStudent(studentId) {
        const student = this.students.find(s => s.id === studentId);
        if (!student) {
            this.showToast('الطالب غير موجود', 'error');
            return;
        }

        const existingModal = document.getElementById('deleteStudentModal');
        if (existingModal) {
            existingModal.remove();
        }
        const existingBackdrop = document.querySelector('.modal-backdrop');
        if (existingBackdrop) {
            existingBackdrop.remove();
        }
        document.body.classList.remove('modal-open');

        const modalHtml = `
            <div class="modal fade" id="deleteStudentModal" tabindex="-1" aria-labelledby="deleteStudentModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content">
                        <div class="modal-body text-center">
                            <i class="fas fa-user-times fa-4x text-danger mb-3"></i>
                            <p class="fs-5">هل أنت متأكد من حذف الطالب</p>
                            <p class="fs-4 fw-bold text-danger student-name">"${student.name}"</p>
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
        const deleteModal = document.getElementById('deleteStudentModal');
        const modal = new bootstrap.Modal(deleteModal);

        deleteModal.addEventListener('hidden.bs.modal', () => {
            document.body.classList.remove('modal-open');
            const backdrop = document.querySelector('.modal-backdrop');
            if (backdrop) backdrop.remove();
            deleteModal.remove();
        });

        const confirmBtn = deleteModal.querySelector('.confirm-delete');
        confirmBtn.addEventListener('click', async () => {
            try {
                const response = await fetch(`http://localhost:5000/api/students/delete/${studentId}`, {
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

                this.showToast('تم حذف الطالب بنجاح', 'success');
                modal.hide();
                
                deleteModal.remove();
                const backdrop = document.querySelector('.modal-backdrop');
                if (backdrop) backdrop.remove();
                document.body.classList.remove('modal-open');
                
                setTimeout(() => window.location.reload(), 1000);

            } catch (error) {
                console.error('Delete error:', error);
                this.showToast(error.message || 'حدث خطأ أثناء محاولة الحذف', 'error');
            }
        });

        modal.show();
    }

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
        
        setTimeout(() => toast._element.remove(), 5000);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new StudentManager();
});