// Main JavaScript file for Shahin Auto Service

// DOM Content Loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// Initialize Application
function initializeApp() {
    initializeMobileMenu();
    initializeDarkMode();
    initializeScrollAnimations();
    initializeLazyLoading();
    initializeContactForm();
    initializeBackToTop();
    initializeSmoothScrolling();
    initializeParallax();
    initializeVideoLazyLoading();
    initializeSearchFunctionality();
    initializeHeaderScroll();
}

// Mobile Menu Functions
function initializeMobileMenu() {
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    const mobileMenuClose = document.getElementById('mobile-menu-close');

    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', () => {
            mobileMenu.classList.add('open');
            document.body.style.overflow = 'hidden';
        });

        if (mobileMenuClose) {
            mobileMenuClose.addEventListener('click', closeMobileMenu);
        }

        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!mobileMenu.contains(e.target) && !mobileMenuButton.contains(e.target)) {
                closeMobileMenu();
            }
        });

        // Close menu on escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && mobileMenu.classList.contains('open')) {
                closeMobileMenu();
            }
        });
    }
}

function closeMobileMenu() {
    const mobileMenu = document.getElementById('mobile-menu');
    if (mobileMenu) {
        mobileMenu.classList.remove('open');
        document.body.style.overflow = '';
    }
}

// Dark Mode Functions
function initializeDarkMode() {
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    const darkModeToggleMobile = document.getElementById('dark-mode-toggle-mobile');
    const body = document.body;

    // Check for saved dark mode preference
    const savedDarkMode = localStorage.getItem('darkMode');
    if (savedDarkMode === 'true') {
        body.classList.add('dark-mode');
    }

    // Check for system preference
    if (!savedDarkMode && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        body.classList.add('dark-mode');
        localStorage.setItem('darkMode', 'true');
    }

    function toggleDarkMode() {
        body.classList.toggle('dark-mode');
        const isDarkMode = body.classList.contains('dark-mode');
        localStorage.setItem('darkMode', isDarkMode);
        
        // Update toggle button text
        const toggleText = isDarkMode ? 'حالت روشن' : 'حالت تاریک';
        if (darkModeToggleMobile) {
            darkModeToggleMobile.textContent = toggleText;
        }
    }

    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', toggleDarkMode);
    }
    
    if (darkModeToggleMobile) {
        darkModeToggleMobile.addEventListener('click', toggleDarkMode);
    }
}

// Scroll Animations
function initializeScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all elements with data-aos attribute
    document.querySelectorAll('[data-aos]').forEach(element => {
        observer.observe(element);
    });
}

// Lazy Loading for Images
function initializeLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    if (images.length === 0) return;

    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                img.classList.add('loaded');
                imageObserver.unobserve(img);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '50px'
    });

    images.forEach(img => {
        img.classList.add('lazy');
        imageObserver.observe(img);
    });
}

// Contact Form Handling
function initializeContactForm() {
    const contactForm = document.getElementById('contact-form');
    const contactFormMessage = document.getElementById('contact-form-message');
    const loadingSpinner = document.getElementById('loading-spinner');

    if (!contactForm) return;

    contactForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(contactForm);
        const data = {
            name: formData.get('name')?.trim(),
            email: formData.get('email')?.trim(),
            message: formData.get('message')?.trim()
        };

        // Validation
        if (!data.name || !data.email || !data.message) {
            showMessage('لطفاً تمام فیلدها را پر کنید', 'error');
            return;
        }

        if (!isValidEmail(data.email)) {
            showMessage('لطفاً یک ایمیل معتبر وارد کنید', 'error');
            return;
        }

        showLoading(true);

        try {
            const response = await fetch('/api/contact/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (result.success) {
                showMessage(result.message, 'success');
                contactForm.reset();
            } else {
                showMessage(result.message || 'خطا در ارسال پیام', 'error');
            }
        } catch (error) {
            console.error('Contact form error:', error);
            showMessage('خطا در ارسال پیام. لطفاً دوباره تلاش کنید.', 'error');
        } finally {
            showLoading(false);
        }
    });

    function showMessage(message, type) {
        if (!contactFormMessage) return;

        contactFormMessage.textContent = message;
        contactFormMessage.className = `mt-4 p-3 rounded-lg ${
            type === 'success' 
                ? 'bg-green-100 text-green-800 border border-green-200' 
                : 'bg-red-100 text-red-800 border border-red-200'
        }`;
        contactFormMessage.classList.remove('hidden');
        
        // Hide message after 5 seconds
        setTimeout(() => {
            contactFormMessage.classList.add('hidden');
        }, 5000);
    }

    function showLoading(show) {
        if (loadingSpinner) {
            if (show) {
                loadingSpinner.classList.remove('hidden');
            } else {
                loadingSpinner.classList.add('hidden');
            }
        }
    }
}

// Back to Top Button
function initializeBackToTop() {
    const backToTopButton = document.getElementById('back-to-top');

    if (!backToTopButton) return;

    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            backToTopButton.classList.remove('hidden');
        } else {
            backToTopButton.classList.add('hidden');
        }
    });

    backToTopButton.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// Smooth Scrolling
function initializeSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const headerHeight = document.querySelector('header')?.offsetHeight || 0;
                const targetPosition = target.offsetTop - headerHeight - 20;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Parallax Effect
function initializeParallax() {
    const parallaxElements = document.querySelectorAll('.parallax');
    
    if (parallaxElements.length === 0) return;

    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        
        parallaxElements.forEach(element => {
            const speed = element.dataset.speed || 0.5;
            const yPos = -(scrolled * speed);
            element.style.transform = `translateY(${yPos}px)`;
        });
    });
}

// Video Lazy Loading
function initializeVideoLazyLoading() {
    const videoObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const iframe = entry.target;
                if (iframe.dataset.src) {
                    iframe.src = iframe.dataset.src;
                    iframe.removeAttribute('data-src');
                    videoObserver.unobserve(iframe);
                }
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '100px'
    });

    document.querySelectorAll('iframe[data-src]').forEach(iframe => {
        videoObserver.observe(iframe);
    });
}

// Search Functionality
function initializeSearchFunctionality() {
    const searchInput = document.getElementById('search-input');
    
    if (!searchInput) return;

    let searchTimeout;
    
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        const searchTerm = this.value.toLowerCase().trim();
        
        if (searchTerm.length < 2) {
            showAllResults();
            return;
        }
        
        searchTimeout = setTimeout(() => {
            performSearch(searchTerm);
        }, 300);
    });

    function performSearch(term) {
        const searchableElements = document.querySelectorAll('[data-searchable]');
        let hasResults = false;
        
        searchableElements.forEach(element => {
            const title = element.querySelector('[data-search-title]')?.textContent.toLowerCase() || '';
            const content = element.querySelector('[data-search-content]')?.textContent.toLowerCase() || '';
            
            if (title.includes(term) || content.includes(term)) {
                element.style.display = 'block';
                element.classList.add('search-highlight');
                hasResults = true;
            } else {
                element.style.display = 'none';
                element.classList.remove('search-highlight');
            }
        });
        
        showSearchResults(hasResults);
    }

    function showAllResults() {
        const searchableElements = document.querySelectorAll('[data-searchable]');
        searchableElements.forEach(element => {
            element.style.display = 'block';
            element.classList.remove('search-highlight');
        });
        hideSearchResults();
    }

    function showSearchResults(hasResults) {
        let resultsMessage = document.getElementById('search-results-message');
        if (!resultsMessage) {
            resultsMessage = document.createElement('div');
            resultsMessage.id = 'search-results-message';
            resultsMessage.className = 'text-center py-4 text-gray-600';
            const searchContainer = document.querySelector('.search-container');
            if (searchContainer) {
                searchContainer.appendChild(resultsMessage);
            }
        }
        
        if (hasResults) {
            resultsMessage.textContent = '';
            resultsMessage.classList.add('hidden');
        } else {
            resultsMessage.textContent = 'نتیجه‌ای یافت نشد';
            resultsMessage.classList.remove('hidden');
        }
    }

    function hideSearchResults() {
        const resultsMessage = document.getElementById('search-results-message');
        if (resultsMessage) {
            resultsMessage.classList.add('hidden');
        }
    }
}

// Utility Functions
function getCSRFToken() {
    const token = document.querySelector('[name=csrfmiddlewaretoken]');
    return token ? token.value : '';
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

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

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Service Modal Functions (for home page)
function openServiceModal(serviceSlug) {
    const modal = document.getElementById('service-modal');
    const title = document.getElementById('modal-title');
    const content = document.getElementById('modal-content');
    
    if (!modal || !title || !content) return;
    
    // Show loading
    content.innerHTML = '<div class="text-center py-8"><div class="loading-spinner mx-auto"></div></div>';
    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
    
    // Fetch service data
    fetch(`/api/services/${serviceSlug}/`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            title.textContent = data.name;
            content.innerHTML = `
                <div class="space-y-4">
                    <img src="${data.image}" alt="${data.name}" class="w-full h-48 object-cover rounded-lg">
                    <p class="text-gray-600">${data.description}</p>
                    <div class="flex gap-2">
                        ${data.instagram_link ? `<a href="${data.instagram_link}" target="_blank" class="flex-1 bg-gradient-to-r from-purple-500 to-pink-500 text-white text-center py-2 px-4 rounded-lg hover:from-purple-600 hover:to-pink-600 transition-all duration-300">مشاهده در اینستاگرام</a>` : ''}
                        <a href="/service/${data.slug}/" class="flex-1 bg-primary-blue text-white text-center py-2 px-4 rounded-lg hover:bg-blue-700 transition-all duration-300">مشاهده آموزش</a>
                    </div>
                </div>
            `;
        })
        .catch(error => {
            console.error('Error loading service:', error);
            content.innerHTML = '<p class="text-red-500 text-center">خطا در بارگذاری اطلاعات</p>';
        });
}

function closeServiceModal() {
    const modal = document.getElementById('service-modal');
    if (modal) {
        modal.classList.add('hidden');
        document.body.style.overflow = '';
    }
}

// Share Functions
function shareOnWhatsApp() {
    const url = encodeURIComponent(window.location.href);
    const text = encodeURIComponent(document.title);
    window.open(`https://wa.me/?text=${text}%20${url}`, '_blank');
}

function shareOnTelegram() {
    const url = encodeURIComponent(window.location.href);
    const text = encodeURIComponent(document.title);
    window.open(`https://t.me/share/url?url=${url}&text=${text}`, '_blank');
}

function copyLink() {
    navigator.clipboard.writeText(window.location.href).then(() => {
        // Show success message
        const button = event.target.closest('button');
        if (button) {
            const originalText = button.innerHTML;
            button.innerHTML = '<svg class="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>کپی شد';
            button.classList.add('bg-green-500', 'hover:bg-green-600');
            button.classList.remove('bg-gray-500', 'hover:bg-gray-600');
            
            setTimeout(() => {
                button.innerHTML = originalText;
                button.classList.remove('bg-green-500', 'hover:bg-green-600');
                button.classList.add('bg-gray-500', 'hover:bg-gray-600');
            }, 2000);
        }
    }).catch(err => {
        console.error('Failed to copy link:', err);
    });
}

// Error Handling
window.addEventListener('error', function(e) {
    console.error('JavaScript error:', e.error);
});

window.addEventListener('unhandledrejection', function(e) {
    console.error('Unhandled promise rejection:', e.reason);
});

// Header Scroll Effect
function initializeHeaderScroll() {
    const header = document.querySelector('header');
    if (!header) return;

    const scrollThreshold = 50;

    window.addEventListener('scroll', throttle(() => {
        const currentScroll = window.pageYOffset || document.documentElement.scrollTop;

        if (currentScroll > scrollThreshold) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    }, 10));
}

// Performance Monitoring
if ('performance' in window) {
    window.addEventListener('load', function() {
        setTimeout(() => {
            const perfData = performance.getEntriesByType('navigation')[0];
            console.log('Page load time:', perfData.loadEventEnd - perfData.loadEventStart, 'ms');
        }, 0);
    });
}
