document.addEventListener("DOMContentLoaded", () => {
  const savedTheme = localStorage.getItem("theme");
  if (savedTheme === "dark") {
    document.body.classList.add("dark");
  }
});

const toggleThemeBtn = document.getElementById("toggle-theme");

toggleThemeBtn.onclick = () => {
  document.body.classList.toggle("dark");
  const theme = document.body.classList.contains("dark") ? "dark": "light";
  localStorage.setItem("theme", theme);
};