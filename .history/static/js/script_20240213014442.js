// delete images on error
const images = document.querySelectorAll("img");

images.forEach(function (image) {
    image.addEventListener("error", function () {
        console.error("Image load error:", image.src);
        console.log("404 image:", image.src);
        const parentElement = image.parentElement;
        if (parentElement) {
            console.log("parentElement:", parentElement);
            parentElement.remove();
            console.log("image removed");
        }
    });
});

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

// const copyButtons_2 = document.querySelectorAll(".prompt-text-wrapper");
// copyButtons_2.forEach(function (button) {
//     button.addEventListener("click", function () {
//         console.log("copy button clicked");
//         const text =
//             this.parentNode.parentNode.querySelector(
//                 ".prompt-text-p"
//             ).textContent;
//         navigator.clipboard.writeText(text).then(
//             () => {
//                 console.log("Copied to clipboard:", text);
//                 this.classList.add("copied");
//                 setTimeout(() => {
//                     this.classList.remove("copied");
//                 }, 200);
//             },
//             function (err) {
//                 console.error("Async: Could not copy text: ", err);
//             }
//         );
//     });
// });
