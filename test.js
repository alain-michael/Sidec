// --------------------for responsive side bar
function myFunction1(x) {
    if (x.matches) { // If media query matches
      document.querySelector(".ham_menu").click()
    } 
  }
  
  // Create a MediaQueryList object
  var x = window.matchMedia("(max-width: 768px)")
  
  // Call listener function at run time
  setTimeout(()=>{
    myFunction1(x);
  },10)

  
  // Attach listener function on state changes
  x.addEventListener("change", function() {
    myFunction1(x);
  });
         
/* Toggle menu */

let arrow = document.querySelectorAll(".arrow");

for (var i = 0; i < arrow.length; i++) {
    arrow[i].addEventListener("click", (e) => {
        let arrowParent = e.target.parentElement.parentElement;
        arrowParent.classList.toggle("ShowMenu");
    });
}
    let sidebar = document.querySelector(".sidebar");
    let sidebarbtn = document.querySelector(".ham_menu");
    sidebarbtn.addEventListener("click", () => {
        sidebar.classList.toggle("close")
    })

    /* script for profile */
    let profile = document.querySelector('.home-section .home-content .flex .profile-2');

    document.querySelector('#user-btn').onclick = () =>{
        profile.classList.toggle('active');
        SearchForm.classList.remove('active');
    }

    let SearchForm = document.querySelector('.home-section .home-content .flex .search-form');

document.querySelector('#search-btn').onclick = () =>{
    SearchForm.classList.toggle('active');
}

    window.onscroll = () => {
        profile.classList.remove('active');
        SearchForm.classList.remove('active');
    }

//script 
const progressBar = document.querySelector(".progress-bar");
const progressText = document.querySelector(".progress-text");

const progress = (value) => {
    const percentage = (value / time) * 100;
    progressBar.style.width = `${percentage}%`
    progressText.innerHTML = `${value}`;
};

let questions,
    time = 30,
    score = 0,
    currentQuestion,
    timer;

const startBtn = document.querySelector(".start"),
    numQuestions = document.querySelector("#num-questions"),
    category = document.querySelector("#category"),
    difficulty = document.querySelector("#difficulty"),
    timePerQuestion = document.querySelector("#time"),
    quiz = document.querySelector(".quiz"),
    startscreen = document.querySelector(".start-screen");

const startQuiz = () => {
    const num = numQuestions.value;
    cat = category.value;
    diff = difficulty.value;
//api url
const url = `https://opentdb.com/api.php?amount=${encodeURIComponent(num)}&category=${encodeURIComponent(cat)}&difficulty=${encodeURIComponent(diff)}&type=multiple`;


fetch(url)
.then((res) => res.json())
.then((data) => {
  que stions = data.results;
 // Add this line for debugging
  startscreen.classList.add("hide");
  quiz.classList.remove("hide");
  currentQuestion = 0;

  showQuestion(questions[1]);
});


};

startBtn.addEventListener("click", startQuiz);

const submitBtn = document.querySelector(".submit"),
nextBtn = document.querySelector(".next");

const showQuestion = (question) => {
    const questionText = document.querySelector(".question");

    answersWrapper = document.querySelector(".answer-wrapper");
    questionNumber = document.querySelector(".number");

questionText.innerHTML = question.question;

const answers = [...question.incorrect_answers,
     question.correct_answer.toString(),
];

//shuffle array

answers.sort(() => Math.random() - 0.5);
answersWrapper.innerHTML = "";
answers.forEach((answer) => {
    answersWrapper.innerHTML += `
    <div class="answer">
    <span class="text">${answer}</span>
    <span class="checkbox">
        <span class="icon">✔</span>
    </span>
</div>
`;
});

questionNumber.innerHTML = `
Question <span class="current">${currentQuestion + 1}</span>
<span class="total">${questions.length}</span>
`;


const answersDiv = document.querySelectorAll(".answer");
answersDiv.forEach((answer) => {
    answer.addEventListener("click", () => {
        console.log("From answersDiv", answer.textContent)
        // if answer not already submitted
        if (!answer.classList.contains("checked")) {
            // remove selected for other answers
            answersDiv.forEach((otherAnswer) => {
                otherAnswer.classList.remove("selected");
            });
            answer.classList.add("selected");
            submitBtn.disabled = false;
        }
    });
});

// after updating question, start timer
time = timePerQuestion.value;
startTimer(time);
};

const startTimer = (time) => {
    timer = setInterval(() => {
        if (timer >= 0) {
            progress(time);
            time--;
        } else {
            checkAnswer();
        }
    }, 1000);
};

submitBtn.addEventListener("click", () => {
    checkAnswer();
});

function checkAnswer () {
    clearInterval(timer);

    const selectedAnswer = document.querySelector(".answer.selected");
    if (selectedAnswer) {
        const answer = selectedAnswer.querySelector(".text").innerHTML;
        if (answer == questions[currentQuestion - 1].correct_answer) {
            // if answer matches with correct answer, increase score
            score++;
            selectedAnswer.classList.add("correct");
        } else {
            // if wrong selected
            const correctAnswer = document.querySelectorAll(".answer").forEach((answer) => {
                if (answer.querySelector(".text").innerHTML == questions[currentQuestion - 1].correct_answer) {
                    answer.classList.add("correct");
                }
            });
        }
    }
};
