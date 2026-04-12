/* Main JavaScript */

// Logo flip animation - only on first page load
document.addEventListener('DOMContentLoaded', function() {
    // Check if this is the first load using sessionStorage
    const isFirstLoad = !sessionStorage.getItem('site-loaded');
    
    // Handle navbar logo
    const navLogo = document.getElementById('navbar-logo');
    // Handle hero logo (if on home page)
    const heroLogo = document.querySelector('.hero-logo');
    
    if (isFirstLoad) {
        // First load: trigger animation on both logos
        if (navLogo) {
            navLogo.classList.remove('first-load');
            void navLogo.offsetWidth; // Force reflow
            navLogo.classList.add('first-load');
        }
        
        if (heroLogo) {
            heroLogo.classList.remove('first-load');
            void heroLogo.offsetWidth; // Force reflow
            heroLogo.classList.add('first-load');
        }
        
        // Mark that site has been loaded
        sessionStorage.setItem('site-loaded', 'true');
    } else {
        // Subsequent navigation: no animation
        if (navLogo) {
            navLogo.classList.remove('first-load');
        }
        if (heroLogo) {
            heroLogo.classList.remove('first-load');
        }
    }
});

// Form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (form && form.checkValidity() === false) {
        event.preventDefault();
        event.stopPropagation();
    }
    if (form) {
        form.classList.add('was-validated');
    }
}

// Smooth scroll for internal links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// Auto-hide alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            try {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            } catch (e) {
                alert.style.display = 'none';
            }
        }, 5000);
    });
    
    // Initialize countdowns for all deadline elements
    const countdownElements = document.querySelectorAll('.countdown[data-deadline]');
    countdownElements.forEach(element => {
        const deadline = element.getAttribute('data-deadline');
        if (deadline) {
            startCountdownElement(deadline, element);
        }
    });
});

// Format phone numbers
function formatPhoneNumber(phone) {
    const cleaned = phone.replace(/\D/g, '');
    if (cleaned.length === 10) {
        return `+254${cleaned.slice(1)}`;
    }
    return phone;
}

// Countdown timer for tax deadlines - updated for new structure
function startCountdownElement(endDate, element) {
    const updateCountdown = () => {
        const now = new Date().getTime();
        const distance = new Date(endDate).getTime() - now;

        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);

        if (element) {
            // Update the countdown values
            const daysSpan = element.querySelector('.days-value');
            const hoursSpan = element.querySelector('.hours-value');
            const minsSpan = element.querySelector('.mins-value');
            const secsSpan = element.querySelector('.secs-value');
            
            if (daysSpan) daysSpan.textContent = String(days).padStart(2, '0');
            if (hoursSpan) hoursSpan.textContent = String(hours).padStart(2, '0');
            if (minsSpan) minsSpan.textContent = String(minutes).padStart(2, '0');
            if (secsSpan) secsSpan.textContent = String(seconds).padStart(2, '0');
        }

        if (distance < 0) {
            return true; // Return true to signal the timer should stop
        }
        return false;
    };
    
    // Update immediately
    const shouldStop = updateCountdown();
    
    // Update every second
    if (!shouldStop) {
        const timer = setInterval(() => {
            if (updateCountdown()) {
                clearInterval(timer);
            }
        }, 1000);
    }
}

// Legacy function for backward compatibility
function startCountdown(endDate, elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        startCountdownElement(endDate, element);
    }
}

// Tab switching
function switchTab(tabName) {
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => tab.style.display = 'none');
    const tab = document.getElementById(tabName);
    if (tab) {
        tab.style.display = 'block';
    }
}

// Dark mode toggle (optional)
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
}
