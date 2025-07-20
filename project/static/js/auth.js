const form = document.getElementById("form");
const spinner = document.getElementById("spinner");

form.addEventListener('submit', (e) => {
  spinner.classList.remove("hidden")
})
