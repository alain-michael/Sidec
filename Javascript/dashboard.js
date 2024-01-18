
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


    document.addEventListener("DOMContentLoaded", function () {
        // Line chart
        var lineChartData = {
            labels: ["January", "February", "March", "April", "May", "June", "July", "August"],
            datasets: [
                {
                    label: "Current performance",
                    borderColor: "rgb(152, 53, 255)",
                    data: [65, 59, 80, 81, 56, 67, 84, 98],
                    fill: false,
                    lineTension: 0.4,
                },
                {
                    label: "2021",
                    borderColor: "rgb(220, 220, 220)",
                    data: [45, 70, 60, 85, 75, 68, 75, 69],
                    fill: false,
                    lineTension: 0.4,
                }
            ]
        };
    
        var lineChartOptions = {
            responsive: true,
        };
    
        var lineCtx = document.getElementById('lineChart').getContext('2d');
        var lineChart = new Chart(lineCtx, {
            type: 'line',
            data: lineChartData,
            options: lineChartOptions
        });
    
        // Donut chart
        var donutChartData = {
            labels: ['Completed', 'In Progress'],
            datasets: [{
                data: [30, 70],
                backgroundColor: ['#36A2EB', '#9538ff'],
                borderWidth: 1,
            }],
        };
    
        var donutChartOptions = {
            responsive: true,
            cutout: '85%',
        };
    
        var donutCtx = document.getElementById('courseDonutChart').getContext('2d');
        var donutChart = new Chart(donutCtx, {
            type: 'doughnut',
            data: donutChartData,
            options: donutChartOptions
        });
    
        // Pie chart
        var pieChartData = {
            labels: ["Buea", "Kigali", "Lagos"],
            datasets: [
                {
                    data: [75, 15, 10],
                    backgroundColor: ["#3498db", "#2ecc71", "#e74c3c"],
                },
            ],
        };
    
        var pieChartOptions = {
            title: {
                display: true,
                text: "Top Student Locations",
            },
        };
    
        var pieCtx = document.getElementById("myPieChart").getContext("2d");
        var pieChart = new Chart(pieCtx, {
            type: "pie",
            data: pieChartData,
            options: pieChartOptions,
        });
    
        // Your other functions and event listeners go here
    
        // For example, the to-do list functions:
    
        function toggleTask(taskId) {
            const checkbox = document.getElementById(taskId);
            const label = checkbox.nextElementSibling;
            label.style.textDecoration = checkbox.checked ? 'line-through' : 'none';
        }
    
        function removeTask(taskId) {
            const taskElement = document.getElementById(taskId);
            if (taskElement) {
                taskElement.parentElement.remove();
            }
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
                    <span class="remove-btn" onclick="removeTask('${newTaskId}')">&times;</span>
                `;
    
                tasksList.appendChild(newTask);
                newTaskInput.value = '';
            }
        }
    });
   
   
    //script for calendar
    const daysTag = document.querySelector(".days"),
currentDate = document.querySelector(".current-date"),
prevNextIcon = document.querySelectorAll(".icons span");
// getting new date, current year and month
let date = new Date(),
currYear = date.getFullYear(),
currMonth = date.getMonth();
// storing full name of all months in array
const months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"];
const renderCalendar = () => {
    let firstDayofMonth = new Date(currYear, currMonth, 1).getDay(), // getting first day of month
    lastDateofMonth = new Date(currYear, currMonth + 1, 0).getDate(), // getting last date of month
    lastDayofMonth = new Date(currYear, currMonth, lastDateofMonth).getDay(), // getting last day of month
    lastDateofLastMonth = new Date(currYear, currMonth, 0).getDate(); // getting last date of previous month
    let liTag = "";
    for (let i = firstDayofMonth; i > 0; i--) { // creating li of previous month last days
        liTag += `<li class="inactive">${lastDateofLastMonth - i + 1}</li>`;
    }
    for (let i = 1; i <= lastDateofMonth; i++) { // creating li of all days of current month
        // adding active class to li if the current day, month, and year matched
        let isToday = i === date.getDate() && currMonth === new Date().getMonth() 
                     && currYear === new Date().getFullYear() ? "active" : "";
        liTag += `<li class="${isToday}">${i}</li>`;
    }
    for (let i = lastDayofMonth; i < 6; i++) { // creating li of next month first days
        liTag += `<li class="inactive">${i - lastDayofMonth + 1}</li>`
    }
    currentDate.innerText = `${months[currMonth]} ${currYear}`; // passing current mon and yr as currentDate text
    daysTag.innerHTML = liTag;
}
renderCalendar();
prevNextIcon.forEach(icon => { // getting prev and next icons
    icon.addEventListener("click", () => { // adding click event on both icons
        // if clicked icon is previous icon then decrement current month by 1 else increment it by 1
        currMonth = icon.id === "prev" ? currMonth - 1 : currMonth + 1;
        if(currMonth < 0 || currMonth > 11) { // if current month is less than 0 or greater than 11
            // creating a new date of current year & month and pass it as date value
            date = new Date(currYear, currMonth, new Date().getDate());
            currYear = date.getFullYear(); // updating current year with new date year
            currMonth = date.getMonth(); // updating current month with new date month
        } else {
            date = new Date(); // pass the current date as date value
        }
        renderCalendar(); // calling renderCalendar function
    });
});


  // Function to open the chat form and close the floating message
  function openFormAndCloseMessage() {
    document.getElementById('floating-message').style.display = 'none';
    document.getElementById('myForm').style.display = 'block';
  }

  // Function to close the chat form
  function closeForm() {
    document.getElementById('myForm').style.display = 'none';
  }

  // Add event listener for the reply icon
  document.querySelector('.reply-icon').addEventListener('click', function () {
    openFormAndCloseMessage();
  });

  // Add event listener for the close icon
  document.querySelector('.close-icon').addEventListener('click', function () {
    document.getElementById('floating-message').style.display = 'none';
  });
  

  //script for acordion 

  var acc = document.getElementsByClassName("accordion");
var i;

for (i = 0; i < acc.length; i++) {
  acc[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var panel = this.nextElementSibling;
    if (panel.style.maxHeight) {
      panel.style.maxHeight = null;
    } else {
      panel.style.maxHeight = panel.scrollHeight + "px";
    }
  });
}
//script 
// JavaScript code for course tabs
function openTab(evt, tabName) {
    var i, courses, tablinks;
    courses = document.getElementsByClassName("tabcontent");
    for (i = 0; i < courses.length; i++) {
        courses[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

// Get the element with id="defaultOpen" and click on it
document.getElementById("inProgressTab").click();

