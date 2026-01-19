const API_BASE_URL = "http://127.0.0.1:8000";

document.getElementById("registerForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const message = document.getElementById("message");

    message.textContent = "";
    message.style.color = "red";

    try {
        const response = await fetch(`${API_BASE_URL}/users/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (!response.ok) {
            message.textContent = data.detail || "Registration failed";
            return;
        }

        message.style.color = "green";
        message.textContent = "Registration successful! Redirecting to login...";

        setTimeout(() => {
            window.location.href = "index.html";
        }, 1000);

    } catch (error) {
        console.error(error);
        message.textContent = "Server error";
    }
});