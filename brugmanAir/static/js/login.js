const btn = document.querySelector(".btn");
const btnAfter = document.querySelector(".btn-after");

const eyeIcons = document.querySelectorAll(".eye-icon");

btn.addEventListener("mouseover", (e) => {
  btnAfter.classList.remove("to-left");
  btnAfter.classList.add("to-right");
});

btn.addEventListener("mouseleave", (e) => {
  btnAfter.classList.remove("to-right");
  btnAfter.classList.add("to-left");
});

eyeIcons.forEach((e) => {
  e.addEventListener("click", (el) => {
    const input = el.target.parentElement.firstElementChild;
    const eyeIconText = el.target.innerText;
    if (eyeIconText == "visibility_off") {
      el.target.innerText = "visibility";
      input.type = "text";
    } else {
      el.target.innerText = "visibility_off";
      input.type = "password";
    }
  });
});
