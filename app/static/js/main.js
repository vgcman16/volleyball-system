// Loading Spinner Management
const spinner = {
    show: function() {
        const spinnerWrapper = document.querySelector('.spinner-wrapper');
        if (spinnerWrapper) {
            spinnerWrapper.classList.add('active');
        }
    },
    hide: function() {
        const spinnerWrapper = document.querySelector('.spinner-wrapper');
        if (spinnerWrapper) {
            spinnerWrapper.classList.remove('active');
        }
    }
};

// Form Validation
document.addEventListener('DOMContentLoaded', function() {
    // Password strength indicator
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    passwordInputs.forEach(input => {
        input.addEventListener('input', function() {
            const strength = checkPasswordStrength(this.value);
            updatePasswordStrengthIndicator(this, strength);
        });
    });

    // Form submission handling
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!this.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            } else {
                spinner.show();
            }
            this.classList.add('was-validated');
        });
    });

    // Profile image preview
    const profileImageInput = document.getElementById('profile_image');
    if (profileImageInput) {
        profileImageInput.addEventListener('change', previewImage);
    }

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});

// Password Strength Checker
function checkPasswordStrength(password) {
    let strength = 0;
    
    // Length check
    if (password.length >= 8) strength += 1;
    
    // Contains number
    if (/\d/.test(password)) strength += 1;
    
    // Contains lowercase
    if (/[a-z]/.test(password)) strength += 1;
    
    // Contains uppercase
    if (/[A-Z]/.test(password)) strength += 1;
    
    // Contains special character
    if (/[^A-Za-z0-9]/.test(password)) strength += 1;
    
    return strength;
}

// Update Password Strength Indicator
function updatePasswordStrengthIndicator(input, strength) {
    let indicator = input.nextElementSibling;
    if (!indicator || !indicator.classList.contains('password-strength')) {
        indicator = document.createElement('div');
        indicator.className = 'password-strength progress mt-2';
        indicator.style.height = '5px';
        indicator.innerHTML = '<div class="progress-bar" role="progressbar"></div>';
        input.parentNode.insertBefore(indicator, input.nextSibling);
    }
    
    const progressBar = indicator.querySelector('.progress-bar');
    const percentage = (strength / 5) * 100;
    progressBar.style.width = percentage + '%';
    
    // Update color based on strength
    let color;
    if (strength <= 2) color = 'bg-danger';
    else if (strength <= 3) color = 'bg-warning';
    else if (strength <= 4) color = 'bg-info';
    else color = 'bg-success';
    
    progressBar.className = 'progress-bar ' + color;
}

// Profile Image Preview
function previewImage(e) {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const preview = document.querySelector('.profile-pic-wrapper img');
            if (preview) {
                preview.src = e.target.result;
            }
        }
        reader.readAsDataURL(file);
    }
}

// Alert Auto-dismiss
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});

// Confirmation Dialog
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// Date Formatting
function formatDate(date) {
    return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Time Formatting
function formatTime(time) {
    return new Date(time).toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
    });
}

// AJAX Request Helper
async function makeRequest(url, options = {}) {
    try {
        spinner.show();
        const response = await fetch(url, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            }
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Request failed:', error);
        throw error;
    } finally {
        spinner.hide();
    }
}

// Form Data to JSON
function formDataToJson(form) {
    const formData = new FormData(form);
    const data = {};
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }
    return data;
}

// Debounce Function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}
