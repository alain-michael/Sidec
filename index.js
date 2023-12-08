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


// script.js to handle thank you message
document.addEventListener("DOMContentLoaded", function () {
    var contactForm = document.getElementById("contactForm");
    var thankYouMessage = document.getElementById("thankYouMessage");

    contactForm.addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent the form from submitting (for demo purposes)

        // You can add code here to handle the actual form submission (e.g., using AJAX)

        // Show the thank-you message
        thankYouMessage.style.display = "block";

        // Hide the thank-you message after a certain duration (e.g., 5 seconds)
        setTimeout(function () {
            thankYouMessage.style.display = "none";
        }, 5000);
    });
});


// script to handle review 
var courseData = {
    labels: ['Biology', 'Physics', 'Mathematics', 'Chemistry', 'History'],
    scores: [80, 75, 90, 85, 70]
};

// Get the canvas element
 // Sample data (replace this with your actual data)
 var courseData = {
    labels: ['Biology', 'Physics', 'Mathematics', 'Chemistry', 'History'],
    scores: [80, 75, 90, 85, 70]
};

 // Sample data (replace this with your actual data)
 var courseData = {
    labels: ['Biology', 'Physics', 'Mathematics', 'Chemistry', 'History'],
    scores: [80, 75, 90, 85, 70]
};

// Get the canvas element
var ctx = document.getElementById('myChart').getContext('2d');

// Create a styled bar chart with reduced bar width
var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: courseData.labels,
        datasets: [{
            label: 'Your preformance, Fred',
            data: courseData.scores,
            backgroundColor: 'rgba(152, 53, 255, 0.8)', // Background color of bars
            borderColor: 'rgba(152, 53, 255, 0.5)', // Border color of bars
            borderWidth: 1 // Border width of bars
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                max: 100,
                grid: {
                    display: false // Remove grid lines on the y-axis
                }
            },
            x: {
                grid: {
                    display: false // Remove grid lines on the x-axis
                }
            }
        },
        plugins: {
            legend: {
                display: true,
                position: 'top', // Position of the legend
                labels: {
                    font: {
                        size: 12 // Font size of the legend labels
                    }
                }
            }
        },
        layout: {
            padding: {
                left: 5, // Adjust left padding to make room for y-axis labels
                right: 5 // Adjust right padding
            }
        }
    }
});


//Function for to-do list

function toggleTask(taskId) {
    const checkbox = document.getElementById(taskId);
    const label = checkbox.nextElementSibling;
    label.style.textDecoration = checkbox.checked ? 'line-through' : 'none';
}

function addTask() {
    const newTaskInput = document.getElementById('new-task');
    const newTaskText = newTaskInput.value.trim();

    if (newTaskText !== '') {
        const tasksList = document.getElementById('tasks-list');
        const newTaskId = 'task' + (tasksList.children.length + 1);

        const newTask = document.createElement('li');
        newTask.innerHTML = `
            <input type="checkbox" id="${newTaskId}" onclick="toggleTask('${newTaskId}')">
            <label for="${newTaskId}">${newTaskText}</label>
        `;

        tasksList.appendChild(newTask);
        newTaskInput.value = '';
    }
}
