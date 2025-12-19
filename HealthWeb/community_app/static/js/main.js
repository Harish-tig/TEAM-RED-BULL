// Main JavaScript file for HealthConnect

document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const navLinks = document.querySelector('.nav-links');

    if (mobileMenuBtn && navLinks) {
        mobileMenuBtn.addEventListener('click', function() {
            navLinks.classList.toggle('active');
            const icon = this.querySelector('i');
            if (icon.classList.contains('fa-bars')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });

        // Close menu when clicking outside
        document.addEventListener('click', function(event) {
            if (!mobileMenuBtn.contains(event.target) && !navLinks.contains(event.target)) {
                navLinks.classList.remove('active');
                const icon = mobileMenuBtn.querySelector('i');
                if (icon.classList.contains('fa-times')) {
                    icon.classList.remove('fa-times');
                    icon.classList.add('fa-bars');
                }
            }
        });
    }

    // Auto-hide messages after 5 seconds
    const messages = document.querySelectorAll('.alert');
    messages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => {
                message.style.display = 'none';
            }, 300);
        }, 5000);
    });

    // Initialize tooltips
    initTooltips();

    // Initialize form validation
    initFormValidation();

    // Smooth scrolling for anchor links
    initSmoothScrolling();
});

// Tooltip functionality
function initTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');

    tooltipElements.forEach(element => {
        const tooltipText = element.getAttribute('data-tooltip');

        // Create tooltip element
        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip';
        tooltip.textContent = tooltipText;
        document.body.appendChild(tooltip);

        // Position tooltip
        function positionTooltip() {
            const rect = element.getBoundingClientRect();
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

            tooltip.style.position = 'absolute';
            tooltip.style.left = rect.left + rect.width / 2 - tooltip.offsetWidth / 2 + 'px';
            tooltip.style.top = rect.top + scrollTop - tooltip.offsetHeight - 10 + 'px';
        }

        // Show tooltip on hover
        element.addEventListener('mouseenter', () => {
            tooltip.style.display = 'block';
            positionTooltip();
        });

        // Hide tooltip
        element.addEventListener('mouseleave', () => {
            tooltip.style.display = 'none';
        });

        // Update position on resize
        window.addEventListener('resize', positionTooltip);
    });
}

// Form validation
function initFormValidation() {
    const forms = document.querySelectorAll('form[data-validate]');

    forms.forEach(form => {
        const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');

        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });

            input.addEventListener('input', function() {
                clearFieldError(this);
            });
        });

        form.addEventListener('submit', function(event) {
            let isValid = true;

            inputs.forEach(input => {
                if (!validateField(input)) {
                    isValid = false;
                }
            });

            if (!isValid) {
                event.preventDefault();
                showFormError(form, 'Please fill in all required fields correctly.');
            }
        });
    });
}

function validateField(field) {
    let isValid = true;
    const value = field.value.trim();

    // Clear previous errors
    clearFieldError(field);

    // Check if empty
    if (field.hasAttribute('required') && !value) {
        showFieldError(field, 'This field is required.');
        isValid = false;
    }

    // Email validation
    if (field.type === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            showFieldError(field, 'Please enter a valid email address.');
            isValid = false;
        }
    }

    // Password strength validation
    if (field.type === 'password' && value) {
        if (value.length < 8) {
            showFieldError(field, 'Password must be at least 8 characters long.');
            isValid = false;
        }
    }

    // Add validation classes
    if (isValid && value) {
        field.classList.add('success');
    } else if (!isValid) {
        field.classList.add('error');
    }

    return isValid;
}

function showFieldError(field, message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'form-error';
    errorDiv.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${message}`;

    field.parentNode.appendChild(errorDiv);
}

function clearFieldError(field) {
    const errorDiv = field.parentNode.querySelector('.form-error');
    if (errorDiv) {
        errorDiv.remove();
    }
    field.classList.remove('error', 'success');
}

function showFormError(form, message) {
    const existingError = form.querySelector('.form-error-general');
    if (existingError) {
        existingError.remove();
    }

    const errorDiv = document.createElement('div');
    errorDiv.className = 'alert alert-error form-error-general';
    errorDiv.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${message}`;

    form.insertBefore(errorDiv, form.firstChild);

    // Scroll to error
    errorDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

// Smooth scrolling
function initSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(event) {
            const href = this.getAttribute('href');

            if (href === '#') return;

            const targetElement = document.querySelector(href);
            if (targetElement) {
                event.preventDefault();

                window.scrollTo({
                    top: targetElement.offsetTop - 100,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Upvote functionality
function handleUpvote(event, element, url) {
    event.preventDefault();

    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        },
        credentials: 'same-origin'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const countElement = element.querySelector('.upvote-count');
            if (countElement) {
                countElement.textContent = data.count;
            }

            const icon = element.querySelector('i');
            if (data.voted) {
                icon.classList.add('text-primary');
                icon.classList.remove('text-muted');
            } else {
                icon.classList.remove('text-primary');
                icon.classList.add('text-muted');
            }
        }
    })
    .catch(error => console.error('Error:', error));
}

// Get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Tab functionality
function switchTab(tabId, containerId) {
    // Hide all tab contents
    const contents = document.querySelectorAll(`#${containerId} .tab-content`);
    contents.forEach(content => {
        content.classList.remove('active');
    });

    // Remove active class from all tabs
    const tabs = document.querySelectorAll(`#${containerId} .tab`);
    tabs.forEach(tab => {
        tab.classList.remove('active');
    });

    // Show selected tab content
    const activeContent = document.getElementById(`${tabId}-content`);
    if (activeContent) {
        activeContent.classList.add('active');
    }

    // Add active class to clicked tab
    const activeTab = document.querySelector(`#${containerId} .tab[data-tab="${tabId}"]`);
    if (activeTab) {
        activeTab.classList.add('active');
    }
}

// Debounce function for performance
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

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diff = now - date;

    // Less than a minute
    if (diff < 60000) {
        return 'just now';
    }

    // Less than an hour
    if (diff < 3600000) {
        const minutes = Math.floor(diff / 60000);
        return `${minutes}m ago`;
    }

    // Less than a day
    if (diff < 86400000) {
        const hours = Math.floor(diff / 3600000);
        return `${hours}h ago`;
    }

    // Less than a week
    if (diff < 604800000) {
        const days = Math.floor(diff / 86400000);
        return `${days}d ago`;
    }

    // Otherwise, format as date
    return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric'
    });
}

// Update all relative timestamps
function updateRelativeTimes() {
    document.querySelectorAll('[data-timestamp]').forEach(element => {
        const timestamp = element.getAttribute('data-timestamp');
        if (timestamp) {
            element.textContent = formatDate(timestamp);
        }
    });
}

// Initialize relative times
updateRelativeTimes();
setInterval(updateRelativeTimes, 60000); // Update every minute