// selecting colors
const colorOptions = document.querySelectorAll('.color-option');
const selectedColor = document.getElementById('selected-color');

colorOptions.forEach(colorOption => {
  colorOption.addEventListener('click', () => {
    // Set the value of the hidden input field to the selected color
    selectedColor.value = colorOption.dataset.color;

    // Remove the "selected" class from all color options
    colorOptions.forEach(option => option.classList.remove('selected'));

    // Add the "selected" class to the clicked color option
    colorOption.classList.add('selected');
  });
});


// selecting size
const sizeOptions = document.querySelectorAll('.size-option');
const selectedSize = document.getElementById('selected-size');

sizeOptions.forEach(sizeOption => {
  sizeOption.addEventListener('click', () => {
    // Set the value of the hidden input field to the selected div text
    selectedSize.value = sizeOption.dataset.value;

    // Remove the "selected" class from all size options
    sizeOptions.forEach(option => option.classList.remove('selected'));

    // Add the "selected" class to the clicked size option
    sizeOption.classList.add('selected');
  });
});



// incresting and decreasing quantity
const decrementBtn = document.getElementById("decrement");
const incrementBtn = document.getElementById("increment");
const inputField = document.getElementById("myInput");

decrementBtn.addEventListener("click", () => {
inputField.value = parseInt(inputField.value) + 1;
});

incrementBtn.addEventListener("click", () => {
if (inputField.value > 1) {
inputField.value = parseInt(inputField.value) - 1;
}
});
