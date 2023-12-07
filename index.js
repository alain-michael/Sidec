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

