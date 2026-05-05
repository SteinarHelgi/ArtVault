//dropdown menu
const MyDropdown = () => {
  document.getElementById("myDropdown").classList.toggle("show");
};

window.onclick = (event) => {
  if (!event.target.closest(".dropdown")) {
    document.getElementById("myDropdown").classList.remove("show");
  }
};

  // close button á popup
  function closeModal() {
    document.getElementById("popupModal").style.display = "none";
  }