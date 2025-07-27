const formOne = document.getElementById("form-one");
const formTwo = document.getElementById("form-two");
const showFormOneBtn = document.getElementById("show-form-one");
const showFormTwoBtn = document.getElementById("show-form-two");

showFormOneBtn.onclick = () => {
  formOne.classList.remove("hidden");
  formTwo.classList.add("hidden");
};
showFormTwoBtn.onclick = () => {
  formTwo.classList.remove("hidden");
  formOne.classList.add("hidden");
};
