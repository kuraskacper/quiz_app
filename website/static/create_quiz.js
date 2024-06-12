document.getElementById('add-question-btn').addEventListener('click', addQuestion);

var questionCounter = 0

function addQuestion(createFirstTwoAnswers = true){
    questionCounter++;

    document.getElementById("question-counter").value = questionCounter;

    const questionDiv = document.createElement('div');
    questionDiv.id = `question-${questionCounter}`
    questionDiv.classList.add('question');

    const answerCounter = document.createElement('input');
    answerCounter.id = 'counter';
    answerCounter.type = 'hidden';
    answerCounter.name = `question-${questionCounter}-answer-counter`;
    answerCounter.value = 0;

    questionDiv.appendChild(answerCounter);

    const questionTextAndBtnDiv = document.createElement('div');
    questionTextAndBtnDiv.className = 'question-text-and-btn';

    const questionText = document.createElement('input');
    questionText.id = 'text';
    questionText.type = 'text';
    questionText.classList.add('input');
    questionText.style.width = '80%';
    questionText.name = `question-${questionCounter}-text`;
    questionText.placeholder = `Podaj terść pytania nr ${questionCounter}`;

    questionTextAndBtnDiv.appendChild(questionText);

    const removeQuestionBtn = document.createElement('button');
    removeQuestionBtn.type = 'button';
    removeQuestionBtn.classList.add('delete-btn');
    removeQuestionBtn.innerHTML = '&times;';
    removeQuestionBtn.onclick = () => removeQuestion(questionDiv);


    questionTextAndBtnDiv.appendChild(removeQuestionBtn);

    questionDiv.appendChild(questionTextAndBtnDiv);

    answersDiv = document.createElement('div');
    answersDiv.id = "answers";

    questionDiv.appendChild(answersDiv);

    const addAnswerBtn = document.createElement('button');
    addAnswerBtn.type = 'button';
    addAnswerBtn.classList.add('input')
    addAnswerBtn.classList.add('btn')
    addAnswerBtn.innerText = "dodaj odpowiedź";
    addAnswerBtn.onclick = () => addAnswer(questionDiv);
    questionDiv.appendChild(addAnswerBtn);

    if(createFirstTwoAnswers){
        addAnswer(questionDiv);
        addAnswer(questionDiv);
    }


    document.getElementById('questions').appendChild(questionDiv);

    return questionTextAndBtnDiv
}

function addAnswer(questionDiv){
    const answerDiv = document.createElement('div');
    answerDiv.className = "ans"
    const answerCounter = questionDiv.querySelector('#counter');
    answerCount = parseInt(answerCounter.value);
    answerCount++;
    answerCounter.value = answerCount;

    answerDiv.innerHTML = `
        <input type="radio" name="correct-${questionDiv.id}" value="answer-${answerCount}" onchange="highlightRightAnswer(this)">
        <input type="text" class="ans_text input-small" placeholder="Odpowiedź nr ${answerCount}" name="${questionDiv.id}-answer-${answerCount}">
        <button type="button" class="delete-btn-small" onclick="removeAnswer(this)">&times;</button>
    `;

    questionDiv.querySelector('#answers').appendChild(answerDiv);

    return answerDiv;
}



function removeQuestion(questionDiv){
    questionCounter--;
    document.getElementById("question-counter").value = questionCounter;
    const allQuestions = document.getElementById('questions');

    allQuestions.removeChild(questionDiv);

    let questions = allQuestions.querySelectorAll(".question");

    for(let i = 0; i< questions.length; i++){
        questions[i].id = `question-${i+1}`;
        questions[i].querySelector("#counter").name = `question-${i+1}-answer-counter`;
        questions[i].querySelector("#text").name  = `question-${i+1}-text`;
        questions[i].querySelector("#text").placeholder  = `Podaj terść pytania nr ${i+1}`;

        answers = questions[i].querySelector("#answers").querySelectorAll(".ans");

        for(let j = 0; j<answers.length; j++){
            inputRadio = answers[j].querySelector('input[type="radio"]');
            inputRadio.name = `correct-${questions[i].id}`;
            inputText = answers[j].querySelector('input[type="text"]');
            inputText.name = `${questions[i].id}-answer-${j+1}`
        }

    }

}


function remakeAnswers(questionDiv, amount, values, checkedOne){

    questionDiv.querySelector('#answers').innerHTML = "";
    questionDiv.querySelector('#counter').value = 0;
    for(let i = 0; i<amount; i++){
        addAnswer(questionDiv)
    }

    answers = questionDiv.querySelector("#answers").querySelectorAll(".ans");
    for( let i = 0; i<answers.length; i++){
        answers[i].querySelector(".ans_text").value = values[i];
        if (checkedOne == i){
            answers[i].querySelector('input[type="radio"]').checked = true;
            answers[i].querySelector('input[type="radio"]').parentNode.style.backgroundColor = '#aaff80';
        }
    }



}

function removeAnswer(answerBtn){
    const answerDiv = answerBtn.parentNode;

    const questionDiv = answerDiv.parentNode.parentNode;

    const answerCounter = questionDiv.querySelector('#counter');
    answerCount = answerCounter.value;
    answerCount--;
    answerCounter.value = answerCount;

    answerId = answerDiv.querySelector('input[type="radio"]').value.split('-')[1];

    values = []
    checkedOne = -1

    answers = questionDiv.querySelector("#answers").querySelectorAll(".ans");
    for(let i = 0; i <= answerCount; i++){
        if (answers[i].querySelector('input[type="radio"]').value.split('-')[1] != answerId){
            values.push(answers[i].querySelector('.ans_text').value)

            if(answers[i].querySelector('input[type="radio"]').checked){
                checkedOne = i;
                if (answerId-1 < i){
                    checkedOne -= 1;
                }

            }
            answers[i].querySelector('input[type="radio"]').checked = false;
        }
    }

    console.log(checkedOne);

    remakeAnswers(questionDiv, answerCount, values, checkedOne)

}




function highlightRightAnswer(radioBtn){
    let radioButtons = radioBtn.parentNode.parentNode.parentNode.querySelectorAll('input[type="radio"]');
    radioButtons.forEach(btn => {
        btn.parentNode.style.backgroundColor = '';
    });
    if (radioBtn.checked){
        radioBtn.parentNode.style.backgroundColor = '#aaff80';
        radioBtn.checked = true;
    }
    else{
        radioBtn.checked = false;
    }

}

function remakeQuiz(quiz = {}){

    document.getElementById('title').value = quiz['info']['title'];
    document.getElementById('description').value = quiz['info']['description'];

    questionCount = quiz['info']['question_count'];
    for(let i = 0; i<questionCount; i++){
        addQuestion(false);
        const questionDiv = document.getElementById('questions').querySelectorAll('.question')[i]
        questionDiv.querySelector('#text').value = quiz['questions'][i]['text']
        for(let j = 0; j<quiz['questions'][i]['answer_count']; j++){
            answerDiv = addAnswer(questionDiv)
            if(quiz['questions'][i]['correct_answer'] !== null){
                if(quiz['questions'][i]['correct_answer'] == j+1){
                    answerDiv.querySelector('input[type="radio"]').checked = true;
                        answerDiv.querySelector('input[type="radio"]').parentNode.style.backgroundColor = '#aaff80';
                }
            }
            answerDiv.querySelector('input[type="text"]').value = quiz['questions'][i]['answers'][j];
        }
    }

}
