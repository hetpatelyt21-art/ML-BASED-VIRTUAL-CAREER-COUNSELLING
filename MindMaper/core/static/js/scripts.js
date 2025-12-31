// Theme Toggle Logic
const themeToggle = document.getElementById("theme-toggle");

themeToggle.addEventListener("click", () => {
  document.body.classList.toggle("light-mode");

  // Save to localStorage
  if (document.body.classList.contains("light-mode")) {
    localStorage.setItem("theme", "light");
  } else {
    localStorage.setItem("theme", "dark");
  }
});

// On page load, apply saved theme
window.addEventListener("DOMContentLoaded", () => {
  const savedTheme = localStorage.getItem("theme");

  if (savedTheme === "light") {
    document.body.classList.add("light-mode");
  } else {
    document.body.classList.remove("light-mode");
  }
});


// Toggle Profile dropdown
function toggleProfileDropdown() {
  const profileDropdown = document.getElementById("profile-dropdown");
  profileDropdown.style.display = (profileDropdown.style.display === "block") ? "none" : "block";
}

// Toggle Take a Test dropdown
function toggleTestDropdown() {
  const testDropdown = document.getElementById("test-dropdown");
  testDropdown.style.display = (testDropdown.style.display === "block") ? "none" : "block";
}

// Close dropdowns when clicking outside
document.addEventListener("click", function (e) {
  // Profile dropdown
  const profileMenu = document.querySelector(".profile-menu");
  const profileDropdown = document.getElementById("profile-dropdown");
  if (profileDropdown && profileMenu && !profileMenu.contains(e.target)) {
    profileDropdown.style.display = "none";
  }

  // Test dropdown
  const testMenu = document.querySelector(".test-menu");
  const testDropdown = document.getElementById("test-dropdown");
  if (testDropdown && testMenu && !testMenu.contains(e.target)) {
    testDropdown.style.display = "none";
  }
});


function updateSliderValue(slider) {
  const valueDisplay = slider.nextElementSibling;
  if (valueDisplay && valueDisplay.classList.contains('slider-value')) {
    valueDisplay.textContent = slider.value;
  }
}
