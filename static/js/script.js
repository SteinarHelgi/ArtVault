function showLoader() {
    const loader = document.getElementById("page-loader");
      if (!form.checkValidity()) {
      return;
      }
    if (loader) {
        loader.style.display = "flex";
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const links = document.querySelectorAll("a");
    const forms = document.querySelectorAll("form");
    const buttons = document.querySelectorAll("button");

    links.forEach(function (link) {
        link.addEventListener("click", function () {
            const href = link.getAttribute("href");

            if (href && href !== "#" && !href.startsWith("javascript")) {
                showLoader();
            }
        });
    });

    forms.forEach(function (form) {
        form.addEventListener("submit", function () {
            showLoader();
        });
    });

    buttons.forEach(function (button) {
        button.addEventListener("click", function () {
            if (button.type === "submit") {
                showLoader();
            }
        });
    });
});

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
      const file = event.target.files[0];

      if (file) {
          const imageURL = URL.createObjectURL(file);

          const uploadBox = document.querySelector(".seller-logo-box");
          const uploadIcon = document.querySelector(".logo-upload-icon");

          if (uploadBox) {
              uploadBox.style.backgroundImage = `url('${imageURL}')`;
              uploadBox.style.backgroundSize = "cover";
              uploadBox.style.backgroundPosition = "center";
          }

          if (uploadIcon) {
              uploadIcon.style.display = "none";
          }

          const preview = document.querySelector("#seller-logo-preview");

          if (preview) {
              preview.src = imageURL;
          }
      }
  };

   window.previewCover = function(event) {
      const file = event.target.files[0];

      if (file) {
          const imageURL = URL.createObjectURL(file);

          const uploadBox = document.querySelector(".seller-logo-box");
          const uploadIcon = document.querySelector(".cover-upload-icon");

          if (uploadBox) {
              uploadBox.style.backgroundImage = `url('${imageURL}')`;
              uploadBox.style.backgroundSize = "cover";
              uploadBox.style.backgroundPosition = "center";
          }

          if (uploadIcon) {
              uploadIcon.style.display = "none";
          }

          const preview = document.querySelector("#seller-cover-preview");

          if (preview) {
              preview.src = imageURL;
          }
      }
  };
   

//price slider

const rangeInput = document.querySelectorAll(".range-input input"),
  priceInput = document.querySelectorAll(".price-input input"),
  range = document.querySelector(".slider .progress");
let priceGap = 1000;

priceInput.forEach((input) => {
  input.addEventListener("input", (e) => {
    let minPrice = parseInt(priceInput[0].value),
      maxPrice = parseInt(priceInput[1].value);

    if (maxPrice - minPrice >= priceGap && maxPrice <= rangeInput[1].max) {
      if (e.target.className === "input-min") {
        rangeInput[0].value = minPrice;
        range.style.left = (minPrice / rangeInput[0].max) * 100 + "%";
      } else {
        rangeInput[1].value = maxPrice;
        range.style.right = 100 - (maxPrice / rangeInput[1].max) * 100 + "%";
      }
    }
  });
});

rangeInput.forEach((input) => {
  input.addEventListener("input", (e) => {
    let minVal = parseInt(rangeInput[0].value),
      maxVal = parseInt(rangeInput[1].value);

    if (maxVal - minVal < priceGap) {
      if (e.target.className === "range-min") {
        rangeInput[0].value = maxVal - priceGap;
      } else {
        rangeInput[1].value = minVal + priceGap;
      }
    } else {
      priceInput[0].value = minVal;
      priceInput[1].value = maxVal;
      range.style.left = (minVal / rangeInput[0].max) * 100 + "%";
      range.style.right = 100 - (maxVal / rangeInput[1].max) * 100 + "%";
    }
  });
});

let minVal = parseInt(rangeInput[0].value);
let maxVal = parseInt(rangeInput[1].value);

range.style.left = (minVal / rangeInput[0].max) * 100 + "%";
range.style.right = 100 - (maxVal / rangeInput[1].max) * 100 + "%";

//silde menu browes artwork
function openFilter() {
    document.getElementById("filterSidebar").classList.add("show");
    document.getElementById("filterOverlay").classList.add("show");
}

function closeFilter() {
    document.getElementById("filterSidebar").classList.remove("show");
    document.getElementById("filterOverlay").classList.remove("show");
}

//big images artwork_details
function openImagePopup(src) {
    const popup = document.getElementById("imagePopup");
    const popupImage = document.getElementById("popupImage");

    popup.style.display = "flex";
    popupImage.src = src;
}

function closeImagePopup() {
    const popup = document.getElementById("imagePopup");
    popup.style.display = "none";
}



