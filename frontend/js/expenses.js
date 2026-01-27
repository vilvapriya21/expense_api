const API_BASE_URL = "http://127.0.0.1:8000";

const token = localStorage.getItem("access_token");
const expensesList = document.getElementById("expensesList");
const expenseForm = document.getElementById("expenseForm");
const expenseMessage = document.getElementById("expenseMessage");

let currentEditId = null;

const editModal = document.getElementById("editModal");
const editAmount = document.getElementById("editAmount");
const editCategory = document.getElementById("editCategory");
const editDescription = document.getElementById("editDescription");

const saveEditBtn = document.getElementById("saveEditBtn");
const cancelEditBtn = document.getElementById("cancelEditBtn");


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

            li.innerHTML = `
                <div>
                    <strong>${exp.category}</strong> - ₹${exp.amount}
                    <br />
                    <small>${exp.description || "No description"}</small>
                    <br />
                    <small>📅 ${exp.expense_date}</small>
                </div>
                <div class="actions-inline">
                    <button onclick="openEditModal(
                        ${exp.id},
                        ${exp.amount},
                        '${exp.category.replace(/'/g, "\\'")}',
                        '${(exp.description || "").replace(/'/g, "\\'")}'
                    )">Edit</button>
                    <button onclick="deleteExpense(${exp.id})" class="secondary">Delete</button>
                </div>
            `;

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
    const expenseDate = document.getElementById("expenseDate").value;

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
                expense_date: expenseDate || null
            }),
        });

        if (!res.ok) throw new Error("Failed to add expense");

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


// ------------------ EDIT MODAL ------------------
function openEditModal(id, amount, category, description) {
    currentEditId = id;

    editAmount.value = amount;
    editCategory.value = category;
    editDescription.value = description;

    editModal.classList.add("show");
}


// Cancel edit
cancelEditBtn?.addEventListener("click", () => {
    editModal.classList.remove("show");

    currentEditId = null;
    editAmount.value = "";
    editCategory.value = "";
    editDescription.value = "";
});


// Save edit
saveEditBtn?.addEventListener("click", async () => {
    if (
        !currentEditId ||
        !editAmount.value ||
        !editCategory.value
    ) {
        alert("Amount and category are required");
        return;
    }

    try {
        const res = await fetch(`${API_BASE_URL}/expenses/${currentEditId}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({
                amount: editAmount.value,
                category: editCategory.value,
                description: editDescription.value,
            }),
        });

        if (!res.ok) throw new Error("Update failed");

        editModal.classList.remove("show");
        currentEditId = null;
        loadExpenses();

    } catch (err) {
        alert("Failed to update expense");
        console.error(err);
    }
});


// Close modal when clicking outside
editModal?.addEventListener("click", (e) => {
    if (e.target === editModal) {
        editModal.classList.remove("show");
        currentEditId = null;
    }
});


// ------------------ DELETE EXPENSE ------------------
async function deleteExpense(id) {
    if (!confirm("Delete this expense?")) return;

    try {
        const res = await fetch(`${API_BASE_URL}/expenses/${id}`, {
            method: "DELETE",
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });

        if (!res.ok) throw new Error("Delete failed");

        loadExpenses();

    } catch (err) {
        alert("Failed to delete expense");
        console.error(err);
    }
}


// Load expenses on page load
loadExpenses();