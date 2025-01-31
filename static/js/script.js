// Add interactivity (e.g., voice input for symptoms)
document.addEventListener('DOMContentLoaded', function () {
    const symptomInput = document.getElementById('symptoms');
    const voiceButton = document.getElementById('voice-button');

    if (voiceButton) {
        voiceButton.addEventListener('click', function () {
            const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.lang = 'en-US';
            recognition.start();

            recognition.onresult = function (event) {
                const transcript = event.results[0][0].transcript;
                symptomInput.value = transcript;
            };
        });
    }
});
