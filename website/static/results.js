function closeAllResults() {
    var resultDetailsElements = document.querySelectorAll('.result-details');
    resultDetailsElements.forEach(function(resultDetails) {
        resultDetails.style.display = 'none';
        resultDetails.parentNode.style.borderColor = '#ccc';
        resultDetails.parentNode.style.outlineColor = 'white';
        resultDetails.parentNode.querySelector('.result-header').style.borderBottom = 'none'
    });
}

function toggleResultDetails(resultId) {
    var resultDetails = document.getElementById(resultId);
    var isCurrentlyVisible = resultDetails.style.display === 'block';

    closeAllResults();

    if (!isCurrentlyVisible) {
        resultDetails.style.display = 'block';
        resultDetails.parentNode.style.borderColor = 'dodgerblue';
        resultDetails.parentNode.style.outlineColor = 'dodgerblue';
        resultDetails.parentNode.querySelector('.result-header').style.borderBottom = '1px solid #ddd'

    }
}

function closeAllAnswers() {
    var answerDetailsElements = document.querySelectorAll('.answer-details');
    answerDetailsElements.forEach(function(answerDetails) {
        answerDetails.style.display = 'none';
        answerDetails.parentNode.style.borderColor = '#ccc';
        answerDetails.parentNode.style.outlineColor = 'white';
        answerDetails.parentNode.querySelector('.answer-header').style.borderBottom = 'none'
    });
}

function toggleAnswerDetails(answerId, color) {
    var answerDetails = document.getElementById(answerId);
    var isCurrentlyVisible = answerDetails.style.display === 'block';

    closeAllAnswers();

    if (!isCurrentlyVisible) {
        answerDetails.style.display = 'block';
        answerDetails.parentNode.style.borderColor = color;
        answerDetails.parentNode.style.outlineColor = color;
        answerDetails.parentNode.querySelector('.answer-header').style.borderBottom = '1px solid #ddd'

    }
}