document.getElementById("login-form").addEventListener("submit", function(event) {
    event.preventDefault();

    // Get form values
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    // Simulate login process (validate credentials from local storage)
    const users = JSON.parse(localStorage.getItem("users")) || [];
    const user = users.find(user => user.username === username && user.password === password);
    if (!user) {
        alert("Invalid username or password. Please try again.");
        return;
    }

    // Redirect to homepage (or any other authenticated page)
    window.location.href = "index.html"; // Change this to the appropriate page
});