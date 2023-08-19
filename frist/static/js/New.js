document.addEventListener('DOMContentLoaded', function () {
  const searchPriceFromInput = document.getElementById('searchPriceFrom');
  const searchPriceToInput = document.getElementById('searchPriceTo');
  const searchButton = document.getElementById('searchButton');

  // Function to check if any of the inputs are empty or invalid
  function validateInputs() {
    const searchPriceFromValue = parseFloat(searchPriceFromInput.value);
    const searchPriceToValue = parseFloat(searchPriceToInput.value);

    if (
      isNaN(searchPriceFromValue) ||
      isNaN(searchPriceToValue) ||
      searchPriceFromValue < 1 ||
      searchPriceToValue < 1 ||
      searchPriceToValue < searchPriceFromValue
    ) {
      searchButton.disabled = true;
      searchButton.classList.add('disabled-button'); // Add the CSS class
    } else {
      searchButton.disabled = false;
      searchButton.classList.remove('disabled-button'); // Remove the CSS class
    }
  }

  // Attach event listeners to input fields
  searchPriceFromInput.addEventListener('input', validateInputs);
  searchPriceToInput.addEventListener('input', validateInputs);
});

