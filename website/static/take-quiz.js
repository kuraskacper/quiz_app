function highlightSelectedAnswer(radio){

    const answers = radio.parentNode.parentNode.querySelectorAll('.answer')

     answers.forEach(answer => {
        answer.style.backgroundColor = 'white';
     });

    if(radio.checked){
        radio.parentNode.style.backgroundColor = '#d1d1d1';
    }
    else{
        radio.parentNode.style.backgroundColor = 'white';
    }

}
