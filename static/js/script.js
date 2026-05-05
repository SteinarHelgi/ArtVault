//dropdown menu
const leftDropdown = () => {
  document.getElementById("leftDropdown").classList.toggle("show");
};

const rightDropdown = () => {
  document.getElementById("rightDropdown").classList.toggle("show");
};

window.onclick = (event) => {
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