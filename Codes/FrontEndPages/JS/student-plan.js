class StudentPlanManager {
    constructor() {
        this.initializeData();
    Promise.all([
        this.loadStudentInfo(),
        this.loadStudentSessions()
    ]).then(() => {
        this.bindElements();
        this.bindEvents();
        this.generatePlan();
        this.setupPrintOptimization();
        this.updateProgressSummary();
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
            // document.getElementById('studentInfo').textContent = 
            // `العمر: ${studentInfo.age} سنة | الأجزاء المحفوظة: ${studentInfo.plan_info?.memorized_parts || 0}`;
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
                const response = await fetch(`http://localhost:5000/api/recitation_session/getSessions/student/${studentId}`, {
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
                
                const data = await response.json();
                const sessions = Array.isArray(data) ? data : [];

                const sessionsByDate = {};
                sessions.forEach(session => {
                    if (!session.date) return;
                    
                    const dateObj = new Date(session.date);
                    const dateStr = dateObj.toISOString().split('T')[0];

                    if (!sessionsByDate[dateStr]) {
                        sessionsByDate[dateStr] = {
                            memorization: null,
                            minorRevision: null,
                            majorRevision: null
                        };
                    }
                    
                    switch (session.type) {
                        case 'New_Memorization':
                            sessionsByDate[dateStr].memorization = session;
                            break;
                        case 'Minor_Revision':
                            sessionsByDate[dateStr].minorRevision = session;
                            break;
                        case 'Major_Revision':
                            sessionsByDate[dateStr].majorRevision = session;
                            break;
                    }
                });
                
                this.sessions = sessionsByDate;
                return this.sessions;
    
            } catch (error) {
                console.error('Error fetching sessions:', error);
                this.showNotification('حدث خطأ أثناء تحميل جلسات الحفظ', 'danger');
                return {};
            }
        }
        return {};
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
        const dates = Object.keys(this.sessions || {}).sort();
        
        if (!this.sessions || Object.keys(this.sessions).length === 0) {
            html = `
            <tr>
                <td colspan="15" class="text-center" style="font-size: 1.1rem; padding: 20px; font-weight: bold;">لا توجد خطة للطالب لهذا الأسبوع</td>
            </tr>`;
        } else {
            dates.forEach((date, index) => {
                const currentDate = new Date(date);
                const dayName = this.arabicDays[currentDate.getDay()];
                const dateStr = this.formatDate(currentDate);
                const daySession = this.sessions[date];
                
                html += `
                <tr>
                    <td>${index + 1}</td>
                    <td class="day-col">${dayName}</td>
                    <td class="date-col">${dateStr}</td>
                    ${daySession?.memorization ? `
                        <td class="memorization-cell">${daySession.memorization.start_verse?.surah_name || '-'}</td>
                        <td class="memorization-cell">${daySession.memorization.start_verse?.order_in_surah || '-'}</td>
                        <td class="memorization-cell">${daySession.memorization.end_verse?.surah_name || '-'}</td>
                        <td class="memorization-cell">${daySession.memorization.end_verse?.order_in_surah || '-'}</td>
                    ` : '<td colspan="4" class="memorization-cell text-center">لا يوجد حفظ جديد للطالب</td>'}
                    ${daySession.minorRevision ? `
                        <td class="minor-revision-cell">${daySession.minorRevision.start_verse.surah_name}</td>
                        <td class="minor-revision-cell">${daySession.minorRevision.start_verse.order_in_surah}</td>
                        <td class="minor-revision-cell">${daySession.minorRevision.end_verse.surah_name}</td>
                        <td class="minor-revision-cell">${daySession.minorRevision.end_verse.order_in_surah}</td>
                    ` : '<td colspan="4" class="minor-revision-cell text-center">لا يوجد مراجعة صغرى للطالب</td>'}
                    ${daySession.majorRevision ? `
                        <td class="major-revision-cell">${daySession.majorRevision.start_verse.surah_name}</td>
                        <td class="major-revision-cell">${daySession.majorRevision.start_verse.order_in_surah}</td>
                        <td class="major-revision-cell">${daySession.majorRevision.end_verse.surah_name}</td>
                        <td class="major-revision-cell">${daySession.majorRevision.end_verse.order_in_surah}</td>
                    ` : '<td colspan="4" class="major-revision-cell text-center">لا يوجد مراجعة كبرى للطالب</td>'}
                </tr>`;
            });
        }
        
        this.weekPlanBody.innerHTML = html;
    }
    
    formatDate(date) {
        return `${date.getDate()} ${this.arabicMonths[date.getMonth()]} ${date.getFullYear()}`;
    }

    calculateSessionTotals() {
        const totals = {
            memorization: 0,
            minorRevision: 0,
            majorRevision: 0
        };

        Object.values(this.sessions || {}).forEach(daySession => {
            if (daySession.memorization) {
                totals.memorization += daySession.memorization.pages_count || 0;
            }
            if (daySession.minorRevision) {
                totals.minorRevision += daySession.minorRevision.pages_count || 0;
            }
            if (daySession.majorRevision) {
                totals.majorRevision += daySession.majorRevision.pages_count || 0;
            }
        });

        Object.keys(totals).forEach(key => {
            totals[key] = Number(totals[key].toFixed(1));
            if (totals[key] % 1 === 0) {
                totals[key] = Math.floor(totals[key]);
            }
        });

        return totals;
    }

    updateProgressSummary() {
        const totals = this.calculateSessionTotals();
        this.memorizationSummary.textContent = `${totals.memorization} صفحة`;
        this.minorRevisionSummary.textContent = `${totals.minorRevision} صفحة`;
        this.majorRevisionSummary.textContent = `${totals.majorRevision} صفحة`;
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