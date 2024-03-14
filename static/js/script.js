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

// function deleteFile() {
//     var fileName = document.getElementById("file_name").value;
//     var xhr = new XMLHttpRequest();
//     xhr.open("DELETE", fileName, true);
//     console.log("deleting file:", fileName);
//     xhr.onreadystatechange = function() {
//         if (xhr.readyState == 4) {
//             if (xhr.status == 200) {
//                 console.log("File deleted successfully");
//             } else {
//                 console.error("Failed to delete file: " + xhr.statusText);
//             }
//         }
//     };
//     xhr.send();
// }

const dropzone = document.getElementById("dropzone");
var fileInput = document.getElementById("dropzone-file");
var submitButton = document.getElementById("img-submit-btn");
const form = document.getElementById("imgForm");

fileInput.addEventListener("change", function () {
    if (fileInput.files.length > 0) {
        submitButton.disabled = false;
        dropzone.classList.add("grayed-out");
    } else {
        submitButton.disabled = true;
        dropzone.classList.remove("grayed-out");
    }
});

dropzone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropzone.classList.add("border-blue-500");
});

dropzone.addEventListener("dragleave", () => {
    dropzone.classList.remove("border-blue-500");
});

dropzone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropzone.classList.remove("border-blue-500");
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        const file = files[0];
        fileInput.files = files;
        dropzone.classList.add("grayed-out");
        submitButton.disabled = false;
    }
});