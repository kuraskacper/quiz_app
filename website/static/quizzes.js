function closeAllQuizzes() {
    var quizDetailsElements = document.querySelectorAll('.quiz-details');
    quizDetailsElements.forEach(function(quizDetails) {
        quizDetails.style.display = 'none';
        quizDetails.parentNode.style.borderColor = '#ccc';
        quizDetails.parentNode.style.outlineColor = 'white';
        quizDetails.parentNode.querySelector('.quiz-header').style.borderBottom = 'none'
    });
}

function toggleQuizDetails(quizId) {
    var quizDetails = document.getElementById(quizId);
    var isCurrentlyVisible = quizDetails.style.display === 'block';

    closeAllQuizzes();

    if (!isCurrentlyVisible) {
        quizDetails.style.display = 'block';
        quizDetails.parentNode.style.borderColor = 'dodgerblue';
        quizDetails.parentNode.style.outlineColor = 'dodgerblue';
        quizDetails.parentNode.querySelector('.quiz-header').style.borderBottom = '1px solid #ddd'

    }
}