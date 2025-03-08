// studentsData.js
export const students = [
    {
        id: 1,
        name: "أحمد محمد",
        age: 14,
        memorizedParts: 5,
        percentageValue: 16,
        percentage: "16%",
        lastUpdate: "2024-03-08",
        evaluation: "ممتاز",

    },
    {
        id: 2,
        name: "عمر خالد",
        age: 15,
        memorizedParts: 7,
        percentageValue: 23,
        percentage: "23%",
        lastUpdate: "2024-03-08",
        evaluation: "ممتاز",

    },
    {
        id: 3,
        name: "محمد إبراهيم",
        age: 13,
        memorizedParts: "3 أجزاء",
        percentage: "10%",
        lastUpdate: "2024-03-07",
        evaluation: "جيد جداً",

    },
    {
        id: 4,
        name: "عبدالله سعد",
        age: 16,
        memorizedParts: "10 أجزاء",
        percentage: "33%",
        lastUpdate: "2024-03-07",
        evaluation: "ممتاز",

    },
    {
        id: 5,
        name: "يوسف أحمد",
        age: 14,
        memorizedParts: "4 أجزاء",
        percentage: "13%",
        lastUpdate: "2024-03-06",
        evaluation: "جيد",

    },
    {
        id: 6,
        name: "زياد محمود",
        age: 15,
        memorizedParts: "6 أجزاء",
        percentage: "20%",
        lastUpdate: "2024-03-06",
        evaluation: "جيد جداً",

    },
    {
        id: 7,
        name: "عبدالرحمن علي",
        age: 13,
        memorizedParts: "2 أجزاء",
        percentage: "7%",
        lastUpdate: "2024-03-05",
        evaluation: "جيد",

    },
    {
        id: 8,
        name: "خالد وليد",
        age: 15,
        memorizedParts: "8 أجزاء",
        percentage: "27%",
        lastUpdate: "2024-03-05",
        evaluation: "ممتاز",

    },
    {
        id: 9,
        name: "فهد سلطان",
        age: 14,
        memorizedParts: "5 أجزاء",
        percentage: "17%",
        lastUpdate: "2024-03-04",
        evaluation: "جيد جداً",

    },
    {
        id: 10,
        name: "سعد ناصر",
        age: 16,
        memorizedParts: "12 أجزاء",
        percentage: "40%",
        lastUpdate: "2024-03-04",
        evaluation: "ممتاز",

    }
];

// Simple data arrays for filters and selections
export const evaluations = ['ممتاز', 'جيد جداً', 'جيد', 'مقبول', 'ضعيف'];
export const lastUpdates = ['2024-03-08', '2024-03-07', '2024-03-06', '2024-03-05', '2024-03-04'];

// Helper function to get student by ID
export const getStudentById = (id) => {
    return students.find(student => student.id === id) || null;
};

// Helper function to filter students by evaluation
export const filterStudentsByEvaluation = (evaluation) => {
    return students.filter(student => student.evaluation === evaluation);
};