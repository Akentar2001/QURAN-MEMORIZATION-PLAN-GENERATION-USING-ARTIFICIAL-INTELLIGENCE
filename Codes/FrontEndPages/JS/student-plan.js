// Student Plan Manager Class
class StudentPlanManager {
    constructor() {
        this.initializeData();
        this.bindElements();
        this.bindEvents();
        this.initializeChart();
    }

    initializeData() {
        this.arabicMonths = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"];
        this.arabicDays = ["الأحد", "الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت"];

        // Sample data for two weeks and month plans
        this.twoWeeksPlanData = this.generatePlanData(14);
        this.monthPlanData = this.generatePlanData(30);
    }

    bindElements() {
        this.periodButtons = document.querySelectorAll('.time-period-selector .btn');
        this.planPeriods = document.querySelectorAll('.plan-period');
        this.printButton = document.getElementById('printPlan');
        this.twoWeeksPlan = document.getElementById('twoWeeksPlan');
        this.monthPlan = document.getElementById('monthPlan');
    }

    bindEvents() {
        // Time period selector functionality
        this.periodButtons.forEach(button => {
            button.addEventListener('click', this.handlePeriodChange.bind(this));
        });

        // Print functionality
        this.printButton.addEventListener('click', () => window.print());
    }

    handlePeriodChange(event) {
        // Remove active class from all buttons
        this.periodButtons.forEach(btn => btn.classList.remove('active'));

        // Add active class to clicked button
        event.currentTarget.classList.add('active');

        // Hide all plan periods
        this.planPeriods.forEach(period => period.style.display = 'none');

        // Show selected plan period
        const selectedPeriod = event.currentTarget.getAttribute('data-period');
        document.getElementById(`${selectedPeriod}Plan`).style.display = 'block';

        // Load data for the selected period if not already loaded
        if (selectedPeriod === 'twoWeeks' && !this.twoWeeksPlanLoaded) {
            this.renderPlanPeriod(this.twoWeeksPlanData, this.twoWeeksPlan);
            this.twoWeeksPlanLoaded = true;
        } else if (selectedPeriod === 'month' && !this.monthPlanLoaded) {
            this.renderPlanPeriod(this.monthPlanData, this.monthPlan);
            this.monthPlanLoaded = true;
        }

        // Update progress summary based on selected period
        this.updateProgressSummary(selectedPeriod);
    }

    updateProgressSummary(period) {
        let memorization, majorRevision, minorRevision;

        switch (period) {
            case 'week':
                memorization = '10 صفحات';
                majorRevision = '5 أجزاء';
                minorRevision = '30 صفحة';
                break;
            case 'twoWeeks':
                memorization = '20 صفحة';
                majorRevision = '10 أجزاء';
                minorRevision = '60 صفحة';
                break;
            case 'month':
                memorization = '40 صفحة';
                majorRevision = '20 جزء';
                minorRevision = '120 صفحة';
                break;
        }

        document.querySelector('.info-box.bg-success .info-box-number').textContent = memorization;
        document.querySelector('.info-box.bg-primary .info-box-number').textContent = majorRevision;
        document.querySelector('.info-box.bg-warning .info-box-number').textContent = minorRevision;
    }

    generatePlanData(days) {
        const planData = [];
        const startDate = new Date();

        for (let i = 0; i < days; i++) {
            const currentDate = new Date(startDate);
            currentDate.setDate(startDate.getDate() + i);

            const dayName = this.arabicDays[currentDate.getDay()];
            const dayNumber = i + 1;
            const dateString = `${currentDate.getDate()} ${this.arabicMonths[currentDate.getMonth()]} ${currentDate.getFullYear()}`;

            // Generate memorization content based on day
            const memorizationContent = {
                title: `سورة البقرة (آية ${i * 10 + 1}-${i * 10 + 10})`,
                amount: 'صفحتان'
            };

            // Generate major revision content
            const majorRevisionContent = {
                title: `جزء ${i % 30 + 1}`,
                amount: '1 جزء'
            };

            // Generate minor revision content
            const minorRevisionContent = {
                title: `الصفحات ${i * 5 + 1}-${i * 5 + 6} من سورة البقرة`,
                amount: '6 صفحات'
            };

            planData.push({
                dayNumber,
                dayName,
                dateString,
                memorization: memorizationContent,
                majorRevision: majorRevisionContent,
                minorRevision: minorRevisionContent
            });
        }

        return planData;
    }

    renderPlanPeriod(data, container) {
        // Clear existing content
        container.innerHTML = '';

        // Generate day rows
        data.forEach(day => {
            const dayRow = this.createDayRow(day);
            container.appendChild(dayRow);
        });
    }

    createDayRow(day) {
        const dayRow = document.createElement('div');
        dayRow.className = 'row day-row';

        // Create day header
        const dayHeader = `
            <div class="col-12">
                <div class="day-header">
                    <div class="d-flex align-items-center">
                        <div class="day-icon">
                            <i class="fas fa-calendar-day"></i>
                        </div>
                        <h5 class="mb-0">اليوم ${this.getArabicNumber(day.dayNumber)} - ${day.dayName}</h5>
                    </div>
                    <span class="badge bg-light text-dark">${day.dateString}</span>
                </div>
            </div>
        `;

        // Create memorization column
        const memorizationColumn = `
            <div class="col-md-4 mb-3 mb-md-0">
                <div class="section-column memorization-col">
                    <div class="section-header">
                        <i class="fas fa-book"></i> الحفظ الجديد
                    </div>
                    <div class="section-content">
                        <p>${day.memorization.title}</p>
                        <small class="text-muted">المقدار: ${day.memorization.amount}</small>
                    </div>
                </div>
            </div>
        `;

        // Create major revision column
        const majorRevisionColumn = `
            <div class="col-md-4 mb-3 mb-md-0">
                <div class="section-column revision-col">
                    <div class="section-header">
                        <i class="fas fa-sync"></i> المراجعة الكبرى
                    </div>
                    <div class="section-content">
                        <p>${day.majorRevision.title}</p>
                        <small class="text-muted">المقدار: ${day.majorRevision.amount}</small>
                    </div>
                </div>
            </div>
        `;

        // Create minor revision column
        const minorRevisionColumn = `
            <div class="col-md-4">
                <div class="section-column minor-revision-col">
                    <div class="section-header">
                        <i class="fas fa-redo"></i> المراجعة الصغرى
                    </div>
                    <div class="section-content">
                        <p>${day.minorRevision.title}</p>
                        <small class="text-muted">المقدار: ${day.minorRevision.amount}</small>
                    </div>
                </div>
            </div>
        `;

        // Combine all columns
        dayRow.innerHTML = dayHeader + memorizationColumn + majorRevisionColumn + minorRevisionColumn;

        return dayRow;
    }

    getArabicNumber(number) {
        const arabicNumbers = ['الأول', 'الثاني', 'الثالث', 'الرابع', 'الخامس', 'السادس', 'السابع', 'الثامن', 'التاسع', 'العاشر'];
        if (number <= 10) {
            return arabicNumbers[number - 1];
        }
        return number.toString();
    }

    initializeChart() {
        const ctx = document.getElementById('progressChart').getContext('2d');
        this.progressChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو'],
                datasets: [{
                    label: 'الحفظ الجديد',
                    data: [10, 15, 12, 18, 20, 25],
                    borderColor: '#28a745',
                    tension: 0.4,
                    fill: false
                }, {
                    label: 'المراجعة الكبرى',
                    data: [5, 8, 6, 10, 12, 15],
                    borderColor: '#4a90e2',
                    tension: 0.4,
                    fill: false
                }, {
                    label: 'المراجعة الصغرى',
                    data: [30, 35, 32, 38, 40, 45],
                    borderColor: '#ffc107',
                    tension: 0.4,
                    fill: false
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            font: {
                                family: 'Tajawal'
                            }
                        }
                    },
                    title: {
                        display: true,
                        text: 'تقدم الحفظ والمراجعة',
                        font: {
                            family: 'Tajawal',
                            size: 16
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            font: {
                                family: 'Tajawal'
                            }
                        }
                    },
                    x: {
                        ticks: {
                            font: {
                                family: 'Tajawal'
                            }
                        }
                    }
                }
            }
        });
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new StudentPlanManager();
});

// Time period selector functionality
document.addEventListener('DOMContentLoaded', function () {
    // Handle time period selection
    const periodButtons = document.querySelectorAll('.time-period-selector .btn');
    periodButtons.forEach(button => {
        button.addEventListener('click', function () {
            // Remove active class from all buttons
            periodButtons.forEach(btn => btn.classList.remove('active'));
            // Add active class to clicked button
            this.classList.add('active');

            // Hide all plan periods
            document.querySelectorAll('.plan-period').forEach(plan => {
                plan.style.display = 'none';
            });

            // Show selected plan period
            const period = this.getAttribute('data-period');
            document.getElementById(`${period}Plan`).style.display = 'block';
        });
    });

    // Print functionality
    document.getElementById('printPlan').addEventListener('click', function () {
        window.print();
    });

    // Initialize chart
    initializeChart();

    // Edit plan functionality
    setupEditMode();
});

// Initialize progress chart
function initializeChart() {
    const ctx = document.getElementById('progressChart').getContext('2d');
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['1 مارس', '5 مارس', '10 مارس', '15 مارس', '20 مارس', '25 مارس', '30 مارس'],
            datasets: [
                {
                    label: 'الحفظ الجديد',
                    data: [0, 10, 20, 30, 40, 50, 60],
                    borderColor: '#28a745',
                    backgroundColor: 'rgba(40, 167, 69, 0.1)',
                    tension: 0.4
                },
                {
                    label: 'المراجعة الكبرى',
                    data: [0, 5, 10, 15, 20, 25, 30],
                    borderColor: '#007bff',
                    backgroundColor: 'rgba(0, 123, 255, 0.1)',
                    tension: 0.4
                },
                {
                    label: 'المراجعة الصغرى',
                    data: [0, 6, 12, 18, 24, 30, 36],
                    borderColor: '#ffc107',
                    backgroundColor: 'rgba(255, 193, 7, 0.1)',
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        font: {
                            family: 'Tajawal'
                        }
                    }
                },
                tooltip: {
                    bodyFont: {
                        family: 'Tajawal'
                    },
                    titleFont: {
                        family: 'Tajawal'
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'الصفحات',
                        font: {
                            family: 'Tajawal',
                            size: 14
                        }
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'التاريخ',
                        font: {
                            family: 'Tajawal',
                            size: 14
                        }
                    }
                }
            }
        }
    });
}

// Setup edit mode functionality
function setupEditMode() {
    const editButton = document.querySelector('.btn-primary[href="#"]');

    editButton.addEventListener('click', function (e) {
        e.preventDefault();
        toggleEditMode();
    });
}

// Toggle between view and edit modes
function toggleEditMode() {
    const isEditMode = document.body.classList.toggle('edit-mode');
    const editButton = document.querySelector('.btn-primary[href="#"]');

    if (isEditMode) {
        // Change to save button
        editButton.innerHTML = '<i class="fas fa-save ms-1"></i> حفظ التغييرات';
        editButton.classList.remove('btn-primary');
        editButton.classList.add('btn-success');

        // Make content editable
        makeContentEditable(true);

        // Add cancel button
        const cancelButton = document.createElement('button');
        cancelButton.className = 'btn btn-danger no-print';
        cancelButton.innerHTML = '<i class="fas fa-times ms-1"></i> إلغاء';
        cancelButton.id = 'cancelEdit';
        cancelButton.addEventListener('click', function () {
            // Reload the page to discard changes
            location.reload();
        });

        editButton.parentNode.insertBefore(cancelButton, editButton);
    } else {
        // Change back to edit button
        editButton.innerHTML = '<i class="fas fa-edit ms-1"></i> تعديل الخطة';
        editButton.classList.remove('btn-success');
        editButton.classList.add('btn-primary');

        // Make content non-editable
        makeContentEditable(false);

        // Remove cancel button
        const cancelButton = document.getElementById('cancelEdit');
        if (cancelButton) {
            cancelButton.remove();
        }

        // Save changes (in a real app, this would send data to the server)
        savePlanChanges();
    }
}

// Make plan content editable or non-editable
function makeContentEditable(editable) {
    // Make section content editable
    const sectionContents = document.querySelectorAll('.section-content p, .section-content small');
    sectionContents.forEach(element => {
        element.contentEditable = editable;
        if (editable) {
            element.classList.add('editable');
        } else {
            element.classList.remove('editable');
        }
    });
}

// Save plan changes
function savePlanChanges() {
    // In a real application, this function would collect all the edited content
    // and send it to the server via an API call

    // For demonstration, just show a success message
    const notification = document.createElement('div');
    notification.className = 'alert alert-success position-fixed';
    notification.style.bottom = '20px';
    notification.style.right = '20px';
    notification.style.zIndex = '1050';
    notification.innerHTML = '<i class="fas fa-check-circle ms-2"></i>تم حفظ التغييرات بنجاح';

    document.body.appendChild(notification);

    // Remove notification after 3 seconds
    setTimeout(() => {
        notification.remove();
    }, 3000);
}