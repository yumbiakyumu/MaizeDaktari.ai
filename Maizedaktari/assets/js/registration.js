document.getElementById("registration-form").addEventListener("submit", function(event) {
    event.preventDefault();

    // Get form values
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    // Simulate registration process (store user data in local storage)
    const users = JSON.parse(localStorage.getItem("users")) || [];
    const existingUser = users.find(user => user.username === username);
    if (existingUser) {
        alert("Username already exists. Please choose a different username.");
        return;
    }

    // Add new user
    users.push({ username, password });
    localStorage.setItem("users", JSON.stringify(users));

    // Redirect to login page
    window.location.href = "login.html";
});