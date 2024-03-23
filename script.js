// Фильтр
document
  .getElementById("complete-checkbox")
  .addEventListener("change", function () {
    const completeElements = document.querySelectorAll(".complete");

    completeElements.forEach(function (element) {
      if (this.checked) {
        element.classList.add("shown");
      } else {
        element.classList.remove("shown");
      }
    }, this);
  });

document.getElementById("bad-checkbox").addEventListener("change", function () {
  const badElements = document.querySelectorAll(".bad");

  badElements.forEach(function (element) {
    if (this.checked) {
      element.classList.add("shown");
    } else {
      element.classList.remove("shown");
    }
  }, this);
});

document
  .getElementById("wait-checkbox")
  .addEventListener("change", function () {
    const badElements = document.querySelectorAll(".wait");

    badElements.forEach(function (element) {
      if (this.checked) {
        element.classList.add("shown");
      } else {
        element.classList.remove("shown");
      }
    }, this);
  });

// Фильтр very mini
document
  .getElementById("complete-checkbox-very-mini")
  .addEventListener("change", function () {
    const completeElements = document.querySelectorAll(".complete");

    completeElements.forEach(function (element) {
      if (this.checked) {
        element.classList.add("shown");
      } else {
        element.classList.remove("shown");
      }
    }, this);
  });

document
  .getElementById("bad-checkbox-very-mini")
  .addEventListener("change", function () {
    const badElements = document.querySelectorAll(".bad");

    badElements.forEach(function (element) {
      if (this.checked) {
        element.classList.add("shown");
      } else {
        element.classList.remove("shown");
      }
    }, this);
  });

document
  .getElementById("wait-checkbox-very-mini")
  .addEventListener("change", function () {
    const badElements = document.querySelectorAll(".wait");

    badElements.forEach(function (element) {
      if (this.checked) {
        element.classList.add("shown");
      } else {
        element.classList.remove("shown");
      }
    }, this);
  });
// Фильтр mini
document
  .getElementById("complete-checkbox-mini")
  .addEventListener("change", function () {
    const completeElements = document.querySelectorAll(".complete");

    completeElements.forEach(function (element) {
      if (this.checked) {
        element.classList.add("shown");
      } else {
        element.classList.remove("shown");
      }
    }, this);
  });

document
  .getElementById("bad-checkbox-mini")
  .addEventListener("change", function () {
    const badElements = document.querySelectorAll(".bad");

    badElements.forEach(function (element) {
      if (this.checked) {
        element.classList.add("shown");
      } else {
        element.classList.remove("shown");
      }
    }, this);
  });

document
  .getElementById("wait-checkbox-mini")
  .addEventListener("change", function () {
    const badElements = document.querySelectorAll(".wait");

    badElements.forEach(function (element) {
      if (this.checked) {
        element.classList.add("shown");
      } else {
        element.classList.remove("shown");
      }
    }, this);
  });

// Открытие inProcess
window.onload = function () {
  var detailsElements = document.querySelectorAll("details");

  detailsElements.forEach(function (details) {
    var summary = details.querySelector("summary.inProcess");
    if (summary) {
      details.open = true;
    }
  });
};

// Menu
document.getElementById("menuButton").addEventListener("click", function () {
  document.getElementById("menu").classList.toggle("open");
});
