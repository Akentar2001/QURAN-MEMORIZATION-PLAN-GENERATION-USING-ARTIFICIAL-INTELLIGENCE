const surahs = [
    { id: 1, name: "الفاتحة", verses: 7 },
    { id: 2, name: "البقرة", verses: 286 },
    { id: 3, name: "آل عمران", verses: 200 },
    { id: 4, name: "النساء", verses: 176 },
    { id: 5, name: "المائدة", verses: 120 },
    { id: 6, name: "الأنعام", verses: 165 },
    { id: 7, name: "الأعراف", verses: 206 },
    { id: 8, name: "الأنفال", verses: 75 },
    { id: 9, name: "التوبة", verses: 129 },
    { id: 10, name: "يونس", verses: 109 },
    { id: 11, name: "هود", verses: 123 },
    { id: 12, name: "يوسف", verses: 111 },
    { id: 13, name: "الرعد", verses: 43 },
    { id: 14, name: "إبراهيم", verses: 52 },
    { id: 15, name: "الحجر", verses: 99 },
    { id: 16, name: "النحل", verses: 128 },
    { id: 17, name: "الإسراء", verses: 111 },
    { id: 18, name: "الكهف", verses: 110 },
    { id: 19, name: "مريم", verses: 98 },
    { id: 20, name: "طه", verses: 135 },
    { id: 21, name: "الأنبياء", verses: 112 },
    { id: 22, name: "الحج", verses: 78 },
    { id: 23, name: "المؤمنون", verses: 118 },
    { id: 24, name: "النور", verses: 64 },
    { id: 25, name: "الفرقان", verses: 77 },
    { id: 26, name: "الشعراء", verses: 227 },
    { id: 27, name: "النمل", verses: 93 },
    { id: 28, name: "القصص", verses: 88 },
    { id: 29, name: "العنكبوت", verses: 69 },
    { id: 30, name: "الروم", verses: 60 },
    { id: 31, name: "لقمان", verses: 34 },
    { id: 32, name: "السجدة", verses: 30 },
    { id: 33, name: "الأحزاب", verses: 73 },
    { id: 34, name: "سبأ", verses: 54 },
    { id: 35, name: "فاطر", verses: 45 },
    { id: 36, name: "يس", verses: 83 },
    { id: 37, name: "الصافات", verses: 182 },
    { id: 38, name: "ص", verses: 88 },
    { id: 39, name: "الزمر", verses: 75 },
    { id: 40, name: "غافر", verses: 85 },
    { id: 41, name: "فصلت", verses: 54 },
    { id: 42, name: "الشورى", verses: 53 },
    { id: 43, name: "الزخرف", verses: 89 },
    { id: 44, name: "الدخان", verses: 59 },
    { id: 45, name: "الجاثية", verses: 37 },
    { id: 46, name: "الأحقاف", verses: 35 },
    { id: 47, name: "محمد", verses: 38 },
    { id: 48, name: "الفتح", verses: 29 },
    { id: 49, name: "الحجرات", verses: 18 },
    { id: 50, name: "ق", verses: 45 },
    { id: 51, name: "الذاريات", verses: 60 },
    { id: 52, name: "الطور", verses: 49 },
    { id: 53, name: "النجم", verses: 62 },
    { id: 54, name: "القمر", verses: 55 },
    { id: 55, name: "الرحمن", verses: 78 },
    { id: 56, name: "الواقعة", verses: 96 },
    { id: 57, name: "الحديد", verses: 29 },
    { id: 58, name: "المجادلة", verses: 22 },
    { id: 59, name: "الحشر", verses: 24 },
    { id: 60, name: "الممتحنة", verses: 13 },
    { id: 61, name: "الصف", verses: 14 },
    { id: 62, name: "الجمعة", verses: 11 },
    { id: 63, name: "المنافقون", verses: 11 },
    { id: 64, name: "التغابن", verses: 18 },
    { id: 65, name: "الطلاق", verses: 12 },
    { id: 66, name: "التحريم", verses: 12 },
    { id: 67, name: "الملك", verses: 30 },
    { id: 68, name: "القلم", verses: 52 },
    { id: 69, name: "الحاقة", verses: 52 },
    { id: 70, name: "المعارج", verses: 44 },
    { id: 71, name: "نوح", verses: 28 },
    { id: 72, name: "الجن", verses: 28 },
    { id: 73, name: "المزمل", verses: 20 },
    { id: 74, name: "المدثر", verses: 56 },
    { id: 75, name: "القيامة", verses: 40 },
    { id: 76, name: "الإنسان", verses: 31 },
    { id: 77, name: "المرسلات", verses: 50 },
    { id: 78, name: "النبأ", verses: 40 },
    { id: 79, name: "النازعات", verses: 46 },
    { id: 80, name: "عبس", verses: 42 },
    { id: 81, name: "التكوير", verses: 29 },
    { id: 82, name: "الانفطار", verses: 19 },
    { id: 83, name: "المطففين", verses: 36 },
    { id: 84, name: "الانشقاق", verses: 25 },
    { id: 85, name: "البروج", verses: 22 },
    { id: 86, name: "الطارق", verses: 17 },
    { id: 87, name: "الأعلى", verses: 19 },
    { id: 88, name: "الغاشية", verses: 26 },
    { id: 89, name: "الفجر", verses: 30 },
    { id: 90, name: "البلد", verses: 20 },
    { id: 91, name: "الشمس", verses: 15 },
    { id: 92, name: "الليل", verses: 21 },
    { id: 93, name: "الضحى", verses: 11 },
    { id: 94, name: "الشرح", verses: 8 },
    { id: 95, name: "التين", verses: 8 },
    { id: 96, name: "العلق", verses: 19 },
    { id: 97, name: "القدر", verses: 5 },
    { id: 98, name: "البينة", verses: 8 },
    { id: 99, name: "الزلزلة", verses: 8 },
    { id: 100, name: "العاديات", verses: 11 },
    { id: 101, name: "القارعة", verses: 11 },
    { id: 102, name: "التكاثر", verses: 8 },
    { id: 103, name: "العصر", verses: 3 },
    { id: 104, name: "الهمزة", verses: 9 },
    { id: 105, name: "الفيل", verses: 5 },
    { id: 106, name: "قريش", verses: 4 },
    { id: 107, name: "الماعون", verses: 7 },
    { id: 108, name: "الكوثر", verses: 3 },
    { id: 109, name: "الكافرون", verses: 6 },
    { id: 110, name: "النصر", verses: 3 },
    { id: 111, name: "المسد", verses: 5 },
    { id: 112, name: "الإخلاص", verses: 4 },
    { id: 113, name: "الفلق", verses: 5 },
    { id: 114, name: "الناس", verses: 6 }
];


function createStudentCard(student) {
    const cardId = `card-${student.id}`;
    const sectionOrder = ['memorization', 'minor_review', 'major_review'];

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
                        <i class="fas fa-chevron-down toggle-icon"></i>
                    </div>
                </div>
                <div class="save-button-container ${student.attendance_status === 'absent' ? 'show' : ''}" style="display: ${student.attendance_status === 'absent' ? 'block' : 'none'}">
                    <div class="py-2 px-3">
                        <button class="btn btn-primary btn-sm w-100" 
                                id="save-absent-${cardId}" 
                                onclick="saveEvaluation(${student.id})">
                            حفظ
                        </button>
                    </div>
                </div>
                <div class="sections-container" style="display: none">
                    ${sectionOrder
                        .map(sectionKey => createSection(sectionKey, student.sections[sectionKey], student.id))
                        .filter(section => section !== '')
                        .join('')}
                    <div class="card-footer bg-transparent border-0 py-2">
                        <button class="btn btn-primary btn-sm w-100" 
                                id="save-present-${cardId}" 
                                onclick="saveEvaluation(${student.id})"
                                ${student.attendance_status === 'present' ? 'disabled' : ''}>
                            حفظ التقييم
                        </button>
                    </div>
                </div>
            </div>
        </div>`;
}

function toggleAttendance(studentId) {
    const checkbox = document.getElementById(`attendance-${studentId}`);
    const card = document.getElementById(`card-${studentId}`);
    const sectionsContainer = card.querySelector('.sections-container');
    const saveButtonContainer = card.querySelector('.save-button-container');
    const student = students.find(s => s.id === parseInt(studentId));

    student.attendance_status = checkbox.checked ? 'present' : 'absent';
    
    sectionsContainer.style.display = 'none';
    
    saveButtonContainer.style.display = checkbox.checked ? 'none' : 'block';
    
    if (!checkbox.checked) {
        Object.values(student.sections).forEach(section => {
            section.grade = null;
        });
    } else {
        checkEvaluations(`card-${studentId}`);
    }
}

function toggleCard(cardId) {
    const card = document.getElementById(cardId);
    const sectionsContainer = card.querySelector('.sections-container');
    const toggleIcon = card.querySelector('.toggle-icon');
    const isAbsent = !card.querySelector('.form-check-input').checked;
    
    if (isAbsent) return;
    
    if (sectionsContainer.style.display === 'none') {
        sectionsContainer.style.display = 'block';
        toggleIcon.classList.remove('fa-chevron-down');
        toggleIcon.classList.add('fa-chevron-up');
    } else {
        sectionsContainer.style.display = 'none';
        toggleIcon.classList.remove('fa-chevron-up');
        toggleIcon.classList.add('fa-chevron-down');
    }
}

function createSection(title, data, studentId) {
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
                        <select class="surah-select from-surah-select" onchange="updateVerseOptions(this, 'from', '${studentId}', '${title}')">
                            ${surahs.map(s => `<option value="${s.name}" ${s.name === data.fromS ? 'selected' : ''}>${s.name}</option>`).join('')}
                        </select>
                        <select class="verse-input from-verse-input" onchange="checkEvaluations('card-${studentId}')">
                            ${generateVerseOptions(data.fromS, data.fromV)}
                        </select>
                    </div>
                </div>
                
                <div class="surah-group">
                    <span class="control-label">إلى</span>
                    <div class="surah-control">
                        <select class="surah-select to-surah-select" onchange="updateVerseOptions(this, 'to', '${studentId}', '${title}')">
                            ${surahs.map(s => `<option value="${s.name}" ${s.name === data.toS ? 'selected' : ''}>${s.name}</option>`).join('')}
                        </select>
                        <select class="verse-input to-verse-input" onchange="checkEvaluations('card-${studentId}')">
                             ${generateVerseOptions(data.toS, data.toV)}
                        </select>
                    </div>
                </div>
            </div>
            
            <div class="evaluation-footer d-flex justify-content-end align-items-center">
                <select class="form-select form-select-sm evaluation-select" onchange="checkEvaluations('card-${studentId}')" style="width: 120px">
                    <option value="" ${!data.grade ? 'selected' : ''} disabled>اختر التقييم</option>
                    <option value="5" ${data.grade === 5 ? 'selected' : ''}>ممتاز</option>
                    <option value="4" ${data.grade === 4 ? 'selected' : ''}>جيد جدا</option>
                    <option value="3" ${data.grade === 3 ? 'selected' : ''}>جيد</option>
                    <option value="2" ${data.grade === 2 ? 'selected' : ''}>مقبول</option>
                    <option value="0" ${data.grade === 0 ? 'selected' : ''}>غير حافظ</option>
                </select>
            </div>
        </div>`;
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
        const sectionElement = card.querySelector(`.${sectionType}`);
        const gradeSelect = sectionElement.querySelector('.evaluation-select');
        const fromSurahSelect = sectionElement.querySelector('.from-surah-select').value;
        const toSurahSelect = sectionElement.querySelector('.to-surah-select').value;
        const fromVerseSelect = parseInt(sectionElement.querySelector('.from-verse-input').value);
        const toVerseSelect = parseInt(sectionElement.querySelector('.to-verse-input').value);
        const selectedGrade = parseInt(gradeSelect.value);

        evaluationData.sections[sectionType] = {
            session_id: data.session_id,
            grade: isPresent ? selectedGrade : null,
            is_accepted: isPresent ? (selectedGrade > 0) : false,
            fromSurah: isPresent && selectedGrade > 0 && (fromSurahSelect !== data.fromS || fromVerseSelect !== data.fromV)? surahs.find(s => s.name === fromSurahSelect).id : null,
            fromVerse: isPresent && selectedGrade > 0 && (fromSurahSelect !== data.fromS || fromVerseSelect !== data.fromV)? fromVerseSelect : null,
            toSurah: isPresent && selectedGrade > 0 && (toSurahSelect !== data.toS || toVerseSelect !== data.toV)? surahs.find(s => s.name === toSurahSelect).id : null,
            toVerse: isPresent && selectedGrade > 0 && (toSurahSelect !== data.toS || toVerseSelect !== data.toV)? toVerseSelect : null
        };
    });

    fetch(`http://localhost:5000/api/recitation_session/updateSessions/student/${studentId}`, {
        method: 'PUT',
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

    if (searchTerm) {
        filteredStudents = filteredStudents.filter(student =>
            student.name.toLowerCase().includes(searchTerm)
        );
    }

    if (evaluationStatus !== 'all') {
        filteredStudents = filteredStudents.filter(student => {
            const hasEvaluation = Object.values(student.sections).some(section => section.grade !== null);
            return evaluationStatus === 'evaluated' ? hasEvaluation : !hasEvaluation;
        });
    }

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
    const saveButtonPresent = document.getElementById(`save-present-${cardId}`);
    const isAbsent = !card.querySelector('.form-check-input').checked;

    if (isAbsent) {
        return;
    }

    const allSelected = Array.from(selects).every(select => select.value !== '');
    if (saveButtonPresent) {
        saveButtonPresent.disabled = !allSelected;
    }
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

let students = [];

async function fetchStudents() {
    try {
        const response = await fetch('http://localhost:5000/api/recitation_session/getAllSessionsStudents');
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

document.addEventListener('DOMContentLoaded', () => {
    fetchStudents();

    document.getElementById('searchInput').addEventListener('input', filterStudents);
    document.getElementById('sortOrder').addEventListener('change', filterStudents);
    document.getElementById('evaluationFilter').addEventListener('change', filterStudents);
});
