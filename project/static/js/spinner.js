document.addEventListener('DOMContentLoaded', function () {
    const loadingSpinner = document.getElementById("loading-spinner");
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function () {
            loadingSpinner.classList.remove("hidden")
        });
    });
})
