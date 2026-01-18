const API_BASE_URL = "http://127.0.0.1:8000";

document.getElementById("loginForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const message = document.getElementById("message");

    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: new URLSearchParams({
                username: username,
                password: password
            })
        });

        const data = await response.json();

        if (!response.ok) {
            message.textContent = data.detail || "Login failed";
            return;
        }

        // ✅ Save JWT token using the same key as dashboard.js expects
        localStorage.setItem("access_token", data.access_token);

        // Redirect to dashboard
        window.location.href = "dashboard.html";

    } catch (error) {
        message.textContent = "Server error";
        console.error(error);
    }
});