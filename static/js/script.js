const loadingScreen = document.querySelector(".loadingScreen");

const showLoadingScreen = () => {
    loadingScreen?.classList.add("show");
};

const hideLoadingScreen = () => {
    loadingScreen?.classList.remove("show");
};

window.addEventListener("load", hideLoadingScreen);

window.addEventListener("pageshow", hideLoadingScreen);

document.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
        showLoadingScreen();
    });
});

document.querySelectorAll("form").forEach((form) => {
    form.addEventListener("submit", () => {
        showLoadingScreen();
    });
});

// dropdown
const toggleLeftDropdown = (event) => {
    event.stopPropagation();
    document.getElementById("leftDropdown")?.classList.toggle("show");
};

const toggleRightDropdown = (event) => {
    event.stopPropagation();
    document.getElementById("rightDropdown")?.classList.toggle("show");
};

window.addEventListener("click", (event) => {
    if (!event.target.closest(".dropdown")) {
        document.getElementById("leftDropdown")?.classList.remove("show");
    }

    if (!event.target.closest(".profile-dropdown")) {
        document.getElementById("rightDropdown")?.classList.remove("show");
    }
});

// close button popup
const closeModal = () => {
    document.getElementById("popupModal").style.display = "none";
};

// searchbar filtering for browse artwork
const filterFunction = () => {
    let input = document.getElementById("searchbar");
    let filter = input.value.toUpperCase();

    let cards = document.getElementsByClassName("art-card");

    for (let i = 0; i < cards.length; i++) {
        let cardText = cards[i].innerText.toUpperCase();

        if (cardText.indexOf(filter) > -1) {
            cards[i].style.display = "";
        } else {
            cards[i].style.display = "none";
        }
    }
};

// scroll func on landing page
const scrollArt = (button, direction) => {
    const wrapper = button.closest(".art-scroll-wrapper");
    const container = wrapper.querySelector(".gallery-scroll-container");

    container.scrollBy({
        left: direction * 300,
        behavior: "smooth"
    });
};

//preview of profile image for seller setup/edit
window.previewBuyerProfileImage = (event) => {
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

//preview of logo for seller setup/edit
window.previewLogo = (event) => {
    const file = event.target.files[0];

    if (file) {
        const imageURL = URL.createObjectURL(file);

        // for setup
        const uploadBox = document.querySelector(".seller-upload-box");
        const uploadIcon = document.querySelector(".logo-upload-icon");

        if (uploadBox) {
            uploadBox.style.backgroundImage = `url('${imageURL}')`;
            uploadBox.style.backgroundSize = "cover";
            uploadBox.style.backgroundPosition = "center";
        }

        // for edit
        if (uploadIcon) {
            uploadIcon.style.display = "none";
        }

        const preview = document.querySelector("#seller-logo-preview");

        if (preview) {
            preview.src = imageURL;
        }
    }
};

//preview of cover photo for seller setup/edit
window.previewCover = (event) => {
    const file = event.target.files[0];

    if (file) {
        const imageURL = URL.createObjectURL(file);

        // for setup
        const uploadBox = document.querySelector(".seller-cover-box");
        const uploadIcon = document.querySelector(".cover-upload-icon");

        if (uploadBox) {
            uploadBox.style.backgroundImage = `url('${imageURL}')`;
            uploadBox.style.backgroundSize = "cover";
            uploadBox.style.backgroundPosition = "center";
        }

        // for edit
        if (uploadIcon) {
            uploadIcon.style.display = "none";
        }

        const preview = document.querySelector("#seller-cover-preview");

        if (preview) {
            preview.src = imageURL;
        }
    }
};

// MM/YY card expirations
document.addEventListener("input", (event) => {
    if (!event.target.classList.contains("card-expiration-input")) return;

    let value = event.target.value.replace(/\D/g, "").slice(0, 4);

    if (value.length > 2) {
        value = value.slice(0, 2) + "/" + value.slice(2);
    }

    event.target.value = value;
});

// price slider
const rangeInput = document.querySelectorAll(".range-input input"),
    priceInput = document.querySelectorAll(".price-input input"),
    range = document.querySelector(".slider .progress");

if (rangeInput.length >= 2 && priceInput.length >= 2 && range) {
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
                    range.style.right =
                        100 - (maxPrice / rangeInput[1].max) * 100 + "%";
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
                range.style.right =
                    100 - (maxVal / rangeInput[1].max) * 100 + "%";
            }
        });
    });

    let minVal = parseInt(rangeInput[0].value);
    let maxVal = parseInt(rangeInput[1].value);

    range.style.left = (minVal / rangeInput[0].max) * 100 + "%";
    range.style.right =
        100 - (maxVal / rangeInput[1].max) * 100 + "%";
}

// slide menu browse artwork
const openFilter = () => {
    document.getElementById("filterSidebar").classList.add("show");
    document.getElementById("filterOverlay").classList.add("show");
};

const closeFilter = () => {
    document.getElementById("filterSidebar").classList.remove("show");
    document.getElementById("filterOverlay").classList.remove("show");
};

// big images artwork_details
const openImagePopup = (src) => {
    const popup = document.getElementById("imagePopup");
    const popupImage = document.getElementById("popupImage");

    popup.style.display = "flex";
    popupImage.src = src;
};


const closeImagePopup = () => {
    const popup = document.getElementById("imagePopup");
    popup.style.display = "none";
};




