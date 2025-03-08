// Arrays for dropdowns
const memorizationAmounts = [
    "ثمن صفحة (حوالي سطران)",
    // ... rest of the array
];

const smallRevisionAmounts = [
    "نصف صفحة",
    // ... rest of the array
];

const largeRevisionAmounts = [
    "صفحة",
    // ... rest of the array
];

// Initialize form functionality
document.addEventListener('DOMContentLoaded', function () {
    populateSurahs();
    setupMemorizationToggle();
    setupDaySelection();
    setupFormSubmission();
    setupVerseValidation();
    populateDropdowns();

    // Set default date to today
    document.getElementById('registrationDate').valueAsDate = new Date();
});

// Functions
function populateDropdowns() {
    // ... existing function
}

function setupDaySelection() {
    // ... existing function
}

function setupVerseValidation() {
    // ... existing function
}

function setupFormSubmission() {
    // ... existing function
}