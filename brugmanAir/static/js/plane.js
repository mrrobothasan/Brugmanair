const planeSec = document.querySelector(".plane-sec");
const planeToAdmin = document.querySelector(".plane-to-admin");

const fly = setTimeout(() => {
  planeSec.classList.add("active");
}, 2000);
const land = setTimeout(() => {
  planeSec.classList.remove("active");
}, 4000);
const end = setTimeout(() => {
  planeSec.classList.add("runway-margin");
}, 7000);
const hidePlane = setTimeout(() => {
  planeToAdmin.classList.add("go-to-admin");
}, 8000);
