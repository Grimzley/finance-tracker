document.addEventListener('DOMContentLoaded', function () {
    const typeSelect = document.querySelector('#id_transaction_type');
    const categorySelect = document.querySelector('#id_category');

    const modal = new bootstrap.Modal(document.getElementById('transaction-modal'));
    const modalTitle = document.getElementById('modal-label');
    const transactionForm = document.getElementById('transaction-form');
    const deleteForm = document.getElementById('delete-form');
    const addBtn = document.getElementById('add-button');
    const submitBtn = document.getElementById('submit-button');
    const deleteBtn = document.getElementById('delete-button');

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
        'shopping': 'Shopping',
        'entertainment': 'Entertainment',
        'health': 'Healthcare',
        'savings': 'Savings',
        'exp_other': 'Other'
    };
    function updateCategoryOptions(type, category = '') {
        categorySelect.innerHTML = '';

        const placeholder = document.createElement('option');
        placeholder.value = '';
        placeholder.textContent = type ? 'Select a category' : 'Select transaction type first';
        placeholder.disabled = true;
        placeholder.selected = !category;
        categorySelect.appendChild(placeholder);

        if (!type) return;

        const options = type === 'income' ? incomeCategories : expenseCategories;

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
        updateCategoryOptions(typeSelect.value);
    }

    // Add Button
    if (addBtn) {
        addBtn.addEventListener('click', function () {
            const createUrl = this.dataset.createUrl;

            transactionForm.action = createUrl;

            modalTitle.textContent = 'Add Transaction';
            submitBtn.textContent = 'Add';
            deleteBtn.classList.add('d-none');
            
            transactionForm.reset();
            modal.show();
        });
    }

    // Edit/Delete Button
    document.querySelectorAll('.edit-button').forEach(button => {
        button.addEventListener('click', function () {
            const title = this.dataset.title;
            const amount = this.dataset.amount;
            const type = this.dataset.transactionType;
            const category = this.dataset.category;

            const editUrl = this.dataset.editUrl;
            const deleteUrl = this.dataset.deleteUrl;
            transactionForm.action = editUrl;
            deleteForm.action = deleteUrl

            modalTitle.textContent = 'Edit Transaction';
            submitBtn.textContent = 'Update';
            deleteBtn.classList.remove('d-none');

            transactionForm.querySelector('#id_title').value = title;
            transactionForm.querySelector('#id_amount').value = amount;
            transactionForm.querySelector('#id_transaction_type').value = type;
            updateCategoryOptions(type, category);
            transactionForm.querySelector('#id_category').value = category;
        });
    });
});
