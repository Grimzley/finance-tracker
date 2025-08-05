document.addEventListener('DOMContentLoaded', function () {
  const formOne = document.getElementById("form-one");
  const formTwo = document.getElementById("form-two");

  document.querySelectorAll('.show-form-one').forEach(button => {
      button.addEventListener('click', function(e) {
        formOne.classList.remove("d-none");
        formTwo.classList.add("d-none");
      });
  });

  document.querySelectorAll('.show-form-two').forEach(button => {
      button.addEventListener('click', function(e) {
        formTwo.classList.remove("d-none");
        formOne.classList.add("d-none");
      });
  });
})
