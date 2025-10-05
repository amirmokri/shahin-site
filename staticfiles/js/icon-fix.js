// Font Awesome Icon Fix Script
(function() {
    'use strict';
    
    // Icon mappings with Unicode fallbacks
    const iconMappings = {
        'fa-home': { unicode: '🏠', code: '\\f015' },
        'fa-phone': { unicode: '📞', code: '\\f095' },
        'fa-envelope': { unicode: '✉️', code: '\\f0e0' },
        'fa-calendar-check': { unicode: '📅', code: '\\f274' },
        'fa-newspaper': { unicode: '📰', code: '\\f1ea' },
        'fa-cogs': { unicode: '⚙️', code: '\\f085' },
        'fa-cog': { unicode: '⚙️', code: '\\f013' },
        'fa-gears': { unicode: '⚙️', code: '\\f085' },
        'fa-star': { unicode: '⭐', code: '\\f005' },
        'fa-check': { unicode: '✅', code: '\\f00c' },
        'fa-arrow-left': { unicode: '←', code: '\\f060' },
        'fa-arrow-up': { unicode: '↑', code: '\\f062' },
        'fa-play': { unicode: '▶️', code: '\\f04b' },
        'fa-clock': { unicode: '🕐', code: '\\f017' },
        'fa-tag': { unicode: '🏷️', code: '\\f02b' },
        'fa-eye': { unicode: '👁️', code: '\\f06e' },
        'fa-book': { unicode: '📖', code: '\\f02d' },
        'fa-comments': { unicode: '💬', code: '\\f086' },
        'fa-comment-slash': { unicode: '🚫', code: '\\f4b3' },
        'fa-paper-plane': { unicode: '✈️', code: '\\f1d8' },
        'fa-location-dot': { unicode: '📍', code: '\\f3c5' },
        'fa-moon': { unicode: '🌙', code: '\\f186' },
        'fa-chart-bar': { unicode: '📊', code: '\\f080' },
        'fa-tools': { unicode: '🔧', code: '\\f7d9' },
        'fa-server': { unicode: '🖥️', code: '\\f233' },
        'fa-code': { unicode: '💻', code: '\\f121' },
        'fa-database': { unicode: '🗄️', code: '\\f1c0' },
        'fa-rocket': { unicode: '🚀', code: '\\f135' },
        'fa-plus': { unicode: '➕', code: '\\f067' },
        'fa-sign-out-alt': { unicode: '🚪', code: '\\f2f5' },
        'fa-exclamation-triangle': { unicode: '⚠️', code: '\\f071' },
        'fa-spinner': { unicode: '⏳', code: '\\f110' },
        'fa-check-circle': { unicode: '✅', code: '\\f058' },
        'fa-exclamation-circle': { unicode: '❌', code: '\\f06a' },
        'fa-external-link-alt': { unicode: '🔗', code: '\\f35d' },
        'fa-user': { unicode: '👤', code: '\\f007' },
        'fa-comment': { unicode: '💬', code: '\\f075' },
        'fa-list': { unicode: '📋', code: '\\f03a' },
        'fa-chevron-left': { unicode: '◀️', code: '\\f053' },
        'fa-chevron-right': { unicode: '▶️', code: '\\f054' },
        'fa-headset': { unicode: '🎧', code: '\\f590' },
        'fa-circle-info': { unicode: 'ℹ️', code: '\\f05a' },
        'fa-info-circle': { unicode: 'ℹ️', code: '\\f05a' }
    };
    
    // Brand icon mappings
    const brandIconMappings = {
        'fa-instagram': { unicode: '📷', code: '\\f16d' }
    };
    
    function injectFontAwesomeCSS() {
        const css = `
            @font-face {
                font-family: "Font Awesome 6 Free";
                font-style: normal;
                font-weight: 900;
                font-display: block;
                src: url("/static/fontawesome/webfonts/fa-solid-900.woff2") format("woff2"),
                     url("/static/fontawesome/webfonts/fa-solid-900.ttf") format("truetype");
            }
            @font-face {
                font-family: "Font Awesome 6 Brands";
                font-style: normal;
                font-weight: 400;
                font-display: block;
                src: url("/static/fontawesome/webfonts/fa-brands-400.woff2") format("woff2"),
                     url("/static/fontawesome/webfonts/fa-brands-400.ttf") format("truetype");
            }
            .fas, .far, .fab, .fa {
                font-family: "Font Awesome 6 Free", "Font Awesome 6 Pro", "Font Awesome 6 Brands" !important;
                font-weight: 900 !important;
                font-style: normal !important;
                -webkit-font-smoothing: antialiased !important;
                -moz-osx-font-smoothing: grayscale !important;
            }
            .fab {
                font-family: "Font Awesome 6 Brands" !important;
                font-weight: 400 !important;
            }
            .far {
                font-family: "Font Awesome 6 Free" !important;
                font-weight: 400 !important;
            }
        `;
        
        // Add specific icon content rules
        Object.keys(iconMappings).forEach(iconClass => {
            css += `.${iconClass}:before { content: "${iconMappings[iconClass].code}" !important; }\n`;
        });
        
        Object.keys(brandIconMappings).forEach(iconClass => {
            css += `.${iconClass}:before { content: "${brandIconMappings[iconClass].code}" !important; }\n`;
        });
        
        const style = document.createElement('style');
        style.textContent = css;
        style.id = 'fontawesome-fix-css';
        document.head.appendChild(style);
    }
    
    function applyFallbackIcons() {
        document.querySelectorAll('i[class*="fa-"]').forEach(icon => {
            const classes = icon.className.split(' ');
            let fallbackIcon = null;
            
            for (let className of classes) {
                if (iconMappings[className]) {
                    fallbackIcon = iconMappings[className].unicode;
                    break;
                }
            }
            
            if (fallbackIcon) {
                icon.style.fontFamily = 'Arial, sans-serif';
                icon.style.fontSize = '1.2em';
                icon.textContent = fallbackIcon;
                console.log('Applied fallback for:', icon.className);
            }
        });
        
        // Handle brand icons
        document.querySelectorAll('i[class*="fab"]').forEach(icon => {
            const classes = icon.className.split(' ');
            if (classes.includes('fa-instagram')) {
                icon.style.fontFamily = 'Arial, sans-serif';
                icon.style.fontSize = '1.2em';
                icon.textContent = '📷';
            }
        });
    }
    
    function checkFontAwesomeStatus() {
        const testIcon = document.createElement('i');
        testIcon.className = 'fas fa-home';
        testIcon.style.position = 'absolute';
        testIcon.style.left = '-9999px';
        testIcon.style.visibility = 'hidden';
        testIcon.style.fontSize = '20px';
        document.body.appendChild(testIcon);
        
        const computedStyle = window.getComputedStyle(testIcon);
        const fontFamily = computedStyle.getPropertyValue('font-family');
        const content = window.getComputedStyle(testIcon, '::before').content;
        
        document.body.removeChild(testIcon);
        
        return {
            fontFamily: fontFamily,
            content: content,
            isWorking: fontFamily.includes('Font Awesome') && content !== 'none' && content !== '""'
        };
    }
    
    function fixIcons() {
        console.log('Starting Font Awesome icon fix...');
        
        // First, inject our CSS
        injectFontAwesomeCSS();
        
        // Wait for fonts to load
        setTimeout(() => {
            const status = checkFontAwesomeStatus();
            console.log('Font Awesome Status:', status);
            
            if (!status.isWorking) {
                console.warn('Font Awesome still not working, applying fallback icons');
                applyFallbackIcons();
            } else {
                console.log('Font Awesome is working correctly!');
            }
        }, 500);
    }
    
    // Run the fix when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', fixIcons);
    } else {
        fixIcons();
    }
    
    // Also run after a delay to catch any late-loading icons
    setTimeout(fixIcons, 2000);
    
})();
