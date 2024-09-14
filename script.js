// Function to fetch all expenses from the server and display them
function fetchExpenses() {
    fetch('/expenses')
        .then(response => response.json())
        .then(data => {
            const expenseList = document.getElementById('expenseList');
            const totalExpense = document.getElementById('totalExpense');
            expenseList.innerHTML = '';
            totalExpense.innerText = data.total_expense.toFixed(2);

            // Loop through each expense and add to the DOM
            data.expenses.forEach(expense => {
                addExpenseToDOM(expense);
            });
        })
        .catch(error => console.error('Error fetching expenses:', error));
}

// Function to add an expense via API and update the view
function addExpense() {
    const description = document.getElementById('description').value;
    const amount = document.getElementById('amount').value;

    if (!description || !amount || isNaN(amount)) {
        alert('Please enter a valid description and amount.');
        return;
    }

    // Send POST request to add the new expense
    fetch('/expenses', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ description, amount }),
    })
    .then(response => response.json())
    .then(() => {
        fetchExpenses(); // Refresh expenses
    })
    .catch(error => console.error('Error adding expense:', error));
