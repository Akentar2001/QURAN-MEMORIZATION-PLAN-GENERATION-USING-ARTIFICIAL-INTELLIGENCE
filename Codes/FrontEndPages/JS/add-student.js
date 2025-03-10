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
   
const weekDays = [
    { name: "الأحد", default: true },
    { name: "الاثنين", default: true },
    { name: "الثلاثاء", default: true },
    { name: "الأربعاء", default: true },
    { name: "الخميس", default: true },
    { name: "الجمعة", default: false },
    { name: "السبت", default: false }
    ];

    const memorizationDirections = [
    { id: 'baqara-nas', name: 'من سورة البقرة إلى الناس', default: false },
    { id: 'nas-baqara', name: 'من سورة الناس إلى البقرة', default: true }
    ];
    
const revisionDirections = [
    { id: 'baqara-nas', name: 'من سورة البقرة إلى الناس', default: true },
    { id: 'nas-baqara', name: 'من سورة الناس إلى البقرة', default: false }
    ];
    
const newMemorizationOptions = [
    "ثمن صفحة (حوالي سطران)",
    "سدس صفحة (سطران ونصف)",
    "خمس صفحة (ثلاثة أسطر)",
    "ربع صفحة (أربعة أسطر)",
    "ثلث صفحة (خمسة أسطر)",
    "نصف صفحة (سبعة أسطر)",
    "ثلثي صفحة (عشرة أسطر)",
    "صفحة",
    "صفحة وربع",
    "صفحة ونصف",
    "صفحة وثلثي صفحة",
    "صفحتان",
    "صفحتان ونصف",
    "ثلاث صفحات",
    "ثلاث صفحات ونصف",
    "أربع صفحات",
    "أربع صفحات ونصف",
    "خمس صفحات",
    "ست صفحات",
    "سبع صفحات",
    "ثمان صفحات",
    "تسع صفحات",
    "عشر صفحات"
    ];
    
const smallRevisionOptions = [
    "نصف صفحة",
    "صفحة",
    "صفحة ونصف",
    "صفحتان",
    "صفحتان ونصف",
    "ثلاث صفحات",
    "ثلاث صفحات ونصف",
    "أربع صفحات",
    "أربع صفحات ونصف",
    "خمس صفحات",
    "ست صفحات",
    "سبع صفحات",
    "ثمان صفحات",
    "تسع صفحات",
    "عشر صفحات",
    "١٥ صفحة",
    "٢٠ صفحة",
    "٢٥ صفحة",
    "٣٠ صفحة"
    ];
    
const largeRevisionOptions = [
    "صفحة",
    "صفحتان",
    "ثلاث صفحات",
    "أربع صفحات",
    "خمس صفحات",
    "ست صفحات",
    "سبع صفحات",
    "ثمان صفحات",
    "تسع صفحات",
    "نصف جزء (عشر صفحات)",
    "١١ صفحة",
    "١٢ صفحة",
    "١٣ صفحة",
    "١٤ صفحة",
    "١٥ صفحة",
    "١٦ صفحة",
    "١٧ صفحة",
    "١٨ صفحة",
    "١٩ صفحة",
    "جزء (٢٠ صفحة)",
    "٢٥ صفحة",
    "جزء ونصف (٣٠ صفحة)",
    "٣٥ صفحة",
    "جزءان (٤٠ صفحة)",
    "جزءان ونصف (٥٠ صفحة)",
    "ثلاثة أجزاء (٦٠ صفحة)",
    "أربعة أجزاء (٨٠ صفحة)",
    "خمسة أجزاء (١٠٠ صفحة)",
    "ستة أجزاء (١٢٠ صفحة)",
    "سبعة أجزاء (١٤٠ صفحة)",
    "ثمانية أجزاء (١٦٠ صفحة)",
    "تسعة أجزاء (١٨٠ صفحة)",
    "عشرة أجزاء (٢٠٠ صفحة)"
    ];

// Populate Surah dropdowns
function populateSurahs() {
    const fromSurahSelect = document.getElementById('fromSurah');
    const toSurahSelect = document.getElementById('toSurah');

    surahs.forEach(surah => {
        const option = document.createElement('option');
        option.value = surah.name;
        option.textContent = surah.name;
        fromSurahSelect.appendChild(option.cloneNode(true));
        toSurahSelect.appendChild(option.cloneNode(true));
    });
}

function setupMemorizationToggle() {
    document.querySelectorAll('input[name="hasMemorization"]').forEach(radio => {
        radio.addEventListener('change', function () {
            const memorizationDetailsContainer = document.getElementById('memorizationDetailsContainer');
            if (this.value === 'yes') {
                memorizationDetailsContainer.classList.remove('d-none');
            } else {
                memorizationDetailsContainer.classList.add('d-none');
            }
        });
    });
}

function setupDaySelection() {
    const daysContainer = document.querySelector('.d-flex.flex-wrap.gap-1');
    daysContainer.innerHTML = ''; // Clear existing buttons

    weekDays.forEach(day => {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = `btn btn-sm ${day.default ? 'btn-primary selected-day' : 'btn-outline-secondary'} day-btn`;
    button.setAttribute('data-day', day.name);
    button.textContent = day.name;

    button.addEventListener('click', function() {
        this.classList.toggle('selected-day');
        this.classList.toggle('btn-outline-secondary');
        this.classList.toggle('btn-primary');
        updateSelectedDays();
    });

    daysContainer.appendChild(button);
    });
    updateSelectedDays();
}

// Add this helper function
function updateSelectedDays() {
    const selectedDays = Array.from(document.querySelectorAll('.day-btn.selected-day'))
    .map(btn => btn.dataset.day);
    document.getElementById('selectedDays').value = selectedDays.join(',');
}


// Add this new function
function setupMemorizationAmounts() {
    const newMemSelect = document.getElementById('newMemorizationAmount');
    const smallRevSelect = document.getElementById('smallRevisionAmount');
    const largeRevSelect = document.getElementById('largeRevisionAmount');

    // Clear and populate new memorization select
    newMemSelect.innerHTML = '<option value="" selected disabled>اختر كمية الحفظ</option>';
    newMemorizationOptions.forEach(option => {
    const el = document.createElement('option');
    el.value = option;
    el.textContent = option;
    newMemSelect.appendChild(el);
    });

    // Clear and populate small revision select
    smallRevSelect.innerHTML = '<option value="" selected disabled>اختر كمية المراجعة</option>';
    smallRevisionOptions.forEach(option => {
    const el = document.createElement('option');
    el.value = option;
    el.textContent = option;
    smallRevSelect.appendChild(el);
    });

    // Clear and populate large revision select
    largeRevSelect.innerHTML = '<option value="" selected disabled>اختر كمية المراجعة</option>';
    largeRevisionOptions.forEach(option => {
    const el = document.createElement('option');
    el.value = option;
    el.textContent = option;
    largeRevSelect.appendChild(el);
});
}

// Replace the populateSurahs function with this new function
function setupDirectionSelectors() {
    const memDirectionSelect = document.querySelector('#memorizationDetailsContainer select');
    const revDirectionSelect = document.querySelector('#RevDetailsContainer select');

    // Clear existing options
    memDirectionSelect.innerHTML = '';
    revDirectionSelect.innerHTML = '';

    // Add memorization directions
    memorizationDirections.forEach(direction => {
    const option = document.createElement('option');
    option.value = direction.id;
    option.textContent = direction.name;
    if (direction.default) option.selected = true;
    memDirectionSelect.appendChild(option);
    });

    // Add revision directions
    revisionDirections.forEach(direction => {
    const option = document.createElement('option');
    option.value = direction.id;
    option.textContent = direction.name;
    if (direction.default) option.selected = true;
    revDirectionSelect.appendChild(option);
});
}

function setupSurahSelection() {
    const toSurahSelect = document.getElementById('toSurah');
    const toVerseSelect = document.getElementById('toVerse');

    toSurahSelect.innerHTML = '<option value="" selected disabled>اختر السورة</option>';

    surahs.forEach(surah => {
    const option = document.createElement('option');
    option.value = surah.name;
    option.textContent = surah.name;
    toSurahSelect.appendChild(option);
    });

    toSurahSelect.addEventListener('change', function() {
    const selectedSurah = surahs.find(s => s.name === this.value);
    if (selectedSurah) {
        const verseSelect = document.createElement('select');
        verseSelect.className = 'form-select';
        verseSelect.id = 'toVerse';
        
        verseSelect.innerHTML = '<option value="" selected disabled>اختر الآية</option>';
        for (let i = 1; i <= selectedSurah.verses; i++) {
            const option = document.createElement('option');
            option.value = i;
            option.textContent = `الآية ${i}`;
            verseSelect.appendChild(option);
        }

        const oldVerseInput = document.getElementById('toVerse');
        oldVerseInput.parentNode.replaceChild(verseSelect, oldVerseInput);
    }
    });
}

function setupFormSubmission() {
    document.getElementById('addStudentForm').addEventListener('submit', function (event) {
    event.preventDefault();

    const formData = {
        personalInfo: {
            name: document.getElementById('studentName').value,
            age: document.getElementById('studentAge').value,
            gender: document.getElementById('studentGender').value,
            nationality: document.getElementById('nationality').value,
            parentPhone: document.getElementById('parentPhone').value,
            attendanceDays: document.getElementById('selectedDays').value
        },
        memorization: {
            memorizationDirection: document.getElementById('memDirection').value,
            revisionDirection: document.getElementById('revDirection').value,
            toSurah: document.getElementById('toSurah').value,
            toVerse: document.getElementById('toVerse').value
        },
        memorizationPlan: {
            newMemorizationAmount: document.getElementById('newMemorizationAmount').value,
            smallRevisionAmount: document.getElementById('smallRevisionAmount').value,
            largeRevisionAmount: document.getElementById('largeRevisionAmount').value,
            notes: document.getElementById('notes').value
        }
    };

    const successToast = new bootstrap.Toast(document.getElementById('successToast'));
    successToast.show();

    console.log("Form submitted successfully", formData);
    });
}

document.addEventListener('DOMContentLoaded', function () {
    setupDirectionSelectors();
    setupSurahSelection();
    setupMemorizationToggle();
    setupDaySelection();
    setupMemorizationAmounts();
    setupFormSubmission();
});
