const API_BASE_URL = "http://127.0.0.1:8000";

const token = localStorage.getItem("access_token");
const expensesList = document.getElementById("expensesList");
const expenseForm = document.getElementById("expenseForm");
const expenseMessage = document.getElementById("expenseMessage");

// ------------------ LOAD EXPENSES ------------------
async function loadExpenses() {
    try {
        const res = await fetch(`${API_BASE_URL}/expenses/`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });

        if (!res.ok) throw new Error("Failed to fetch expenses");

        const expenses = await res.json();
        expensesList.innerHTML = "";

        if (expenses.length === 0) {
            expensesList.innerHTML = "<li>No expenses found</li>";
            return;
        }

        expenses.forEach(exp => {
            const li = document.createElement("li");
            li.textContent = `${exp.category} - ₹${exp.amount} (${exp.description || "No description"})`;
            expensesList.appendChild(li);
        });

    } catch (err) {
        console.error(err);
        expensesList.innerHTML = "<li>Error loading expenses</li>";
    }
}

// ------------------ ADD EXPENSE ------------------
expenseForm?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const amount = document.getElementById("amount").value;
    const category = document.getElementById("category").value;
    const description = document.getElementById("description").value;

    try {
        const res = await fetch(`${API_BASE_URL}/expenses/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({
                amount,
                category,
                description,
            }),
        });

        if (!res.ok) {
            throw new Error("Failed to add expense");
        }

        expenseMessage.style.color = "green";
        expenseMessage.textContent = "Expense added successfully";

        expenseForm.reset();
        loadExpenses();

    } catch (err) {
        expenseMessage.style.color = "red";
        expenseMessage.textContent = "Error adding expense";
        console.error(err);
    }
});

// Load expenses on page load
loadExpenses();