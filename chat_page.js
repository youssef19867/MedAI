let currentQuestionIndex = -1;
let answers = {};

// Predefined symptom categories
const questions = [
    "Skin & Nail Symptoms",
    "Respiratory & Throat Symptoms",
    "Gastrointestinal & Digestive Symptoms",
    "Urinary & Bladder Symptoms",
    "Liver & Metabolic Symptoms",
    "Fever/Infection/Inflammation",
    "Neurological & Sensory Symptoms",
    "Musculoskeletal & Joint Symptoms",
    "Cardiovascular & Circulation",
    "Weight/Appetite & Endocrine",
    "Psychological & Mood Symptoms",
    "Eye & Vision Symptoms",
    "Miscellaneous/Other",
    "Risk Factors & Exposures"
];

// DOM Elements
const messagesDiv = document.querySelector('.messages');
const inputField = document.querySelector('input');
const sendButton = document.querySelector('button');

// Initialize chat
function initChat() {
    currentQuestionIndex = 0;
    askQuestion();
}

function askQuestion() {
    const botMsg = document.createElement('div');
    botMsg.className = 'message bot-message';
    botMsg.textContent = `Have you experienced any ${questions[currentQuestionIndex]}? (Yes/No)`;
    messagesDiv.appendChild(botMsg);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function handleUserInput(message) {
    const normalized = message.toLowerCase();
    if (!['yes', 'no', 'y', 'n'].includes(normalized)) {
        showError('Please answer with Yes or No.');
        return false;
    }
    answers[questions[currentQuestionIndex]] = normalized.startsWith('y') ? 1 : 0;
    currentQuestionIndex++;
    return true;
}

function showError(text) {
    const errorMsg = document.createElement('div');
    errorMsg.className = 'message bot-message';
    errorMsg.textContent = text;
    messagesDiv.appendChild(errorMsg);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function sendMessage() {
    const message = inputField.value.trim();
    if (!message) return;

    // Add user message
    const userMsg = document.createElement('div');
    userMsg.className = 'message user-message';
    userMsg.textContent = message;
    messagesDiv.appendChild(userMsg);

    // Handle conversation flow
    if (currentQuestionIndex >= 0 && currentQuestionIndex < questions.length) {
        if (!handleUserInput(message)) {
            inputField.value = '';
            return;
        }

        if (currentQuestionIndex < questions.length) {
            askQuestion();
        } else {
            submitAnswers();
        }
    }

    inputField.value = '';
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// Modify the submitAnswers function to use feature names
function submitAnswers() {
    const botMsg = document.createElement('div');
    botMsg.className = 'message bot-message';
    botMsg.textContent = 'Analyzing your symptoms...';
    messagesDiv.appendChild(botMsg);

    // Convert question texts to feature format
    const formattedAnswers = {};
    questions.forEach((question, index) => {
        const featureName = question.toLowerCase()
            .replace(/&/g, 'and')
            .replace(/[^a-zA-Z0-9 ]/g, '')
            .replace(/ +/g, '_');
        formattedAnswers[featureName] = answers[question];
    });

    fetch('http://127.0.0.1:8000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formattedAnswers)
    })
    .then(response => {
        if (!response.ok) throw new Error('Server error');
        return response.json();
    })
    .then(showResults)
    .catch(handleError);
}

function showResults(data) {
    const resultMsg = document.createElement('div');
    resultMsg.className = 'message bot-message';
    resultMsg.innerHTML = `
        Predicted Condition: ${data.prediction}<br>
        Confidence: ${data.confidence}%
        <br><br><em>Remember: This is not a substitute for professional medical advice.</em>
    `;
    messagesDiv.appendChild(resultMsg);
}

function handleError(error) {
    console.error('Error:', error);
    showError('Error processing your request. Please try again.');
}

// Event Listeners
sendButton.addEventListener('click', sendMessage);
inputField.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

// Initialize the chat
initChat();
