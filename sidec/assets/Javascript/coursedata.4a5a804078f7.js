


function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        mybutton.style.display = "block";
    } else {
        mybutton.style.display = "none";
    }
};

// When the user clicks on the button, scroll to the top of the document smoothly
function toggleDropdown() {
  var dropdownContent = document.getElementById("myDropdown");
  var arrowIcon = document.getElementById("arrowIcon");
  if (dropdownContent.style.display === "block") {
    dropdownContent.style.display = "none";
    arrowIcon.classList.remove("rotate");
  } else {
    dropdownContent.style.display = "block";
    arrowIcon.classList.add("rotate");
  }
};

//Script for course accordion 
function openCourse(evt, courseName) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(courseName).style.display = "block";
  evt.currentTarget.className += " active";
}

function myFunction() {
  var x = document.getElementById("ReadMore");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
};

//script for toggling navbar
function toggleNavbar() {
  var x = document.getElementById("myLinks");
  if (x.style.display === "block") {
    x.style.display = "none";
  } else {
    x.style.display = "block";
  }
};
function toggleMobileDropdown() {
  var mobileDropdownContent = document.getElementById("mobileDropdown");
  var arrowIcon = document.getElementById("arrowIconMobile");
  if (mobileDropdownContent.style.display === "block") {
    mobileDropdownContent.style.display = "none";
    arrowIcon.classList.remove("rotate");
  } else {
    mobileDropdownContent.style.display = "block";
    arrowIcon.classList.add("rotate");
  }
 
}; 
