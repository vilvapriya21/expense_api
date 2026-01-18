document.getElementById("registerForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const message = document.getElementById("message");

    try {
        const response = await fetch(`${API_BASE_URL}/users/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (!response.ok) {
            message.style.color = "red";
            message.textContent = data.detail || "Registration failed";
            return;
        }

        message.style.color = "green";
        message.textContent = "Registration successful! Redirecting to login...";

        // redirect after slight delay
        setTimeout(() => {
            window.location.href = "index.html";
        }, 1000);

    } catch (error) {
        message.style.color = "red";
        message.textContent = "Server error";
        console.error(error);
    }

    return false; // prevent default form behavior
});