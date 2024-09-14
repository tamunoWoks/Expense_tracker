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
