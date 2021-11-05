// flash messages
let alertWrapper = document.querySelector(".alert");
let alertClose = document.querySelector(".alert__close");

if (alertWrapper) {
  alertClose.addEventListener("click", function () {
    alertWrapper.classList.add("hidden");
  });
}

//pagination and search

const searchForm = document.querySelector("#searchForm");
const pageLinks = document.querySelectorAll(".page-link");

if (searchForm) {
  for (let link of pageLinks) {
    link.addEventListener("click", function (e) {
      e.preventDefault();

      let page = this.dataset.page;

      searchForm.innerHTML += `<input type='number' value=${page} name='page' hidden>`;
      searchForm.submit();
    });
  }
}
