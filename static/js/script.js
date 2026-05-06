function toggleLeftDropdown(event) {
    event.stopPropagation();
    document.getElementById("leftDropdown")?.classList.toggle("show");
}

function toggleRightDropdown(event) {
    event.stopPropagation();
    document.getElementById("rightDropdown")?.classList.toggle("show");
}

window.addEventListener("click", function (event) {
    if (!event.target.closest(".dropdown")) {
        document.getElementById("leftDropdown")?.classList.remove("show");
    }

  if (!event.target.closest(".profile-dropdown")) {
    document.getElementById("rightDropdown")?.classList.remove("show");
  }
};

  // close button á popup
  function closeModal() {
    document.getElementById("popupModal").style.display = "none";
  }


