const surahs = [
    { name: "الفاتحة", verses: 7 },
    { name: "البقرة", verses: 286 },
    { name: "آل عمران", verses: 200 },
    { name: "النساء", verses: 176 },
    { name: "المائدة", verses: 120 },
    { name: "الأنعام", verses: 165 },
    { name: "الأعراف", verses: 206 },
    { name: "الأنفال", verses: 75 },
    { name: "التوبة", verses: 129 },
    { name: "يونس", verses: 109 },
    { name: "هود", verses: 123 },
    { name: "يوسف", verses: 111 },
    { name: "الرعد", verses: 43 },
    { name: "إبراهيم", verses: 52 },
    { name: "الحجر", verses: 99 },
    { name: "النحل", verses: 128 },
    { name: "الإسراء", verses: 111 },
    { name: "الكهف", verses: 110 },
    { name: "مريم", verses: 98 },
    { name: "طه", verses: 135 },
    { name: "الأنبياء", verses: 112 },
    { name: "الحج", verses: 78 },
    { name: "المؤمنون", verses: 118 },
    { name: "النور", verses: 64 },
    { name: "الفرقان", verses: 77 },
    { name: "الشعراء", verses: 227 },
    { name: "النمل", verses: 93 },
    { name: "القصص", verses: 88 },
    { name: "العنكبوت", verses: 69 },
    { name: "الروم", verses: 60 },
    { name: "لقمان", verses: 34 },
    { name: "السجدة", verses: 30 },
    { name: "الأحزاب", verses: 73 },
    { name: "سبأ", verses: 54 },
    { name: "فاطر", verses: 45 },
    { name: "يس", verses: 83 },
    { name: "الصافات", verses: 182 },
    { name: "ص", verses: 88 },
    { name: "الزمر", verses: 75 },
    { name: "غافر", verses: 85 },
    { name: "فصلت", verses: 54 },
    { name: "الشورى", verses: 53 },
    { name: "الزخرف", verses: 89 },
    { name: "الدخان", verses: 59 },
    { name: "الجاثية", verses: 37 },
    { name: "الأحقاف", verses: 35 },
    { name: "محمد", verses: 38 },
    { name: "الفتح", verses: 29 },
    { name: "الحجرات", verses: 18 },
    { name: "ق", verses: 45 },
    { name: "الذاريات", verses: 60 },
    { name: "الطور", verses: 49 },
    { name: "النجم", verses: 62 },
    { name: "القمر", verses: 55 },
    { name: "الرحمن", verses: 78 },
    { name: "الواقعة", verses: 96 },
    { name: "الحديد", verses: 29 },
    { name: "المجادلة", verses: 22 },
    { name: "الحشر", verses: 24 },
    { name: "الممتحنة", verses: 13 },
    { name: "الصف", verses: 14 },
    { name: "الجمعة", verses: 11 },
    { name: "المنافقون", verses: 11 },
    { name: "التغابن", verses: 18 },
    { name: "الطلاق", verses: 12 },
    { name: "التحريم", verses: 12 },
    { name: "الملك", verses: 30 },
    { name: "القلم", verses: 52 },
    { name: "الحاقة", verses: 52 },
    { name: "المعارج", verses: 44 },
    { name: "نوح", verses: 28 },
    { name: "الجن", verses: 28 },
    { name: "المزمل", verses: 20 },
    { name: "المدثر", verses: 56 },
    { name: "القيامة", verses: 40 },
    { name: "الإنسان", verses: 31 },
    { name: "المرسلات", verses: 50 },
    { name: "النبأ", verses: 40 },
    { name: "النازعات", verses: 46 },
    { name: "عبس", verses: 42 },
    { name: "التكوير", verses: 29 },
    { name: "الانفطار", verses: 19 },
    { name: "المطففين", verses: 36 },
    { name: "الانشقاق", verses: 25 },
    { name: "البروج", verses: 22 },
    { name: "الطارق", verses: 17 },
    { name: "الأعلى", verses: 19 },
    { name: "الغاشية", verses: 26 },
    { name: "الفجر", verses: 30 },
    { name: "البلد", verses: 20 },
    { name: "الشمس", verses: 15 },
    { name: "الليل", verses: 21 },
    { name: "الضحى", verses: 11 },
    { name: "الشرح", verses: 8 },
    { name: "التين", verses: 8 },
    { name: "العلق", verses: 19 },
    { name: "القدر", verses: 5 },
    { name: "البينة", verses: 8 },
    { name: "الزلزلة", verses: 8 },
    { name: "العاديات", verses: 11 },
    { name: "القارعة", verses: 11 },
    { name: "التكاثر", verses: 8 },
    { name: "العصر", verses: 3 },
    { name: "الهمزة", verses: 9 },
    { name: "الفيل", verses: 5 },
    { name: "قريش", verses: 4 },
    { name: "الماعون", verses: 7 },
    { name: "الكوثر", verses: 3 },
    { name: "الكافرون", verses: 6 },
    { name: "النصر", verses: 3 },
    { name: "المسد", verses: 5 },
    { name: "الإخلاص", verses: 4 },
    { name: "الفلق", verses: 5 },
    { name: "الناس", verses: 6 }
];


function createStudentCard(student) {
    const cardId = `card-${student.id}`;

    return `
        <div class="col-12 col-md-6 col-lg-4">
            <div class="card student-card mb-2" id="${cardId}">
                <div class="card-header bg-white d-flex justify-content-between align-items-center p-3" onclick="toggleCard('${cardId}')">
                    <h5 class="mb-0 text-primary">${student.name}</h5>
                    <div class="d-flex align-items-center gap-2">
                        <div class="form-check form-switch">
                            <input class="form-check-input" type="checkbox" 
                                   id="attendance-${student.id}" 
                                   ${student.attendance_status === 'present' ? 'checked' : ''}
                                   onchange="toggleAttendance('${student.id}')">
                            <label class="form-check-label" for="attendance-${student.id}">حاضر</label>
                        </div>
                        <i class="fas fa-chevron-up toggle-icon"></i>
                    </div>
                </div>
                <div class="card-body py-2 ${student.attendance_status === 'absent' ? 'disabled' : ''}">
                    ${Object.entries(student.sections).map(([key, value]) => createSection(key, value, student.id)).join('')}
                    <button class="btn btn-primary btn-sm w-100 mt-2" 
                            id="save-${cardId}" 
                            onclick="saveEvaluation(${student.id})" 
                            disabled>
                        حفظ التقييم
                    </button>
                </div>
            </div>
        </div>`;
}

function toggleAttendance(studentId) {
    const checkbox = document.getElementById(`attendance-${studentId}`);
    const cardBody = document.querySelector(`#card-${studentId} .card-body`);
    const student = students.find(s => s.id === parseInt(studentId));

    student.attendance_status = checkbox.checked ? 'present' : 'absent';
    cardBody.classList.toggle('disabled', !checkbox.checked);

    // Reset evaluations if marked as absent
    if (!checkbox.checked) {
        Object.values(student.sections).forEach(section => {
            section.grade = null;
        });
    }

    checkEvaluations(`card-${studentId}`);
}

function createSection(title, data, studentId) {
    // If section doesn't exist, don't render it
    if (!data) return '';

    const displayTitles = {
        'memorization': 'حفظ',
        'minor_review': 'مراجعة صغرى',
        'major_review': 'مراجعة كبرى'
    };
    const displayTitle = displayTitles[title];

    return `
        <div class="section-box ${title}">
            <h6 class="text-muted mb-2">${displayTitle}</h6>
            
            <div class="from-to-container">
                <div class="surah-group">
                    <span class="control-label">من</span>
                    <div class="surah-control">
                        <select class="surah-select" onchange="updateVerseOptions(this, 'from', '${studentId}', '${title}')">
                            ${surahs.map(s => `<option value="${s.name}" ${s.name === data.fromS ? 'selected' : ''}>${s.name}</option>`).join('')}
                        </select>
                        <select class="verse-input" onchange="checkEvaluations('card-${studentId}')">
                            ${generateVerseOptions(data.fromS, data.fromV)}
                        </select>
                    </div>
                </div>
                
                <div class="surah-group">
                    <span class="control-label">إلى</span>
                    <div class="surah-control">
                        <select class="surah-select" onchange="updateVerseOptions(this, 'to', '${studentId}', '${title}')">
                            ${surahs.map(s => `<option value="${s.name}" ${s.name === data.toS ? 'selected' : ''}>${s.name}</option>`).join('')}
                        </select>
                        <select class="verse-input" onchange="checkEvaluations('card-${studentId}')">
                             ${generateVerseOptions(data.toS, data.toV)}
                        </select>
                    </div>
                </div>
            </div>
            
            <div class="evaluation-footer d-flex justify-content-end align-items-center">
                <select class="form-select form-select-sm evaluation-select" onchange="checkEvaluations('card-${studentId}')" style="width: 120px">
                    <option value="" ${!data.grade ? 'selected' : ''} disabled>اختر التقييم</option>
                    <option ${data.grade === 'ممتاز' ? 'selected' : ''}>ممتاز</option>
                    <option ${data.grade === 'جيد جدا' ? 'selected' : ''}>جيد جدا</option>
                    <option ${data.grade === 'جيد' ? 'selected' : ''}>جيد</option>
                    <option ${data.grade === 'ضعيف' ? 'selected' : ''}>ضعيف</option>
                    <option ${data.grade === 'غير حافظ' ? 'selected' : ''}>غير حافظ</option>
                </select>
            </div>
        </div>`;
}

function toggleCard(cardId) {
    const card = document.getElementById(cardId);
    const cardBody = card.querySelector('.card-body');
    if (cardBody.style.display === 'block') {
        cardBody.style.display = 'none';
        card.classList.add('card-minimized');
    } else {
        cardBody.style.display = 'block';
        card.classList.remove('card-minimized');
    }
}

function saveEvaluation(studentId) {
    const card = document.getElementById(`card-${studentId}`);
    const student = students.find(s => s.id === studentId);
    const isPresent = document.getElementById(`attendance-${studentId}`).checked;

    const evaluationData = {
        student_id: studentId,
        attendance_status: isPresent ? 'present' : 'absent',
        sections: {}
    };

    Object.entries(student.sections).forEach(([sectionType, data]) => {
        // Get the grade from the evaluation select element
        const sectionElement = card.querySelector(`.${sectionType}`);
        const gradeSelect = sectionElement.querySelector('.evaluation-select');
        const selectedGrade = gradeSelect.value;

        evaluationData.sections[sectionType] = {
            session_id: data.session_id,
            grade: isPresent ? selectedGrade : null,
            is_accepted: isPresent ? (selectedGrade !== 'ضعيف' && selectedGrade !== 'غير حافظ') : false
        };
    });

    // Send evaluation to backend
    fetch('http://localhost:5000/api/students/evaluations', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(evaluationData)
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification(`تم حفظ تقييم الطالب ${student.name} بنجاح`);
                updateProgress();
            } else {
                showNotification('حدث خطأ أثناء حفظ التقييم', 'error');
            }
        })
        .catch(error => {
            console.error('Error saving evaluation:', error);
            showNotification('حدث خطأ أثناء حفظ التقييم', 'error');
        });
}

function showNotification(message) {
    const notification = document.getElementById('notification');
    const notificationText = document.getElementById('notificationText');
    notificationText.textContent = message;

    notification.style.display = 'block';
    notification.style.opacity = '1';

    setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => {
            notification.style.display = 'none';
        }, 300);
    }, 3000);
}

function filterStudents() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const sortOrder = document.getElementById('sortOrder').value;
    const evaluationStatus = document.getElementById('evaluationFilter').value;

    let filteredStudents = [...students];

    // Filter by search term
    if (searchTerm) {
        filteredStudents = filteredStudents.filter(student =>
            student.name.toLowerCase().includes(searchTerm)
        );
    }

    // Filter by evaluation status
    if (evaluationStatus !== 'all') {
        filteredStudents = filteredStudents.filter(student => {
            const hasEvaluation = Object.values(student.sections).some(section => section.grade !== null);
            return evaluationStatus === 'evaluated' ? hasEvaluation : !hasEvaluation;
        });
    }

    // Apply sorting
    filteredStudents = sortStudents(filteredStudents, sortOrder);

    renderStudents(filteredStudents);

    const visibleCount = document.querySelectorAll('#studentsContainer > div').length;
    document.getElementById('studentCount').textContent = visibleCount;
}

function sortStudents(studentsToSort, sortOrder) {
    switch (sortOrder) {
        case 'nameAscending':
            return studentsToSort.sort((a, b) => a.name.localeCompare(b.name, 'ar'));
        case 'nameDescending':
            return studentsToSort.sort((a, b) => b.name.localeCompare(a.name, 'ar'));
        default:
            return studentsToSort;
    }
}

function renderStudents(studentsToRender) {
    const container = document.getElementById('studentsContainer');
    container.innerHTML = '';

    studentsToRender.forEach(student => {
        container.innerHTML += createStudentCard(student);
    });
}

function generateVerseOptions(surahName, selectedVerse) {
    const surah = surahs.find(s => s.name === surahName);
    if (!surah) return '';

    let options = '';
    for (let i = 1; i <= surah.verses; i++) {
        options += `<option value="${i}" ${i === selectedVerse ? 'selected' : ''}>${i}</option>`;
    }
    return options;
}

function updateVerseOptions(surahSelect, type, studentId, sectionTitle) {
    const surahName = surahSelect.value;
    const verseSelect = surahSelect.parentElement.querySelector('.verse-input');
    const currentValue = verseSelect.value;

    verseSelect.innerHTML = generateVerseOptions(surahName, parseInt(currentValue) || 1);
    checkEvaluations(`card-${studentId}`);
}

function checkEvaluations(cardId) {
    const card = document.getElementById(cardId);
    const selects = card.querySelectorAll('.evaluation-select');
    const saveButton = document.getElementById(`save-${cardId}`);

    const allSelected = Array.from(selects).every(select => select.value !== '');
    saveButton.disabled = !allSelected;
}

function updateProgress() {
    const totalStudents = students.length;
    let completedStudents = 0;

    students.forEach(student => {
        const allSectionsEvaluated = Object.values(student.sections).every(section => section.grade);
        if (allSectionsEvaluated) {
            completedStudents++;
        }
    });

    const progressPercentage = (completedStudents / totalStudents) * 100;
    const progressBar = document.querySelector('.progress-bar');
    progressBar.style.width = `${progressPercentage}%`;
    progressBar.setAttribute('aria-valuenow', progressPercentage);
}

// Replace the static students array with:
let students = [];

// Update the fetchStudents function
async function fetchStudents() {
    try {
        const response = await fetch('http://localhost:5000/api/students/evaluations');
        if (!response.ok) {
            throw new Error('Failed to fetch students');
        }

        students = await response.json();
        renderStudents(students);
        document.getElementById('studentCount').textContent = students.length;
        updateProgress();
    } catch (error) {
        console.error('Error fetching students:', error);
        showNotification('فشل في تحميل بيانات الطلاب', 'error');
    }
}

// In the DOMContentLoaded event listener
document.addEventListener('DOMContentLoaded', () => {
    fetchStudents();

    // Add event listeners for search, sort and evaluation filter
    document.getElementById('searchInput').addEventListener('input', filterStudents);
    document.getElementById('sortOrder').addEventListener('change', filterStudents);
    document.getElementById('evaluationFilter').addEventListener('change', filterStudents);
});