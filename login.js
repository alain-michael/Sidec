/* Javascript for login form toggling */

const container = document.querySelector(".container");
const pwShowHide = document.querySelectorAll(".showHidePw");
const pwFields = document.querySelectorAll(".password");
const signUp = document.querySelector(".signup-link"); // Use querySelector to select the first matching element
const login = document.querySelector(".login-link"); // Use querySelector to select the first matching element

// Js code to show/hide password and change icon //
pwShowHide.forEach(eyeIcon => {
    eyeIcon.addEventListener("click", () => {
        pwFields.forEach(pwField => {
            if (pwField.type === "password") {
                pwField.type = "text";
                pwShowHide.forEach(icon => {
                    icon.classList.replace("fa-eye-slash", "fa-eye");
                });
            } else {
                pwField.type = "password";
                pwShowHide.forEach(icon => {
                    icon.classList.replace("fa-eye", "fa-eye-slash");
                });
            }
        });
    });
});

// Js code to toggle between Login and Signup forms
signUp.addEventListener("click", () => {
    container.classList.add("active");
});

login.addEventListener("click", () => {
    container.classList.remove("active");
});