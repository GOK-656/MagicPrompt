// delete images on error
// const images = document.querySelectorAll("img");

// images.forEach(function (image) {
//     image.addEventListener("error", function () {
//         console.error("Image load error:", image.src);
//         console.log("404 image:", image.src);
//         const parentElement = image.parentElement;
//         if (parentElement) {
//             console.log("parentElement:", parentElement);
//             parentElement.remove();
//             console.log("image removed");
//         }
//     });
// });
// function imgError(img) {
//     console.log("Image error:", img.src);
//     const parentElement = img.parentElement;
//     if (parentElement) {
//         console.log("parentElement:", parentElement);
//         parentElement.remove();
//         console.log("image removed");
//     }
// }

// multiselect dropdown
const myForm = document.getElementById("myForm");

$(".ui.multiple.selection.dropdown").dropdown({
    action: "activate",
    onChange: function (value, text, $selectedItem) {
        console.log(value);
        myForm.submit();
    },
});

// switch filter dropdown on
const filterSwitch = document.getElementById("icon-filter");
const filterContent = document.getElementById("multiselect-wrapper");
if (filterSwitch) {
    filterSwitch.addEventListener("click", function () {
        const wrapper = this.closest("#search-bar");
        wrapper.classList.toggle("open");
    });
}

// copy to clipboard
const copyButtons = document.querySelectorAll(".pick-this");
copyButtons.forEach(function (button) {
    button.addEventListener("click", function () {
        console.log("copy button clicked");
        const text =
            this.parentNode.parentNode.querySelector(
                ".prompt-text-p"
            ).textContent;
        navigator.clipboard.writeText(text).then(
            () => {
                console.log("Copied to clipboard:", text);
                this.classList.add("copied");
                setTimeout(() => {
                    this.classList.remove("copied");
                }, 200);
            },
            function (err) {
                console.error("Async: Could not copy text: ", err);
            }
        );
    });
});

function submit_index_form(action) {
    document.getElementById("indexForm").action = action;
    document.getElementById("indexForm").submit();
}

function button2loading(button) {
    const loadingSpan = document.createElement("span");
    loadingSpan.classList.add("loading", "loading-spinner");
    button.innerHTML = "";
    button.appendChild(loadingSpan);
    button.disabled = true;
    var form = button.closest("form");
    setTimeout(() => {
        form.submit();
    }, 1000);
}

function button2pix2pix(button) {
    const loadingSpan = document.createElement("span");
    loadingSpan.classList.add("loading", "loading-spinner");
    button.innerHTML = "";
    button.appendChild(loadingSpan);
    button.disabled = true;
    var form = document.getElementById("pix2pix_form");
    setTimeout(() => {
        form.submit();
    }, 1000);
}

function button2reset(button) {
    const loadingSpan = document.createElement("span");
    loadingSpan.classList.add("loading", "loading-spinner");
    button.innerHTML = "";
    button.appendChild(loadingSpan);
    button.disabled = true;
    var form = document.getElementById("reset_form");
    setTimeout(() => {
        form.submit();
    }, 1000);
}

document.addEventListener("DOMContentLoaded", function () {
    const searchIcon = document.querySelector("#img-icon");
    const overlay = document.querySelector(".overlay");
    const closeButton = document.querySelector("#img-input-wrapper>button");

    searchIcon.addEventListener("click", function () {
        overlay.classList.toggle("active");
    });

    closeButton.addEventListener("click", function () {
        overlay.classList.remove("active");
    });
});

function submit_img_form(action, button) {
    const loadingSpan = document.createElement("span");
    loadingSpan.classList.add("loading", "loading-spinner");
    button.innerHTML = "";
    button.appendChild(loadingSpan);
    button.disabled = true;
    var form = document.getElementById("imgForm");
    form.action = action;
    setTimeout(() => {
        console.log("submitting form");
        form.submit();
    }, 1000);
}
