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


  // searchbar filtering fyrir browse artwork
function filterFunction() {
    let input = document.getElementById("searchbar");
    let filter = input.value.toUpperCase();

    let cards = document.getElementsByClassName("browse-art-link");

    for (let i = 0; i < cards.length; i++) {
        let cardText = cards[i].innerText.toUpperCase();

        if (cardText.indexOf(filter) > -1) {
            cards[i].style.display = "";
        } else {
            cards[i].style.display = "none";
        }
    }
}