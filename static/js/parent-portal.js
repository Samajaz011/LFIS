
// Enhanced Parent Portal JavaScript

document.addEventListener('DOMContentLoaded', function() {
    initParentPortal();
    initAnimations();
    initInteractivity();
    initMobileMenu();
    initLoadingStates();
});

function initParentPortal() {
    // Add fade-in classes to elements
    const cards = document.querySelectorAll('.card');
    const stats = document.querySelectorAll('.stat-card');
    
    cards.forEach((card, index) => {
        card.classList.add('fade-in');
        setTimeout(() => {
            card.classList.add('visible');
        }, 100 * index);
    });
    
    stats.forEach((stat, index) => {
        stat.classList.add('slide-in-left');
        setTimeout(() => {
            stat.classList.add('visible');
        }, 150 * index);
    });
}

function initAnimations() {
    // Intersection Observer for animations
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                
                // Animate counters
                if (entry.target.classList.contains('stat-number')) {
                    animateCounter(entry.target);
                }
                
                // Animate progress bars
                if (entry.target.classList.contains('progress-bar')) {
                    animateProgressBar(entry.target);
                }
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    // Observe elements
    document.querySelectorAll('.fade-in, .slide-in-left, .slide-in-right, .stat-number, .progress-bar').forEach(el => {
        observer.observe(el);
    });
}

function animateCounter(element) {
    const target = parseInt(element.textContent.replace(/[^\d]/g, ''));
    const duration = 2000;
    const increment = target / (duration / 16);
    let current = 0;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        
        let suffix = '';
        if (element.textContent.includes('%')) suffix = '%';
        if (element.textContent.includes('+')) suffix = '+';
        
        element.textContent = Math.floor(current) + suffix;
    }, 16);
}

function animateProgressBar(element) {
    const targetWidth = element.style.width || element.getAttribute('aria-valuenow') + '%';
    element.style.width = '0%';
    
    setTimeout(() => {
        element.style.transition = 'width 2s ease-in-out';
        element.style.width = targetWidth;
    }, 100);
}

function initInteractivity() {
    // Enhanced hover effects for cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
            this.style.boxShadow = '0 15px 40px rgba(0, 0, 0, 0.15)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
            this.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.08)';
        });
    });
    
    // Enhanced button effects
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Ripple effect
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.cssText = `
                position: absolute;
                width: ${size}px;
                height: ${size}px;
                left: ${x}px;
                top: ${y}px;
                background: rgba(255, 255, 255, 0.5);
                border-radius: 50%;
                transform: scale(0);
                animation: ripple 0.6s ease-out;
                pointer-events: none;
            `;
            
            this.style.position = 'relative';
            this.style.overflow = 'hidden';
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
    
    // Table row interactions
    const tableRows = document.querySelectorAll('.table tbody tr');
    tableRows.forEach(row => {
        row.addEventListener('click', function() {
            // Remove active class from other rows
            tableRows.forEach(r => r.classList.remove('table-active'));
            // Add active class to clicked row
            this.classList.add('table-active');
        });
    });
}

function initMobileMenu() {
    // Mobile sidebar toggle
    const sidebarToggle = document.createElement('button');
    sidebarToggle.innerHTML = '<i class="fas fa-bars"></i>';
    sidebarToggle.className = 'btn btn-primary d-md-none position-fixed';
    sidebarToggle.style.cssText = `
        top: 1rem;
        left: 1rem;
        z-index: 1001;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        border: none;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    `;
    
    document.body.appendChild(sidebarToggle);
    
    sidebarToggle.addEventListener('click', function() {
        const sidebar = document.querySelector('.sidebar');
        sidebar.classList.toggle('show');
        
        // Toggle icon
        const icon = this.querySelector('i');
        if (sidebar.classList.contains('show')) {
            icon.className = 'fas fa-times';
        } else {
            icon.className = 'fas fa-bars';
        }
    });
    
    // Close sidebar when clicking outside
    document.addEventListener('click', function(e) {
        const sidebar = document.querySelector('.sidebar');
        const toggle = sidebarToggle;
        
        if (!sidebar.contains(e.target) && !toggle.contains(e.target)) {
            sidebar.classList.remove('show');
            toggle.querySelector('i').className = 'fas fa-bars';
        }
    });
}

function initLoadingStates() {
    // Add loading states to forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            showParentLoading();
            
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
                submitBtn.disabled = true;
                
                // Restore button after 3 seconds if still on page
                setTimeout(() => {
                    if (document.body.contains(submitBtn)) {
                        submitBtn.innerHTML = originalText;
                        submitBtn.disabled = false;
                        hideParentLoading();
                    }
                }, 3000);
            }
        });
    });
    
    // Add loading states to navigation links
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (this.href && !this.href.includes('#')) {
                showParentLoading();
            }
        });
    });
}

function showParentLoading() {
    let loading = document.getElementById('parentLoading');
    if (!loading) {
        loading = document.createElement('div');
        loading.id = 'parentLoading';
        loading.className = 'loading-overlay';
        loading.innerHTML = `
            <div class="loading-spinner">
                <div class="loading-animation">
                    <div class="pulse-ring"></div>
                    <div class="pulse-ring pulse-ring-delay-1"></div>
                    <div class="pulse-ring pulse-ring-delay-2"></div>
                    <div class="school-logo-loading">
                        <img src="/static/images/school_logo.png" alt="Loading">
                    </div>
                </div>
                <div class="loading-text mt-4">
                    <h5 class="mb-2">Parent Portal</h5>
                    <p class="mb-3 opacity-75">Loading...</p>
                    <div class="loading-dots">
                        <span></span><span></span><span></span>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(loading);
    }
    
    loading.style.display = 'flex';
    loading.classList.remove('hidden');
}

function hideParentLoading() {
    const loading = document.getElementById('parentLoading');
    if (loading) {
        loading.classList.add('hidden');
        setTimeout(() => {
            loading.style.display = 'none';
        }, 500);
    }
}

// Utility functions
const ParentPortal = {
    showNotification: function(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} notification position-fixed`;
        notification.style.cssText = `
            top: 20px;
            right: 20px;
            z-index: 10000;
            max-width: 400px;
            opacity: 0;
            transform: translateX(100%);
            transition: all 0.3s ease;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        `;
        
        notification.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'danger' ? 'exclamation-circle' : 'info-circle'} me-2"></i>
                <span>${message}</span>
                <button type="button" class="btn-close ms-auto" onclick="this.parentElement.parentElement.remove()"></button>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.style.opacity = '1';
            notification.style.transform = 'translateX(0)';
        }, 100);
        
        // Auto remove
        setTimeout(() => {
            if (document.body.contains(notification)) {
                notification.style.opacity = '0';
                notification.style.transform = 'translateX(100%)';
                setTimeout(() => {
                    if (document.body.contains(notification)) {
                        notification.remove();
                    }
                }, 300);
            }
        }, 5000);
    },
    
    formatDate: function(date) {
        return new Date(date).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    },
    
    calculateGrade: function(percentage) {
        if (percentage >= 90) return 'A+';
        if (percentage >= 80) return 'A';
        if (percentage >= 70) return 'B+';
        if (percentage >= 60) return 'B';
        if (percentage >= 50) return 'C+';
        if (percentage >= 40) return 'C';
        return 'F';
    }
};

// Add ripple animation CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple {
        to {
            transform: scale(2);
            opacity: 0;
        }
    }
    
    .table-active {
        background-color: rgba(46, 134, 171, 0.1) !important;
        border-left: 4px solid var(--parent-primary) !important;
    }
`;
document.head.appendChild(style);

// Export for global use
window.ParentPortal = ParentPortal;
