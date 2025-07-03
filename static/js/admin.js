// Admin Panel JavaScript

document.addEventListener('DOMContentLoaded', function() {
    initSidebar();
    initDataTables();
    initFormValidation();
    initFileUpload();
    initConfirmations();
    initTooltips();
    initCharacterCounters();
    initAutoSave();
    initBulkActions();
});

// Sidebar functionality
function initSidebar() {
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.querySelector('.sidebar');
    const mainContent = document.querySelector('.main-content');

    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function() {
            if (window.innerWidth <= 768) {
                sidebar.classList.toggle('show');
                
                // Add overlay for mobile
                if (sidebar.classList.contains('show')) {
                    const overlay = document.createElement('div');
                    overlay.className = 'sidebar-overlay';
                    overlay.style.cssText = `
                        position: fixed;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 100%;
                        background: rgba(0, 0, 0, 0.5);
                        z-index: 999;
                    `;
                    document.body.appendChild(overlay);
                    
                    overlay.addEventListener('click', function() {
                        sidebar.classList.remove('show');
                        document.body.removeChild(overlay);
                    });
                } else {
                    const overlay = document.querySelector('.sidebar-overlay');
                    if (overlay) {
                        document.body.removeChild(overlay);
                    }
                }
            }
        });
    }

    // Auto-collapse sidebar on mobile when clicking menu items
    const menuLinks = document.querySelectorAll('.menu-link');
    menuLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (window.innerWidth <= 768 && sidebar) {
                sidebar.classList.remove('show');
                const overlay = document.querySelector('.sidebar-overlay');
                if (overlay) {
                    document.body.removeChild(overlay);
                }
            }
        });
    });

    // Highlight active menu item
    const currentPath = window.location.pathname;
    menuLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
}

// Enhanced DataTables (if library is loaded)
function initDataTables() {
    const tables = document.querySelectorAll('.data-table');
    
    tables.forEach(table => {
        // Add sorting functionality
        const headers = table.querySelectorAll('th[data-sortable]');
        headers.forEach(header => {
            header.style.cursor = 'pointer';
            header.addEventListener('click', function() {
                sortTable(table, header);
            });
        });

        // Add search functionality
        addTableSearch(table);
    });
}

// Simple table sorting
function sortTable(table, header) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const columnIndex = Array.from(header.parentNode.children).indexOf(header);
    const isAscending = !header.classList.contains('sort-asc');

    rows.sort((a, b) => {
        const aValue = a.children[columnIndex].textContent.trim();
        const bValue = b.children[columnIndex].textContent.trim();
        
        if (isNumeric(aValue) && isNumeric(bValue)) {
            return isAscending ? 
                parseFloat(aValue) - parseFloat(bValue) : 
                parseFloat(bValue) - parseFloat(aValue);
        }
        
        return isAscending ? 
            aValue.localeCompare(bValue) : 
            bValue.localeCompare(aValue);
    });

    // Update header classes
    header.parentNode.querySelectorAll('th').forEach(h => {
        h.classList.remove('sort-asc', 'sort-desc');
    });
    header.classList.add(isAscending ? 'sort-asc' : 'sort-desc');

    // Reorder rows
    rows.forEach(row => tbody.appendChild(row));
}

// Check if value is numeric
function isNumeric(value) {
    return !isNaN(parseFloat(value)) && isFinite(value);
}

// Add search functionality to table
function addTableSearch(table) {
    const searchInput = document.createElement('input');
    searchInput.type = 'text';
    searchInput.placeholder = 'Search...';
    searchInput.className = 'form-control form-control-sm mb-3';
    
    table.parentNode.insertBefore(searchInput, table);
    
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const rows = table.querySelectorAll('tbody tr');
        
        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(searchTerm) ? '' : 'none';
        });
    });
}

// Enhanced form validation
function initFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
                
                // Scroll to first error
                const firstError = form.querySelector(':invalid');
                if (firstError) {
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    firstError.focus();
                }
            }
            
            form.classList.add('was-validated');
        });

        // Real-time validation
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('blur', validateField);
            input.addEventListener('input', validateField);
        });
    });
}

function validateField(e) {
    const field = e.target;
    const feedback = field.parentNode.querySelector('.invalid-feedback') || 
                    field.parentNode.querySelector('.valid-feedback');
    
    if (field.checkValidity()) {
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
        if (feedback) feedback.style.display = 'none';
    } else {
        field.classList.remove('is-valid');
        field.classList.add('is-invalid');
        if (feedback) feedback.style.display = 'block';
    }
}

// File upload handling
function initFileUpload() {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(input => {
        input.addEventListener('change', function() {
            handleFileUpload(this);
        });
        
        // Add drag and drop
        const parent = input.closest('.form-group') || input.parentNode;
        addDragAndDrop(parent, input);
    });
}

function handleFileUpload(input) {
    const file = input.files[0];
    if (!file) return;

    // Validate file size (16MB limit)
    if (file.size > 16 * 1024 * 1024) {
        showAlert('File size must be less than 16MB', 'danger');
        input.value = '';
        return;
    }

    // Validate file type
    const allowedTypes = input.accept ? input.accept.split(',').map(t => t.trim()) : [];
    if (allowedTypes.length > 0) {
        const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
        if (!allowedTypes.includes(fileExtension)) {
            showAlert('Invalid file type', 'danger');
            input.value = '';
            return;
        }
    }

    // Show file info
    showFileInfo(input, file);
}

function showFileInfo(input, file) {
    let infoDiv = input.parentNode.querySelector('.file-info');
    if (!infoDiv) {
        infoDiv = document.createElement('div');
        infoDiv.className = 'file-info mt-2';
        input.parentNode.appendChild(infoDiv);
    }

    const fileSize = formatFileSize(file.size);
    infoDiv.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="fas fa-file me-2 text-primary"></i>
            <span>${file.name} (${fileSize})</span>
            <button type="button" class="btn btn-sm btn-outline-danger ms-auto" onclick="clearFile(this)">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
}

function clearFile(button) {
    const infoDiv = button.closest('.file-info');
    const input = infoDiv.parentNode.querySelector('input[type="file"]');
    input.value = '';
    infoDiv.remove();
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Drag and drop functionality
function addDragAndDrop(element, input) {
    element.addEventListener('dragover', function(e) {
        e.preventDefault();
        element.classList.add('drag-over');
    });

    element.addEventListener('dragleave', function(e) {
        e.preventDefault();
        element.classList.remove('drag-over');
    });

    element.addEventListener('drop', function(e) {
        e.preventDefault();
        element.classList.remove('drag-over');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            input.files = files;
            handleFileUpload(input);
        }
    });
}

// Confirmation dialogs
function initConfirmations() {
    const deleteButtons = document.querySelectorAll('[data-confirm]');
    
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm') || 'Are you sure?';
            if (!confirm(message)) {
                e.preventDefault();
                return false;
            }
        });
    });
}

// Initialize tooltips
function initTooltips() {
    const tooltipElements = document.querySelectorAll('[title]');
    
    tooltipElements.forEach(element => {
        const title = element.getAttribute('title');
        element.removeAttribute('title');
        element.setAttribute('data-bs-toggle', 'tooltip');
        element.setAttribute('data-bs-title', title);
    });

    // Initialize Bootstrap tooltips if available
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltipList = [...tooltipElements].map(tooltipTriggerEl => 
            new bootstrap.Tooltip(tooltipTriggerEl)
        );
    }
}

// Character counters for text fields
function initCharacterCounters() {
    const textareas = document.querySelectorAll('textarea[maxlength]');
    
    textareas.forEach(textarea => {
        const maxLength = parseInt(textarea.getAttribute('maxlength'));
        const counter = document.createElement('small');
        counter.className = 'text-muted character-counter';
        textarea.parentNode.appendChild(counter);
        
        function updateCounter() {
            const remaining = maxLength - textarea.value.length;
            counter.textContent = `${remaining} characters remaining`;
            counter.className = remaining < 50 ? 'text-warning character-counter' : 'text-muted character-counter';
        }
        
        textarea.addEventListener('input', updateCounter);
        updateCounter();
    });
}

// Auto-save functionality
function initAutoSave() {
    const forms = document.querySelectorAll('form[data-autosave]');
    
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, textarea, select');
        let saveTimeout;
        
        inputs.forEach(input => {
            input.addEventListener('input', function() {
                clearTimeout(saveTimeout);
                saveTimeout = setTimeout(() => {
                    autoSaveForm(form);
                }, 2000);
            });
        });
        
        // Load saved data on page load
        loadAutoSavedData(form);
    });
}

function autoSaveForm(form) {
    const formData = new FormData(form);
    const data = {};
    
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }
    
    const formId = form.getAttribute('id') || 'form';
    localStorage.setItem(`autosave_${formId}`, JSON.stringify(data));
    
    // Show save indicator
    showSaveIndicator('Draft saved');
}

function loadAutoSavedData(form) {
    const formId = form.getAttribute('id') || 'form';
    const savedData = localStorage.getItem(`autosave_${formId}`);
    
    if (savedData) {
        const data = JSON.parse(savedData);
        
        Object.keys(data).forEach(key => {
            const field = form.querySelector(`[name="${key}"]`);
            if (field && field.type !== 'file') {
                field.value = data[key];
            }
        });
        
        showSaveIndicator('Draft loaded');
    }
}

function showSaveIndicator(message) {
    let indicator = document.querySelector('.save-indicator');
    if (!indicator) {
        indicator = document.createElement('div');
        indicator.className = 'save-indicator';
        indicator.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #28a745;
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 4px;
            z-index: 10000;
            opacity: 0;
            transition: opacity 0.3s ease;
        `;
        document.body.appendChild(indicator);
    }
    
    indicator.textContent = message;
    indicator.style.opacity = '1';
    
    setTimeout(() => {
        indicator.style.opacity = '0';
    }, 2000);
}

// Bulk actions
function initBulkActions() {
    const selectAll = document.querySelector('#selectAll');
    const checkboxes = document.querySelectorAll('input[name="selected[]"]');
    const bulkActions = document.querySelector('.bulk-actions');
    
    if (selectAll && checkboxes.length > 0) {
        selectAll.addEventListener('change', function() {
            checkboxes.forEach(cb => {
                cb.checked = this.checked;
            });
            toggleBulkActions();
        });
        
        checkboxes.forEach(cb => {
            cb.addEventListener('change', toggleBulkActions);
        });
    }
    
    function toggleBulkActions() {
        const selectedCount = document.querySelectorAll('input[name="selected[]"]:checked').length;
        if (bulkActions) {
            bulkActions.style.display = selectedCount > 0 ? 'block' : 'none';
        }
        
        // Update select all state
        if (selectAll) {
            selectAll.indeterminate = selectedCount > 0 && selectedCount < checkboxes.length;
            selectAll.checked = selectedCount === checkboxes.length;
        }
    }
}

// Alert system
function showAlert(message, type = 'info', duration = 5000) {
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show admin-alert`;
    alert.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 10000;
        max-width: 400px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    `;
    
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alert);
    
    // Auto remove
    if (duration > 0) {
        setTimeout(() => {
            if (document.body.contains(alert)) {
                alert.remove();
            }
        }, duration);
    }
}

// Loading states
function showLoading(element, text = 'Loading...') {
    if (element) {
        element.innerHTML = `
            <div class="d-flex align-items-center">
                <div class="spinner-border spinner-border-sm me-2" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                ${text}
            </div>
        `;
        element.style.pointerEvents = 'none';
    }
}

function hideLoading(element, originalContent) {
    if (element) {
        element.innerHTML = originalContent;
        element.style.pointerEvents = 'auto';
    }
}

// AJAX form submission
function submitFormAjax(form, successCallback, errorCallback) {
    const formData = new FormData(form);
    const submitButton = form.querySelector('button[type="submit"]');
    const originalContent = submitButton?.innerHTML;
    
    if (submitButton) {
        showLoading(submitButton, 'Saving...');
    }
    
    fetch(form.action, {
        method: form.method || 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert(data.message || 'Success!', 'success');
            if (successCallback) successCallback(data);
        } else {
            showAlert(data.message || 'An error occurred', 'danger');
            if (errorCallback) errorCallback(data);
        }
    })
    .catch(error => {
        showAlert('Network error occurred', 'danger');
        if (errorCallback) errorCallback(error);
    })
    .finally(() => {
        if (submitButton && originalContent) {
            hideLoading(submitButton, originalContent);
        }
    });
}

// Utility functions
const AdminUtils = {
    // Confirm deletion
    confirmDelete: function(message = 'Are you sure you want to delete this item?') {
        return confirm(message);
    },
    
    // Format date for display
    formatDate: function(date) {
        return new Date(date).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    },
    
    // Generate slug from title
    slugify: function(text) {
        return text.toLowerCase()
            .replace(/[^\w ]+/g, '')
            .replace(/ +/g, '-');
    },
    
    // Copy to clipboard
    copyToClipboard: function(text) {
        navigator.clipboard.writeText(text).then(() => {
            showAlert('Copied to clipboard!', 'success', 2000);
        });
    }
};

// Export for global use
window.AdminPanel = {
    showAlert,
    showLoading,
    hideLoading,
    submitFormAjax,
    AdminUtils
};

// Clear auto-saved data when form is successfully submitted
document.addEventListener('submit', function(e) {
    const form = e.target;
    if (form.hasAttribute('data-autosave')) {
        const formId = form.getAttribute('id') || 'form';
        localStorage.removeItem(`autosave_${formId}`);
    }
});
