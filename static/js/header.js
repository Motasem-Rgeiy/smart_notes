const profile_btn = document.getElementById('profile_btn');
const profile_options = document.getElementById('profile-options');

// 1. Toggle visibility on button click
profile_btn.addEventListener('click', (e) => {
    e.stopPropagation(); // Prevents this click from immediately reaching document!
    profile_options.classList.toggle('hidden');
    profile_options.classList.toggle('flex');
});

// 2. Global listener (placed OUTSIDE, defined only once)
document.addEventListener('click', (e) => {
    // If click is outside the menu and outside the button, hide it
    if (!profile_options.contains(e.target) && !profile_btn.contains(e.target)) {
        profile_options.classList.remove('flex');
        profile_options.classList.add('hidden');
    }
});