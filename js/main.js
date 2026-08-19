// Smooth scrolling for navigation links
const navLinks = document.querySelectorAll('.nav-menu a');

navLinks.forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        const targetId = this.getAttribute('href').substring(1);
        const targetSection = document.getElementById(targetId);
        
        if (targetSection) {
            targetSection.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Form submission
const contactForm = document.querySelector('.contact-form');

if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Get form data
        const formData = new FormData(this);
        
        // Show success message
        alert('Спасибо за вашу заявку! Мы свяжемся с вами в ближайшее время.');
        
        // Clear form
        this.reset();
    });
}

// Primary button click handlers
const primaryButtons = document.querySelectorAll('.btn-primary');

primaryButtons.forEach(button => {
    button.addEventListener('click', function() {
        // Redirect to training or show modal
        const trainingSection = document.getElementById('training');
        if (trainingSection) {
            trainingSection.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});

// Add scroll animation for feature cards
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

document.querySelectorAll('.feature-card, .training-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(card);
});

console.log('ЭЛОу АВТ - Тренажерный комплекс загружен успешно!');