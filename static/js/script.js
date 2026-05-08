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
    const container = wrapper.querySelector(".gallery-scroll-container");

    container.scrollBy({
        left: direction * 300,
        behavior: "smooth"
    });
}

//Image preview
window.previewBuyerProfileImage = function(event) {
    const uploadBox = document.querySelector(".buyer-upload-box");
    const previewIcon = document.querySelector("#buyer-profile-preview");

    const file = event.target.files[0];

    if (file) {
        const imageURL = URL.createObjectURL(file);

        uploadBox.style.backgroundImage = `url('${imageURL}')`;
        uploadBox.style.backgroundSize = "cover";
        uploadBox.style.backgroundPosition = "center";
        uploadBox.style.backgroundRepeat = "no-repeat";

        previewIcon.style.display = "none";
    }
};

  window.previewLogo = function(event) {
    const uploadBox = document.querySelector(".seller-logo-box");
    const uploadIcon = document.querySelector(".logo-upload-icon");

    const file = event.target.files[0];

    if (file) {
        const imageURL = URL.createObjectURL(file);

        uploadBox.style.backgroundImage = `url('${imageURL}')`;
        uploadBox.style.backgroundSize = "cover";
        uploadBox.style.backgroundPosition = "center";

        uploadIcon.style.display = "none";
    }
};

window.previewCover = function(event) {
    const uploadBox = document.querySelector(".seller-cover-box");
    const uploadIcon = document.querySelector(".cover-upload-icon");

    const file = event.target.files[0];

    if (file) {
        const imageURL = URL.createObjectURL(file);

        uploadBox.style.backgroundImage = `url('${imageURL}')`;
        uploadBox.style.backgroundSize = "cover";
        uploadBox.style.backgroundPosition = "center";

        uploadIcon.style.display = "none";
    }
};
