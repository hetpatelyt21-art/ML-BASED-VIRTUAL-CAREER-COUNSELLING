// script.js

document.addEventListener("DOMContentLoaded", () => {
  console.log("Mentoraa Homepage Loaded");

  // Scroll to top on refresh
  window.scrollTo(0, 0);

  // Optional: Smooth scroll for internal nav links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        target.scrollIntoView({ behavior: "smooth" });
      }
    });
  });

  // Placeholder for future features:
  // - Mobile nav toggle
  // - Form submission handling
  // - FAQ expand/collapse
});

function toggleMenu() {
  const nav = document.getElementById("site-nav");
  if (nav) {
    nav.classList.toggle("active");
  }
}

function toggleProfileMenu() {
  const menu = document.getElementById("profile-menu");
  if (menu) {
    menu.classList.toggle("active");
  }
}

function goBack(fallbackUrl) {
  if (window.history.length > 1) {
    window.history.back();
    return;
  }

  window.location.href = fallbackUrl;
}

document.addEventListener("click", (event) => {
  const menu = document.getElementById("profile-menu");
  const trigger = document.querySelector(".profile-dropdown");
  if (!menu || !trigger) {
    return;
  }

  if (!trigger.contains(event.target)) {
    menu.classList.remove("active");
  }
});
