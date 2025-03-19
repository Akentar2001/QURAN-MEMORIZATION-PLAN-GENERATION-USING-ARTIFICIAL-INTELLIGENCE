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

const weekDays = [
    { name: "الأحد", default: true, value: 1 },
    { name: "الاثنين", default: true, value: 2 },
    { name: "الثلاثاء", default: true, value: 4 },
    { name: "الأربعاء", default: true, value: 8 },
    { name: "الخميس", default: true, value: 16 },
    { name: "الجمعة", default: false, value: 32 },
    { name: "السبت", default: false, value: 64 }
];

const memorizationDirections = [
    { id: 'baqara-nas', name: 'من سورة البقرة إلى الناس', default: false, value: true },
    { id: 'nas-baqara', name: 'من سورة الناس إلى البقرة', default: true, value: false }
];

const revisionDirections = [
    { id: 'baqara-nas', name: 'من سورة البقرة إلى الناس', default: true, value: true },
    { id: 'nas-baqara', name: 'من سورة الناس إلى البقرة', default: false, value: false }
];

const newMemorizationOptions = [

    { id: 1, name: "ثمن صفحة (حوالي سطران)", amount: 0.125 },
    { id: 2, name: "سدس صفحة (سطران ونصف)", amount: 0.167 },
    { id: 3, name: "خمس صفحة (ثلاثة أسطر)", amount: 0.2 },
    { id: 4, name: "ربع صفحة (أربعة أسطر)", amount: 0.25 },
    { id: 5, name: "ثلث صفحة (خمسة أسطر)", amount: 0.333 },
    { id: 6, name: "نصف صفحة (سبعة أسطر)", amount: 0.5 },
    { id: 7, name: "ثلثي صفحة (عشرة أسطر)", amount: 0.667 },
    { id: 8, name: "صفحة", amount: 1.0 },
    { id: 9, name: "صفحة وربع", amount: 1.25 },
    { id: 10, name: "صفحة ونصف", amount: 1.5 },
    { id: 11, name: "صفحة وثلثي صفحة", amount: 1.667 },
    { id: 12, name: "صفحتان", amount: 2.0 },
    { id: 13, name: "صفحتان ونصف", amount: 2.5 },
    { id: 14, name: "ثلاث صفحات", amount: 3.0 },
    { id: 15, name: "ثلاث صفحات ونصف", amount: 3.5 },
    { id: 16, name: "أربع صفحات", amount: 4.0 },
    { id: 17, name: "أربع صفحات ونصف", amount: 4.5 },
    { id: 18, name: "خمس صفحات", amount: 5.0 },
    { id: 19, name: "ست صفحات", amount: 6.0 },
    { id: 20, name: "سبع صفحات", amount: 7.0 },
    { id: 21, name: "ثمان صفحات", amount: 8.0 },
    { id: 22, name: "تسع صفحات", amount: 9.0 },
    { id: 23, name: "عشر صفحات", amount: 10.0 }

];

const smallRevisionOptions = [

    { id: 1, name: "نصف صفحة", amount: 0.5 },
    { id: 2, name: "صفحة", amount: 1.0 },
    { id: 3, name: "صفحة ونصف", amount: 1.5 },
    { id: 4, name: "صفحتان", amount: 2.0 },
    { id: 5, name: "صفحتان ونصف", amount: 2.5 },
    { id: 6, name: "ثلاث صفحات", amount: 3.0 },
    { id: 7, name: "ثلاث صفحات ونصف", amount: 3.5 },
    { id: 8, name: "أربع صفحات", amount: 4.0 },
    { id: 9, name: "أربع صفحات ونصف", amount: 4.5 },
    { id: 10, name: "خمس صفحات", amount: 5.0 },
    { id: 11, name: "ست صفحات", amount: 6.0 },
    { id: 12, name: "سبع صفحات", amount: 7.0 },
    { id: 13, name: "ثمان صفحات", amount: 8.0 },
    { id: 14, name: "تسع صفحات", amount: 9.0 },
    { id: 15, name: "عشر صفحات", amount: 10.0 },
    { id: 16, name: "١٥ صفحة", amount: 15.0 },
    { id: 17, name: "٢٠ صفحة", amount: 20.0 },
    { id: 18, name: "٢٥ صفحة", amount: 25.0 },
    { id: 19, name: "٣٠ صفحة", amount: 30.0 }

];

const largeRevisionOptions = [
    { id: 1, name: "صفحة", amount: 1.0 },
    { id: 2, name: "صفحتان", amount: 2.0 },
    { id: 3, name: "ثلاث صفحات", amount: 3.0 },
    { id: 4, name: "أربع صفحات", amount: 4.0 },
    { id: 5, name: "خمس صفحات", amount: 5.0 },
    { id: 6, name: "ست صفحات", amount: 6.0 },
    { id: 7, name: "سبع صفحات", amount: 7.0 },
    { id: 8, name: "ثمان صفحات", amount: 8.0 },
    { id: 9, name: "تسع صفحات", amount: 9.0 },
    { id: 10, name: "نصف جزء (عشر صفحات)", amount: 10.0 },
    { id: 11, name: "١١ صفحة", amount: 11.0 },
    { id: 12, name: "١٢ صفحة", amount: 12.0 },
    { id: 13, name: "١٣ صفحة", amount: 13.0 },
    { id: 14, name: "١٤ صفحة", amount: 14.0 },
    { id: 15, name: "١٥ صفحة", amount: 15.0 },
    { id: 16, name: "١٦ صفحة", amount: 16.0 },
    { id: 17, name: "١٧ صفحة", amount: 17.0 },
    { id: 18, name: "١٨ صفحة", amount: 18.0 },
    { id: 19, name: "١٩ صفحة", amount: 19.0 },
    { id: 20, name: "جزء (٢٠ صفحة)", amount: 20.0 },
    { id: 21, name: "٢٥ صفحة", amount: 25.0 },
    { id: 22, name: "جزء ونصف (٣٠ صفحة)", amount: 30.0 },
    { id: 23, name: "٣٥ صفحة", amount: 35.0 },
    { id: 24, name: "جزءان (٤٠ صفحة)", amount: 40.0 },
    { id: 25, name: "جزءان ونصف (٥٠ صفحة)", amount: 50.0 },
    { id: 26, name: "ثلاثة أجزاء (٦٠ صفحة)", amount: 60.0 },
    { id: 27, name: "أربعة أجزاء (٨٠ صفحة)", amount: 80.0 },
    { id: 28, name: "خمسة أجزاء (١٠٠ صفحة)", amount: 100.0 },
    { id: 29, name: "ستة أجزاء (١٢٠ صفحة)", amount: 120.0 },
    { id: 30, name: "سبعة أجزاء (١٤٠ صفحة)", amount: 140.0 },
    { id: 31, name: "ثمانية أجزاء (١٦٠ صفحة)", amount: 160.0 },
    { id: 32, name: "تسعة أجزاء (١٨٠ صفحة)", amount: 180.0 },
    { id: 33, name: "عشرة أجزاء (٢٠٠ صفحة)", amount: 200.0 }
];

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

        button.addEventListener('click', function () {
            this.classList.toggle('selected-day');
            this.classList.toggle('btn-outline-secondary');
            this.classList.toggle('btn-primary');
            updateSelectedDays();
        });

        daysContainer.appendChild(button);
    });
    updateSelectedDays();
}

function updateSelectedDays() {
    const selectedDays = Array.from(document.querySelectorAll('.day-btn.selected-day'))
        .map(btn => btn.dataset.day);
    // Calculate sum of selected day values
    const selectedDayValues = selectedDays
        .map(dayName => weekDays.find(day => day.name === dayName)?.value || 0)
        .reduce((sum, value) => sum + value, 0);

    document.getElementById('selectedDays').value = selectedDayValues;
}

function setupMemorizationAmounts() {
    const newMemSelect = document.getElementById('newMemorizationAmount');
    const smallRevSelect = document.getElementById('smallRevisionAmount');
    const largeRevSelect = document.getElementById('largeRevisionAmount');

    newMemSelect.innerHTML = '<option value="" selected disabled>اختر كمية الحفظ</option>';
    newMemorizationOptions.forEach(option => {
        const el = document.createElement('option');
        el.value = option.amount;
        el.textContent = option.name;
        newMemSelect.appendChild(el);
    });

    smallRevSelect.innerHTML = '<option value="" selected disabled>اختر كمية المراجعة</option>';
    smallRevisionOptions.forEach(option => {
        const el = document.createElement('option');
        el.value = option.amount;
        el.textContent = option.name;
        smallRevSelect.appendChild(el);
    });

    largeRevSelect.innerHTML = '<option value="" selected disabled>اختر كمية المراجعة</option>';
    largeRevisionOptions.forEach(option => {
        const el = document.createElement('option');
        el.value = option.amount;
        el.textContent = option.name;
        largeRevSelect.appendChild(el);
    });
}

function setupDirectionSelectors() {
    const memDirectionSelect = document.querySelector('#memorizationDetailsContainer select');
    const revDirectionSelect = document.querySelector('#RevDetailsContainer select');

    memDirectionSelect.innerHTML = '';
    revDirectionSelect.innerHTML = '';

    memorizationDirections.forEach(direction => {
        const option = document.createElement('option');
        option.value = direction.value;
        option.textContent = direction.name;
        if (direction.default) option.selected = true;
        memDirectionSelect.appendChild(option);
    });

    revisionDirections.forEach(direction => {
        const option = document.createElement('option');
        option.value = direction.value;
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
        option.value = surah.id;
        option.textContent = surah.name;
        toSurahSelect.appendChild(option);
    });

    toSurahSelect.addEventListener('change', function () {
        const selectedSurah = surahs.find(s => s.id === parseInt(this.value));
        // alert(selectedSurah);
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

        // Get form values
        const name = document.getElementById('studentName').value;
        const age = parseInt(document.getElementById('studentAge').value);
        const gender = document.getElementById('studentGender').value;
        const nationality = document.getElementById('nationality').value;
        const parentPhone = document.getElementById('parentPhone').value;
        const studentPhone = document.getElementById('studentPhone').value;
        const notes = document.getElementById('notes').value;

        // Get memorization plan values
        const memorization_direction = document.getElementById('memDirection').value;
        const revision_direction = document.getElementById('revDirection').value;
        const start_surah = parseInt(document.getElementById('toSurah').value);
        const no_verse_in_surah = parseInt(document.getElementById('toVerse').value);
        const new_memorization_amount = parseFloat(document.getElementById('newMemorizationAmount').value);
        const small_revision_amount = parseFloat(document.getElementById('smallRevisionAmount').value);
        const large_revision_amount = parseFloat(document.getElementById('largeRevisionAmount').value);
        const memorization_days = parseInt(document.getElementById('selectedDays').value);

        // Create data object to send to backend
        const studentData = {
            name: name,
            age: age,
            gender: gender,
            nationality: nationality,
            parent_phone: parentPhone,
            student_phone: studentPhone,
            notes: notes,
            // Add plan info directly to student data as per your backend implementation
            memorization_direction: memorization_direction,
            start_surah: start_surah,
            no_verse_in_surah: no_verse_in_surah,
            revision_direction: revision_direction,
            new_memorization_amount: new_memorization_amount,
            small_revision_amount: small_revision_amount,
            large_revision_amount: large_revision_amount,
            memorization_days: memorization_days
        };

        // Show loading state
        const submitBtn = document.querySelector('button[type="submit"]');
        const originalBtnText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> جاري الحفظ...';
        submitBtn.disabled = true;

        // Send data to backend API
        // Update the fetch URL to use the correct backend URL
        fetch('http://localhost:5000/api/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            mode: 'cors', // Add this line
            credentials: 'include', // Add this line
            body: JSON.stringify(studentData)
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('Success:', data);

                // Show success toast
                const successToast = new bootstrap.Toast(document.getElementById('successToast'));
                successToast.show();

                // Reset form if not "save and add another"
                if (!event.submitter || event.submitter.id !== 'saveAndAddAnother') {
                    setTimeout(() => {
                        window.location.href = '../HTML/index.html'; // Redirect to students list
                    }, 1500);
                } else {
                    document.getElementById('addStudentForm').reset();
                }
            })
            .catch(error => {
                console.error('Error:', error);
                // Show error message
                alert('حدث خطأ أثناء حفظ بيانات الطالب. الرجاء المحاولة مرة أخرى.');
            })
            .finally(() => {
                // Reset button state
                submitBtn.innerHTML = originalBtnText;
                submitBtn.disabled = false;
            });
    });

    // Handle "Save and Add Another" button
    document.getElementById('saveAndAddAnother').addEventListener('click', function (event) {
        // Trigger form submission but mark this button as submitter
        const form = document.getElementById('addStudentForm');
        const submitEvent = new Event('submit', { bubbles: true, cancelable: true });
        submitEvent.submitter = this;
        form.dispatchEvent(submitEvent);
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
