// dashboard.js

document.addEventListener("DOMContentLoaded", () => {
    const API_BASE_URL = "http://127.0.0.1:8000";

    const token = localStorage.getItem("access_token");
    const welcomeEl = document.getElementById("welcome");
    const logoutBtn = document.getElementById("logoutBtn");

    // 1. Protect dashboard
    if (!token) {
        window.location.href = "index.html";
        return;
    }

    // 2. Validate token and load user
    fetch(`${API_BASE_URL}/users/me`, {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    })
        .then((res) => {
            if (!res.ok) {
                throw new Error("Unauthorized");
            }
            return res.json();
        })
        .then((user) => {
            if (welcomeEl) {
                welcomeEl.textContent = `Welcome, ${user.username}!`;
            }
        })
        .catch((error) => {
            console.error("Auth error:", error);
            localStorage.removeItem("access_token");
            window.location.href = "index.html";
        });

    // 3. Logout
    if (logoutBtn) {
        logoutBtn.addEventListener("click", () => {
            localStorage.removeItem("access_token");
            window.location.href = "index.html";
        });
    }
});