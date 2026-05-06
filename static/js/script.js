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
});

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

//scroll func on landing page
function scrollArt(button, direction) {
    const wrapper = button.closest(".art-scroll-wrapper");
    const container = wrapper.querySelector(".art-movement-container");

    container.scrollBy({
        left: direction * 300,
        behavior: "smooth"
    });
}