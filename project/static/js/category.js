document.addEventListener('DOMContentLoaded', function () {
    const typeSelect = document.querySelector('#id_transaction_type');
    const categorySelect = document.querySelector('#id_category');

    const incomeCategories = {
        'salary': 'Salary',
        'freelance': 'Freelance',
        'investment': 'Investment',
        'gift': 'Gift',
        'inc_other': 'Other'
    };

    const expenseCategories = {
        'food': 'Food',
        'bills': 'Bills',
        'transport': 'Transportation',
        'health': 'Healthcare',
        'entertainment': 'Entertainment',
        'shopping': 'Shopping',
        'exp_other': 'Other'
    };

    function updateCategoryOptions(type) {
        const options = type === 'income' ? incomeCategories : expenseCategories;

        categorySelect.innerHTML = '';
        for (const [value, label] of Object.entries(options)) {
            const option = document.createElement('option');
            option.value = value;
            option.textContent = label;
            categorySelect.appendChild(option);
        }
    }

    if (typeSelect) {
        typeSelect.addEventListener('change', function () {
            updateCategoryOptions(this.value);
        });
        if (typeSelect.value) {
            updateCategoryOptions(typeSelect.value);
        }
    }
});
