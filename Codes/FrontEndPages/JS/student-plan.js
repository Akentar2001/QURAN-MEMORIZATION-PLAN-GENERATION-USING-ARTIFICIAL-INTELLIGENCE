const progressSummary = {
    week: {
        memorization: 'البقرة: 1-25',
        majorRevision: 'البقرة: 1-100',
        minorRevision: 'البقرة: 1-50'
    },
};

// Student Plan Manager Class
class StudentPlanManager {
    constructor() {
        this.initializeData();
        this.initializeData();
    Promise.all([
        this.loadStudentInfo(),
        this.loadStudentSessions()
    ]).then(() => {
        this.bindElements();
        this.bindEvents();
        this.generatePlan();
        this.setupPrintOptimization();
        this.updateProgressSummary('week');
    });
    }

    initializeData() {
        this.arabicMonths = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"];
        this.arabicDays = ["الأحد", "الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت"];
    }

    async loadStudentInfo() {
        const urlParams = new URLSearchParams(window.location.search);
        const studentId = parseInt(urlParams.get('id'));
        
        let studentInfo;
        
        if (studentId) {
            try {
                const response = await fetch(`http://localhost:5000/api/students/getStudent/${studentId}`, {
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
        
        if (studentInfo) {
            document.getElementById('studentName').textContent = studentInfo.name;
            document.getElementById('studentInfo').textContent = 
            `العمر: ${studentInfo.age} سنة | الأجزاء المحفوظة: ${studentInfo.plan_info?.memorized_parts || 0}`;
        } else {
            document.getElementById('studentName').textContent = 'اسم الطالب';
            this.showNotification('حدث خطأ أثناء تحميل بيانات الطالب', 'danger');
        }
        
    }

    async loadStudentSessions() {
        const urlParams = new URLSearchParams(window.location.search);
        const studentId = parseInt(urlParams.get('id'));
        
        if (studentId) {
            try {
                const response = await fetch(`http://localhost:5000/api/recitation_session/sessions/student/${studentId}`, {
                    method: 'GET',
                    headers: {
                        'Accept': 'application/json'
                    },
                    mode: 'cors',
                    credentials: 'include'
                });
    
                if (!response.ok) {
                    throw new Error('Failed to fetch sessions');
                }
                
                const sessions = await response.json();
                
                this.sessions = {
                    memorization: sessions.filter(session => session.type === 'New_Memorization'),
                    minorRevision: sessions.filter(session => session.type === 'Minor_Revision'),
                    majorRevision: sessions.filter(session => session.type === 'Major_Revision')
                };
                return this.sessions;
    
            } catch (error) {
                console.error('Error fetching sessions:', error);
                this.showNotification('حدث خطأ أثناء تحميل جلسات الحفظ', 'danger');
                return { memorization: [], minorRevision: [], majorRevision: [] };
            }
        }
        return { memorization: [], minorRevision: [], majorRevision: [] };
    }

    bindElements() {
        this.printButton = document.getElementById('printPlan');
        this.weekPlanBody = document.getElementById('weekPlanBody');
        this.memorizationSummary = document.getElementById('memorizationSummary');
        this.majorRevisionSummary = document.getElementById('majorRevisionSummary');
        this.minorRevisionSummary = document.getElementById('minorRevisionSummary');
    }

    bindEvents() {
        this.printButton.addEventListener('click', () => {
            window.print();
        });
    }

    generatePlan() {
        let html = '';
        const defaultSession = {
            start_verse: { surah_name: '-', order_in_surah: '-' },
            end_verse: { surah_name: '-', order_in_surah: '-' }
        };
    
        const hasMemorization = this.sessions?.memorization?.length > 0;
        const hasMinorRevision = this.sessions?.minorRevision?.length > 0;
        const hasMajorRevision = this.sessions?.majorRevision?.length > 0;

        const numDays = Math.max(
            this.sessions?.memorization?.length || 0,
            this.sessions?.minorRevision?.length || 0,
            this.sessions?.majorRevision?.length || 0,
            1
        );
    
        if (!hasMemorization && !hasMinorRevision && !hasMajorRevision) {
            html += `
            <tr>
                <td>1</td>
                <td class="day-col">${this.arabicDays[0]}</td>
                <td class="date-col">${this.formatDate(new Date())}</td>
                <td colspan="4" class="memorization-cell text-center">لا يوجد حفظ جديد للطالب</td>
                <td colspan="4" class="minor-revision-cell text-center">لا يوجد مراجعة صغرى للطالب</td>
                <td colspan="4" class="major-revision-cell text-center">لا يوجد مراجعة كبرى للطالب</td>
            </tr>`;
        } else {
            for (let i = 0; i < numDays; i++) {
                const dayNum = i + 1;
                const dayName = this.arabicDays[i];
                const date = new Date();
                date.setDate(date.getDate() + i);
                const dateStr = this.formatDate(date);
                
                html += `
                <tr>
                    <td>${dayNum}</td>
                    <td class="day-col">${dayName}</td>
                    <td class="date-col">${dateStr}</td>
                    ${hasMemorization ? `
                        <td class="memorization-cell">${this.sessions.memorization[i]?.start_verse?.surah_name || '-'}</td>
                        <td class="memorization-cell">${this.sessions.memorization[i]?.start_verse?.order_in_surah || '-'}</td>
                        <td class="memorization-cell">${this.sessions.memorization[i]?.end_verse?.surah_name || '-'}</td>
                        <td class="memorization-cell">${this.sessions.memorization[i]?.end_verse?.order_in_surah || '-'}</td>
                    ` : '<td colspan="4" class="memorization-cell text-center">لا يوجد حفظ جديد للطالب</td>'}
                    ${hasMinorRevision ? `
                        <td class="minor-revision-cell">${this.sessions.minorRevision[i]?.start_verse?.surah_name || '-'}</td>
                        <td class="minor-revision-cell">${this.sessions.minorRevision[i]?.start_verse?.order_in_surah || '-'}</td>
                        <td class="minor-revision-cell">${this.sessions.minorRevision[i]?.end_verse?.surah_name || '-'}</td>
                        <td class="minor-revision-cell">${this.sessions.minorRevision[i]?.end_verse?.order_in_surah || '-'}</td>
                    ` : '<td colspan="4" class="minor-revision-cell text-center">لا يوجد مراجعة صغرى للطالب</td>'}
                    ${hasMajorRevision ? `
                        <td class="major-revision-cell">${this.sessions.majorRevision[i]?.start_verse?.surah_name || '-'}</td>
                        <td class="major-revision-cell">${this.sessions.majorRevision[i]?.start_verse?.order_in_surah || '-'}</td>
                        <td class="major-revision-cell">${this.sessions.majorRevision[i]?.end_verse?.surah_name || '-'}</td>
                        <td class="major-revision-cell">${this.sessions.majorRevision[i]?.end_verse?.order_in_surah || '-'}</td>
                    ` : '<td colspan="4" class="major-revision-cell text-center">لا يوجد مراجعة كبرى للطالب</td>'}
                </tr>`;
            }
        }
        this.weekPlanBody.innerHTML = html;
    }
    
    formatDate(date) {
        return `${date.getDate()} ${this.arabicMonths[date.getMonth()]} ${date.getFullYear()}`;
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

}

document.addEventListener('DOMContentLoaded', () => {
    new StudentPlanManager();
});