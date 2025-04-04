const progressSummary = {
    week: {
        memorization: '5 صفحات',
        majorRevision: '5 أجزاء',
        minorRevision: '15 صفحة'
    },
    twoWeeks: {
        memorization: '10 صفحات',
        majorRevision: '10 أجزاء',
        minorRevision: '30 صفحة'
    },
    month: {
        memorization: '30 صفحة',
        majorRevision: '30 جزء',
        minorRevision: '90 صفحة'
    }
};

// Student Plan Manager Class
class StudentPlanManager {
    constructor() {
        this.initializeData();
        this.loadStudentInfo().then(() => {
            this.bindElements();
            this.bindEvents();
            this.generateAllPlans();
            this.setupPrintOptimization();
            this.updateProgressSummary('week');
        });
    }

    initializeData() {
        this.arabicMonths = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"];
        this.arabicDays = ["الأحد", "الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت"];
        this.editMode = false;
        this.originalValues = {}; 
    }

    async loadStudentInfo() {
        const urlParams = new URLSearchParams(window.location.search);
        const studentId = parseInt(urlParams.get('id'));
        
        let studentInfo;
        
        if (studentId) {
            try {
                const response = await fetch(`http://localhost:5000/api/getStudent/${studentId}`, {
                    method: 'GET',
                    headers: {
                        'Accept': 'application/json'
                    },
                    mode: 'cors',
                    credentials: 'include'
                });

                if (!response.ok) {
                    throw new Error('Failed to fetch student info');
                }

                studentInfo = await response.json();
            } catch (error) {
                console.error('Error fetching student:', error);
                this.showNotification('حدث خطأ أثناء تحميل بيانات الطالب', 'danger');
            }
        }
        
        if (!studentInfo) {
            studentInfo = {
                name: 'طالب جديد',
                age: 14,
                memorizedParts: 5
            };
        }
        
        document.getElementById('studentName').textContent = studentInfo.name;
        document.getElementById('studentInfo').textContent = 
            `العمر: ${studentInfo.age} سنة | الأجزاء المحفوظة: ${studentInfo.plan_info?.memorized_parts || 0}`;
    }

    bindElements() {
        this.periodButtons = document.querySelectorAll('.time-period-selector .btn');
        this.planPeriods = document.querySelectorAll('.plan-period');
        this.printButton = document.getElementById('printPlan');
        this.editButton = document.getElementById('editPlan');
        this.saveButton = document.getElementById('savePlan');
        this.cancelButton = document.getElementById('cancelEdit');
        this.weekPlanBody = document.getElementById('weekPlanBody');
        this.twoWeeksPlanBody = document.getElementById('twoWeeksPlanBody');
        this.monthPlanBody = document.getElementById('monthPlanBody');
        this.memorizationSummary = document.getElementById('memorizationSummary');
        this.majorRevisionSummary = document.getElementById('majorRevisionSummary');
        this.minorRevisionSummary = document.getElementById('minorRevisionSummary');
    }

    bindEvents() {
        this.periodButtons.forEach(button => {
            button.addEventListener('click', this.handlePeriodChange.bind(this));
        });

        this.printButton.addEventListener('click', () => {
            // this.optimizeForPrint();
            window.print();
            // this.resetAfterPrint();
        });

        this.editButton.addEventListener('click', this.enterEditMode.bind(this));
        this.saveButton.addEventListener('click', this.saveChanges.bind(this));
        this.cancelButton.addEventListener('click', this.cancelEdit.bind(this));
    }

    generateAllPlans() {
        this.generateWeekPlan();
        this.generateTwoWeeksPlan();
        this.generateMonthPlan();
        
        this.editableFields = document.querySelectorAll('.editable');
    }

    generateWeekPlan() {
        let html = '';
        for (let i = 0; i < 5; i++) {
            const dayNum = i + 1;
            const dayName = this.arabicDays[i];
            const date = new Date(2025, 2, 5 + i); 
            const dateStr = `${date.getDate()} ${this.arabicMonths[date.getMonth()]} ${date.getFullYear()}`;

            html += `
            <tr>
                <td>${dayNum}</td>
                <td class="day-col">${dayName}</td>
                <td class="date-col">${dateStr}</td>
                <td class="editable" data-field="memFrom" data-day="${dayNum}">سورة البقرة (آية ${i * 5 + 31})</td>
                <td class="editable" data-field="memTo" data-day="${dayNum}">سورة البقرة (آية ${i * 5 + 35})</td>
                <td class="editable" data-field="majorRev" data-day="${dayNum}">جزء ${this.getPartName(i)}</td>
                <td class="editable" data-field="minorRevFrom" data-day="${dayNum}">سورة البقرة (آية ${i * 5 + 16})</td>
                <td class="editable" data-field="minorRevTo" data-day="${dayNum}">سورة البقرة (آية ${i * 5 + 30})</td>
            </tr>
            `;
        }
        this.weekPlanBody.innerHTML = html;
    }

    generateTwoWeeksPlan() {
        let html = '';
        for (let i = 0; i < 10; i++) {
            const dayNum = i + 1;
            const dayIndex = i % 5;
            const dayName = this.arabicDays[dayIndex];
            const date = new Date(2025, 2, 5 + i); 
            const dateStr = `${date.getDate()} ${this.arabicMonths[date.getMonth()]} ${date.getFullYear()}`;

            html += `
            <tr>
                <td>${dayNum}</td>
                <td class="day-col">${dayName}</td>
                <td class="date-col">${dateStr}</td>
                <td class="editable" data-field="memFrom" data-day="${dayNum}">سورة البقرة (آية ${i * 5 + 31})</td>
                <td class="editable" data-field="memTo" data-day="${dayNum}">سورة البقرة (آية ${i * 5 + 35})</td>
                <td class="editable" data-field="majorRev" data-day="${dayNum}">جزء ${this.getPartName(i)}</td>
                <td class="editable" data-field="minorRevFrom" data-day="${dayNum}">سورة البقرة (آية ${i * 5 + 16})</td>
                <td class="editable" data-field="minorRevTo" data-day="${dayNum}">سورة البقرة (آية ${i * 5 + 30})</td>
            </tr>
            `;
        }
        this.twoWeeksPlanBody.innerHTML = html;
    }

    generateMonthPlan() {
        let html = '';
        for (let i = 0; i < 30; i++) { 
            const dayNum = i + 1;
            const dayIndex = i % 5;
            const dayName = this.arabicDays[dayIndex];
            const date = new Date(2025, 2, 5 + i);
            const dateStr = `${date.getDate()} ${this.arabicMonths[date.getMonth()]} ${date.getFullYear()}`;

            html += `
            <tr>
                <td>${dayNum}</td>
                <td class="day-col">${dayName}</td>
                <td class="date-col">${dateStr}</td>
                <td class="editable" data-field="memFrom" data-day="${dayNum}">سورة البقرة (آية ${i * 5 + 31})</td>
                <td class="editable" data-field="memTo" data-day="${dayNum}">سورة البقرة (آية ${i * 5 + 35})</td>
                <td class="editable" data-field="majorRev" data-day="${dayNum}">جزء ${this.getPartName(i)}</td>
                <td class="editable" data-field="minorRevFrom" data-day="${dayNum}">سورة البقرة (آية ${i * 5 + 16})</td>
                <td class="editable" data-field="minorRevTo" data-day="${dayNum}">سورة البقرة (آية ${i * 5 + 30})</td>
            </tr>
            `;
        }
        this.monthPlanBody.innerHTML = html;
    }

    getPartName(index) {
        return (index % 30) + 1;
    }

    handlePeriodChange(event) {
        if (this.editMode) {
            if (!confirm("سيتم فقدان التغييرات إذا قمت بتغيير الفترة. هل تريد المتابعة؟")) {
                return;
            }
            this.cancelEdit();
        }

        this.periodButtons.forEach(btn => btn.classList.remove('active'));

        event.currentTarget.classList.add('active');

        this.planPeriods.forEach(period => period.style.display = 'none');

        const selectedPeriod = event.currentTarget.getAttribute('data-period');
        document.getElementById(`${selectedPeriod}Plan`).style.display = 'block';

        this.editableFields = document.querySelectorAll('.editable');

        this.updateProgressSummary(selectedPeriod);
    }

    enterEditMode() {
        this.editMode = true;
        document.body.classList.add('edit-mode');
        this.editButton.style.display = 'none';
        this.saveButton.style.display = 'block';
        this.cancelButton.style.display = 'block';

        this.editableFields.forEach(field => {
            const fieldId = `${field.dataset.field}-${field.dataset.day || '0'}`;
            this.originalValues[fieldId] = field.textContent;
            field.contentEditable = true;

            field.addEventListener('click', this.selectAllContent);
        });
    }

    selectAllContent(e) {
        if (document.body.classList.contains('edit-mode')) {
            const range = document.createRange();
            range.selectNodeContents(e.target);
            const selection = window.getSelection();
            selection.removeAllRanges();
            selection.addRange(range);
        }
    }

    saveChanges() {
        this.editMode = false;
        document.body.classList.remove('edit-mode');
        this.editButton.style.display = 'block';
        this.saveButton.style.display = 'none';
        this.cancelButton.style.display = 'none';

        this.editableFields.forEach(field => {
            field.contentEditable = false;
            field.removeEventListener('click', this.selectAllContent);
        });

        console.log('Changes saved!');

        this.showNotification('تم حفظ التغييرات بنجاح!', 'success');
    }

    cancelEdit() {
        this.editMode = false;
        document.body.classList.remove('edit-mode');
        this.editButton.style.display = 'block';
        this.saveButton.style.display = 'none';
        this.cancelButton.style.display = 'none';

        this.editableFields.forEach(field => {
            field.contentEditable = false;
            const fieldId = `${field.dataset.field}-${field.dataset.day || '0'}`;
            if (this.originalValues[fieldId]) {
                field.textContent = this.originalValues[fieldId];
            }
            field.removeEventListener('click', this.selectAllContent);
        });

        this.originalValues = {};
    }

    updateProgressSummary(period) {
        if (progressSummary[period]) {
            this.memorizationSummary.textContent = progressSummary[period].memorization;
            this.majorRevisionSummary.textContent = progressSummary[period].majorRevision;
            this.minorRevisionSummary.textContent = progressSummary[period].minorRevision;
        }
    }

    setupPrintOptimization() {
        const printStyles = document.createElement('style');
        printStyles.id = 'print-optimization-styles';
        printStyles.textContent = `
            @media print {
                .plan-table { 
                    font-size: 8pt !important; 
                    width: 100% !important;
                }
                .plan-table th, .plan-table td {
                    padding: 2px !important;
                }
                .main-container {
                    padding: 0.5rem !important;
                }
                .plan-table tr { 
                    page-break-inside: avoid !important; 
                }
                .container {
                    width: 100% !important;
                    padding: 0 !important;
                    margin: 0 !important;
                }
                .progress-summary-row {
                    margin-top: 5px !important;
                }
                .student-info-card {
                    padding: 5px !important;
                    margin-bottom: 5px !important;
                }
                .container-header {
                    margin-bottom: 5px !important;
                    padding-bottom: 5px !important;
                    border-bottom-width: 1px !important;
                }
            }
        `;
        document.head.appendChild(printStyles);
    }

    optimizeForPrint() {
        document.body.classList.add('printing');
        document.querySelectorAll('.no-print').forEach(el => {
            el.style.display = 'none';
        });
    }

    resetAfterPrint() {
        document.body.classList.remove('printing');
        document.querySelectorAll('.no-print').forEach(el => {
            el.style.display = '';
        });
    }

    showNotification(message, type = 'success') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} position-fixed top-0 start-50 translate-middle-x mt-3`;
        notification.style.zIndex = '1050';
        notification.textContent = message;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    confirmDeleteStudent(studentId) {
        if (confirm('هل أنت متأكد من حذف هذا الطالب؟')) {
            console.log(`Deleting student with ID: ${studentId}`);
            this.showNotification('تم حذف الطالب بنجاح');
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new StudentPlanManager();
});