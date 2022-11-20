$(function () {
    $('#Start').click(function () {
        $.ajax({
            url: '/addition_questions',
            type: 'GET',
            datatype: 'json',
            success: (response) => {
                // console.log(response)
                createNextButton();
                createPreviousButton();
                removeStartButton();
                main(response['numofq'], response['qmodule'], response['questionset'])
            },
            error: (error) => {
                console.log(error)
            }
        });
    });
});

let questionNumber = 0;
let q;
let a1;
let a2;
let a3;
let a4;
let answer;
let answers = [];
let score = 0;
let question_data;
let numq;
let qmod;
let finishButtonCreated = false;

const removeStartButton = () => {
    let element = document.getElementById("Start");
    element.remove();
    console.log("Removed start button.");
}

function main(numofq, qmodule, questionset) {
    numq = numofq;
    qmod = qmodule;
    question_data = questionset
    loadq(questionNumber);
}

function loadq(i) {
    console.log("Question number: ", questionNumber);
    q = document.getElementById("question");
    a1 = document.getElementById("answer1");
    a2 = document.getElementById("answer2");
    a3 = document.getElementById("answer3");
    a4 = document.getElementById("answer4");
    q.innerHTML = question_data[questionNumber]['quiz_question']
    a1.innerHTML = question_data[questionNumber]['A']
    a2.innerHTML = question_data[questionNumber]['B']
    a3.innerHTML = question_data[questionNumber]['C']
    a4.innerHTML = question_data[questionNumber]['D']
    answer = question_data[i]['quiz_answer']
}

function saveQuestionAnswer() {
    // Different scopes of the answer box
    let ans = document.getElementById("answerbox");
//    console.log(ans)
    ans = ans.querySelector(".answers");
//    console.log(ans)
    ans = ans.querySelector(".answer");
//    console.log("1", ans)
    ans = ans.innerHTML;
//    console.log("2", ans)
    answers[questionNumber] = (ans);
    // console.log(answers)
}

function createNextButton() {
    let mydiv = document.getElementById("next");
    let button = document.createElement('BUTTON');
    let text = document.createTextNode("Next");
    button.appendChild(text);
    button.id = "nextbutton";
    button.className = "btn btn-lg btn-primary btn-block";
    button.onclick = () => {
        saveQuestionAnswer();

        // If trying to go to next question that exists
        if ((questionNumber + 1) < numq) {
            questionNumber++;
            loadq(questionNumber);
        } // If trying to go to previous question that does not exist
        else if ((questionNumber + 1) >= numq) {
            if (finishButtonCreated !== true) {
                finishButtonCreated = true;
                createFinishButton();
            }
        }
    };
    mydiv.appendChild(button);
}

function createPreviousButton() {
    let mydiv = document.getElementById("previous");
    let button = document.createElement('BUTTON');
    let text = document.createTextNode("Previous");
    button.appendChild(text);
    button.id = "previousButton";
    button.className = "btn btn-lg btn-primary btn-block";
    button.onclick = () => {
        saveQuestionAnswer();

        // If trying to go to previous question that exists
        if ((questionNumber - 1) >= 0) {
            questionNumber--;
            loadq(questionNumber);
        } // If trying to go to previous question that does not exist do nothing

    };
    mydiv.appendChild(button);
}

function createFinishButton() {
    let mydiv = document.getElementById("finish");
    let button = document.createElement('BUTTON');
    let text = document.createTextNode("Finish");
    button.appendChild(text);
    button.id = "finishbutton";
    button.className = "btn btn-lg btn-primary btn-block";
    button.onclick = () => {
        for (let i = 0; i <= (question_data.length - 1); i++) {
            // console.log(i)
            // console.log(answers[i])
            // console.log(question_data[i])
            // console.log(question_data[i]['quiz_answer'])
            if (answers[i] === question_data[i]['quiz_answer']) {
                score++;
            }
        }

        console.log("Score: ", score);
        
        //Print the snackbar at the bottom of the page
        QuizFinished();

        //Redirect after snackbar
        setTimeout(function(){
            redirect();
        }, 3000);

        // $.ajax({
        //     url: '/send_results',
        //     type: 'GET',
        //     data: {
        //         Score: score, Module: qmod, Num: numq
        //     },
        //     success: (response) => {
        //         console.log("Success response", response)
        //         //                location.href = "/moduleSelection";
        //     },
        //     error: (error) => {
        //         console.log("error response", error);
        //         //                location.href = "/moduleSelection";
        //     }
        // });
    }
    mydiv.appendChild(button);
}


function allowDrop(event) {
    event.preventDefault();
}

function drag(event) {
    event.dataTransfer.setData("Text", event.target.id);
}

function answer_box_drop(event) {
    event.preventDefault();
    let data = event.dataTransfer.getData("text");
    if (event.target.childNodes.length >= 1) {
        console.log("Prevented multiple answers being given.")
        event.preventDefault();
    } else {
        event.target.appendChild(document.getElementById(data));
    }
}

function drop(event) {
    event.preventDefault();
    let data = event.dataTransfer.getData("text");
    event.target.appendChild(document.getElementById(data));
}

function QuizFinished() {
    // Get the snackbar DIV
    var x = document.getElementById("snackbar");
  
    // Add the "show" class to DIV
    x.className = "show";
  
    // After 3 seconds, remove the show class from DIV
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);

}

function redirect(){
    window.location='/profile';
}
