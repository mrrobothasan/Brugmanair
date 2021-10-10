const profileBtn = document.querySelector(".user-profile");
const profileSettings = document.querySelector(".profile-settings");
const body = document.querySelector(".home");

const sideNavBtn = document.querySelector(".menu-icon");
const sideNav = document.querySelector(".side-nav");
const main = document.querySelector("main");

const fullIcon = document.querySelectorAll(".full-icon");
const tableSec = document.querySelector(".table-con");

const checkAll = document.querySelectorAll(".check-all");

const refreshIcon = document.querySelectorAll(".refresh-icon");

const alertMsg = document.querySelector(".alert");
const sideLinks = document.querySelectorAll(".side-link");

const btn = document.querySelector(".btn");
const btnAfter = document.querySelector(".btn-after");

const eyeIcons = document.querySelectorAll(".eye-icon");
const expandIcons = document.querySelectorAll(".expand-icon");

const pathArray = window.location.pathname.split("/");

profileBtn.addEventListener("click", (e) => {
  profileSettings.classList.toggle("show-profile");
});

if (body) {
  body.addEventListener("click", (e) => {
    if (e.target != profileBtn) {
      if (profileSettings.classList.contains("show-profile")) {
        profileSettings.classList.remove("show-profile");
      }
    }
  });
}

sideNavBtn.addEventListener("click", (e) => {
  sideNav.classList.toggle("hide");
  main.classList.toggle("no-margin");
  sideNavBtn.classList.toggle("open");
});

if (fullIcon) {
  fullIcon.forEach((e) => {
    e.addEventListener("click", (el) => {
      const fullIconTarget = el.target;
      let fullIconVal = fullIconTarget.innerText;
      if (fullIconVal == "fullscreen") {
        fullIconTarget.innerHTML = "fullscreen_exit";
      } else {
        fullIconTarget.innerHTML = "fullscreen";
      }

      const tableContainer =
        fullIconTarget.parentElement.parentElement.parentElement;
      const table =
        fullIconTarget.parentElement.parentElement.nextElementSibling;

      if (table.classList.contains("hide-table")) {
        table.classList.remove("hide-table");
      }

      tableContainer.classList.toggle("full-table");
    });
  });
}

if (checkAll) {
  checkAll.forEach((e) => {
    e.addEventListener("click", (el) => {
      const checkbox = el.target;
      const parent =
        checkbox.parentElement.parentElement.parentElement.nextElementSibling;
      const allCheckBoxes = parent.children;
      for (let tr of allCheckBoxes) {
        const input =
          tr.firstChild.nextElementSibling.firstChild.nextElementSibling;
        if (checkbox.checked) {
          if (!input.checked) {
            input.checked = true;
          }
        } else {
          input.checked = false;
        }
      }
    });
  });
}

setTimeout((e) => {
  if (alertMsg) {
    alertMsg.style.display = "none";
  }
}, 3000);

if (btn) {
  btn.addEventListener("mouseover", (e) => {
    btnAfter.classList.remove("to-left");
    btnAfter.classList.add("to-right");
  });

  btn.addEventListener("mouseleave", (e) => {
    btnAfter.classList.remove("to-right");
    btnAfter.classList.add("to-left");
  });
}

const datumInput = document.getElementById("datum");
const datumLabel = document.getElementById("datum-label");

if (datumInput) {
  datumInput.addEventListener("change", (e) => {
    datumLabel.classList.add("active-datum-label");
  });
}

const selected = document.querySelectorAll(".selected");
const optionsContainerClose = document.querySelectorAll(".options-con");
const optionList = document.querySelectorAll(".option");

selected.forEach((e) => {
  e.addEventListener("click", (el) => {
    const selectedTarget = el.target;
    const optionsContainer = selectedTarget.previousElementSibling;

    selectedTarget.classList.toggle("active");
    optionsContainer.classList.toggle("active");
  });
});

const optionListFun = (list) => {
  list.forEach((e) => {
    e.addEventListener("click", (el) => {
      const optionTarget = el.target;
      const optionsContainer = optionTarget.parentElement;
      const selectedValue = optionTarget.parentElement.nextElementSibling;
      let optionTargetValue = optionTarget.lastElementChild.innerHTML;

      selectedValue.innerHTML = optionTargetValue;

      optionsContainer.classList.remove("active");
      selectedValue.classList.remove("active");
    });
  });
};

optionListFun(optionList);

const checkInput = (el, text) => {
  const inputText = $(el).text();
  if ($.trim(inputText) == text) {
    $(el).css("border-color", "red");
    return null;
  } else {
    return $.trim(inputText);
  }
};

const checkTextInput = (el, text, elType) => {
  if ($(el).val() == text) {
    if (elType == "normal") {
      $(el).next().css("border-color", "red");
      return null;
    } else {
      $(el).next().next().css("border-color", "red");
      return null;
    }
  } else {
    return $(el).val();
  }
};
const showError = (err, msg) => {
  const errText = document.querySelector(".err-text");
  errText.innerHTML = err;
  alertMsg.classList.add(msg);
  $(".alert").css("opacity", "1");
  $(".alert").css("display", "flex");

  setTimeout(() => {
    $(".alert").css("display", "none");
  }, 3000);
};
const submit = (url, event) => {
  const datum = checkTextInput("#datum", "");
  const vertrektijd = checkTextInput("#vertrektijd", "", "normal");
  const aankomsttijd = checkTextInput("#aankomsttijd", "", "normal");
  const prijs = checkTextInput("#prijs", "", "normal");

  const vliegtuig = checkInput(".vli-selected", "Selecteer een Vliegtuig");
  const vertrek = checkInput(
    "#vertrek-selected",
    "Selecteer een vertrek locatie"
  );
  const bestemming = checkInput(".best-selected", "Selecteer een bestemming");
  const pilo1 = checkInput(".pil1-selected", "Selecteer een piloot");
  const co_pil = checkInput(".co-pil-selected", "Selecteer een Co-piloot");
  const stew1 = checkInput(".ste1-selected", "Selecteer een steward");
  const stew2 = checkInput(".ste2-selected", "Selecteer een steward");

  if (
    datum &&
    vertrek &&
    bestemming &&
    vertrektijd &&
    aankomsttijd &&
    prijs &&
    vliegtuig &&
    pilo1 &&
    co_pil &&
    stew1 &&
    stew2 != null
  ) {
    const flight = {
      datum: datum,
      vliegtuig: vliegtuig,
      vertrek: vertrek,
      bestemming: bestemming,
      vertrektijd: vertrektijd,
      aankomsttijd: aankomsttijd,
      pilo1: pilo1,
      co_pil: co_pil,
      stew1: stew1,
      stew2: stew2,
      prijs: prijs,
    };
    if (vertrek === bestemming) {
      showError("Kies verschillende locaties", "danger");
      event.preventDefault();
      return;
    }
    if (stew1 === stew2) {
      showError("Kies verschillende stewards", "danger");
      event.preventDefault();
      return;
    }
    fetch(`${window.origin}/${url}`, {
      method: "POST",
      credentials: "include",
      body: JSON.stringify(flight),
      cache: "no-cache",
      headers: new Headers({
        "content-type": "application/json",
      }),
    }).then(function (response) {
      if (response.status !== 200) {
        console.log(`response was not 200: ${response.status}`);
        return;
      }

      response.json.then(function (data) {
        console.log(data);
      });
    });
  }
};
$("#submit-btn-new-flight").click((e) => {
  submit("new-flight", e);
});
$("#submit-btn-edit-flight").click((e) => {
  submit(`edit-flight/flight/${pathArray[2]}`);
});

sideLinks.forEach((e) => {
  if (e.getAttribute("data-link") == pathArray[1]) {
    e.classList.add("active");
  }
});

$(".best-selected").change(() => {
  console.log("yes");
});
