// Student data
// const studentData = {
//     name: 'أحمد محمد',
//     age: 14,
//     memorizedParts: 5
// };

// Initial progress summary data
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
        this.loadStudentInfo();
        this.bindElements();
        this.bindEvents();
        this.generateAllPlans();
        this.setupPrintOptimization();
        this.updateProgressSummary('week');
    }

    initializeData() {
        this.arabicMonths = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"];
        this.arabicDays = ["الأحد", "الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت"];
        this.editMode = false;
        this.originalValues = {}; // Store original values for cancel functionality
    }

    loadStudentInfo() {
        // Get student ID from URL
        const urlParams = new URLSearchParams(window.location.search);
        const studentId = parseInt(urlParams.get('id'));
        
        let studentInfo;
        
        if (studentId) {
            // Try to find student data from students array
            studentInfo = students.find(s => s.id === studentId);
        }
        
        // If no student found or no ID provided, use default data
        if (!studentInfo) {
            studentInfo = {
                name: 'طالب جديد',
                age: 14,
                memorizedParts: 5
            };
        }
        
        // Update student info
        document.getElementById('studentName').textContent = studentInfo.name;
        document.getElementById('studentInfo').textContent = 
            `العمر: ${studentInfo.age} سنة | الأجزاء المحفوظة: ${studentInfo.memorizedParts}`;
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
        // Time period selector functionality
        this.periodButtons.forEach(button => {
            button.addEventListener('click', this.handlePeriodChange.bind(this));
        });

        // Print functionality
        this.printButton.addEventListener('click', () => {
            // this.optimizeForPrint();
            window.print();
            // this.resetAfterPrint();
        });

        // Edit functionality
        this.editButton.addEventListener('click', this.enterEditMode.bind(this));
        this.saveButton.addEventListener('click', this.saveChanges.bind(this));
        this.cancelButton.addEventListener('click', this.cancelEdit.bind(this));
    }

    generateAllPlans() {
        this.generateWeekPlan();
        this.generateTwoWeeksPlan();
        this.generateMonthPlan();
        
        // Update editable fields after generating content
        this.editableFields = document.querySelectorAll('.editable');
    }

    generateWeekPlan() {
        let html = '';
        for (let i = 0; i < 5; i++) { // 5 days for a week (Sunday to Thursday)
            const dayNum = i + 1;
            const dayName = this.arabicDays[i];
            const date = new Date(2025, 2, 5 + i); // March 5, 2025 + i days
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
        for (let i = 0; i < 10; i++) { // 14 days for two weeks
            const dayNum = i + 1;
            const dayIndex = i % 5;
            const dayName = this.arabicDays[dayIndex];
            const date = new Date(2025, 2, 5 + i); // March 5, 2025 + i days
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
        for (let i = 0; i < 30; i++) { // 30 days for a month
            const dayNum = i + 1;
            const dayIndex = i % 5;
            const dayName = this.arabicDays[dayIndex];
            const date = new Date(2025, 2, 5 + i); // March 5, 2025 + i days
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

    // Helper function to get Quran part names for specific indices
    getPartName(index) {
        return (index % 30) + 1;
    }

    handlePeriodChange(event) {
        // If in edit mode, ask for confirmation before changing period
        if (this.editMode) {
            if (!confirm("سيتم فقدان التغييرات إذا قمت بتغيير الفترة. هل تريد المتابعة؟")) {
                return;
            }
            // Exit edit mode if continuing
            this.cancelEdit();
        }

        // Remove active class from all buttons
        this.periodButtons.forEach(btn => btn.classList.remove('active'));

        // Add active class to clicked button
        event.currentTarget.classList.add('active');

        // Hide all plan periods
        this.planPeriods.forEach(period => period.style.display = 'none');

        // Show selected plan period
        const selectedPeriod = event.currentTarget.getAttribute('data-period');
        document.getElementById(`${selectedPeriod}Plan`).style.display = 'block';

        // Refresh editable fields after changing period
        this.editableFields = document.querySelectorAll('.editable');

        // Update progress summary based on selected period
        this.updateProgressSummary(selectedPeriod);
    }

    enterEditMode() {
        this.editMode = true;
        document.body.classList.add('edit-mode');
        this.editButton.style.display = 'none';
        this.saveButton.style.display = 'block';
        this.cancelButton.style.display = 'block';

        // Store original values and make fields editable
        this.editableFields.forEach(field => {
            const fieldId = `${field.dataset.field}-${field.dataset.day || '0'}`;
            this.originalValues[fieldId] = field.textContent;
            field.contentEditable = true;

            // Add click listener to highlight entire content when clicked
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

        // Make fields non-editable
        this.editableFields.forEach(field => {
            field.contentEditable = false;
            field.removeEventListener('click', this.selectAllContent);
        });

        // Here you would typically save the changes to a database
        console.log('Changes saved!');

        // Show success message
        this.showNotification('تم حفظ التغييرات بنجاح!', 'success');
    }

    cancelEdit() {
        // Revert all changes and exit edit mode
        this.editMode = false;
        document.body.classList.remove('edit-mode');
        this.editButton.style.display = 'block';
        this.saveButton.style.display = 'none';
        this.cancelButton.style.display = 'none';

        // Restore original content
        this.editableFields.forEach(field => {
            field.contentEditable = false;
            const fieldId = `${field.dataset.field}-${field.dataset.day || '0'}`;
            if (this.originalValues[fieldId]) {
                field.textContent = this.originalValues[fieldId];
            }
            field.removeEventListener('click', this.selectAllContent);
        });

        // Reset original values
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
        // Add print-specific styles dynamically
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
        // Hide non-printable elements
        document.querySelectorAll('.no-print').forEach(el => {
            el.style.display = 'none';
        });
    }

    resetAfterPrint() {
        document.body.classList.remove('printing');
        // Restore non-printable elements
        document.querySelectorAll('.no-print').forEach(el => {
            el.style.display = '';
        });
    }

    showNotification(message, type = 'success') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} position-fixed top-0 start-50 translate-middle-x mt-3`;
        notification.style.zIndex = '1050';
        notification.textContent = message;

        // Add to document
        document.body.appendChild(notification);

        // Remove after 3 seconds
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    confirmDeleteStudent(studentId) {
        if (confirm('هل أنت متأكد من حذف هذا الطالب؟')) {
            // Here you would typically make an API call to delete the student
            console.log(`Deleting student with ID: ${studentId}`);
            this.showNotification('تم حذف الطالب بنجاح');
        }
    }
}

// Initialize the StudentPlanManager when the document is ready
document.addEventListener('DOMContentLoaded', () => {
    new StudentPlanManager();
});