document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector('form');
    form.addEventListener('submit', function (event) {
        let username = document.querySelector('#username').value;
        let password = document.querySelector('#password').value;

        if (username === "" || password === "") {
            alert("Please fill out both fields.");
            event.preventDefault();
        }
    });
});
