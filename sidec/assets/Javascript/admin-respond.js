document.addEventListener('DOMContentLoaded', function () {
    const video = document.getElementById('courseVideo');
    const overlay = document.querySelector('.overlay');
    const playIcon = document.querySelector('.ri-play-fill');
  
    // Play/pause on overlay click
    overlay.addEventListener('click', function () {
      if (video.paused) {
        video.play();
        playIcon.style.display = 'none'; // Hide play icon when video starts playing
      } else {
        video.pause();
      }
    });
  
    // Toggle play icon on video play/pause
    video.addEventListener('playing', function () {
      playIcon.style.display = 'none'; // Hide play icon when video is playing
    });
  
    video.addEventListener('pause', function () {
      playIcon.style.display = 'flex'; // Show play icon when video is paused
    });
  
    // Toggle volume controls
    video.addEventListener('volumechange', function () {
      if (video.muted) {
        // Show mute icon when video is muted
        // You can add your own mute icon class or use 'fa-volume-mute' from Font Awesome
        volumeIcon.classList.add('mute-icon');
      } else {
        // Show volume icon when video is not muted
        volumeIcon.classList.remove('mute-icon');
      }
    });
  
    // Add hover effect
    overlay.addEventListener('mouseenter', function () {
      overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
    });
  
    overlay.addEventListener('mouseleave', function () {
      overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.0)';
    });
});

  

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

//function for search in questions tab
function myFunction() {
  // Declare variables
  var input, filter, ul, li, a, i;
  input = document.getElementById("mySearch");
  filter = input.value.toUpperCase();
  ul = document.getElementById("myMenu");
  li = ul.getElementsByTagName("li");

  // Loop through all list items, and hide those who don't match the search query
  for (i = 0; i < li.length; i++) {
    a = li[i].getElementsByTagName("a")[0];
    if (a.innerHTML.toUpperCase().indexOf(filter) > -1) {
      li[i].style.display = "";
    } else {
      li[i].style.display = "none";
    }
  }
}


/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function myFunction3() {
    document.getElementById("myDropdown").classList.toggle("show");
  }
  
  // Close the dropdown menu if the user clicks outside of it
  window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
      var dropdowns = document.getElementsByClassName("dropdown-content");
      var i;
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
  }

  //form
  function openForm() {
    document.getElementById("myForm").style.display = "block";
  }
  
  function closeForm() {
    document.getElementById("myForm").style.display = "none";
  }