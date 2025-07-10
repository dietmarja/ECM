/**
 * DSCG Web Interface - Main JavaScript Application
 * ================================================
 * 
 * Global functionality for the Digital Sustainability Curriculum Generator web interface.
 * Handles common UI interactions, API communications, and utility functions.
 */

// Global application object
const DSCG = {
    config: {
        apiBaseUrl: '/api',
        pollInterval: 2000, // 2 seconds
        maxRetries: 3
    },
    
    state: {
        currentJob: null,
        roles: [],
        isLoading: false
    },
    
    // Initialize application
    init: function() {
        console.log('🚀 Initializing DSCG Web Interface v3.1');
        
        // Set up global event listeners
        this.setupEventListeners();
        
        // Load initial data
        this.loadRoles();
        
        // Setup periodic health check
        this.startHealthCheck();
        
        console.log('✅ DSCG Web Interface initialized successfully');
    },
    
    // Setup global event listeners
    setupEventListeners: function() {
        // Handle navigation active states
        this.updateActiveNavigation();
        
        // Setup toast notifications
        this.setupToastNotifications();
        
        // Handle form validations
        this.setupFormValidations();
        
        // Setup keyboard shortcuts
        this.setupKeyboardShortcuts();
    },
    
    // Update active navigation based on current page
    updateActiveNavigation: function() {
        const currentPath = window.location.pathname;
        const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
        
        navLinks.forEach(link => {
            const href = link.getAttribute('href');
            if (href && currentPath === href) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    },
    
    // Load available roles from API
    loadRoles: async function() {
        try {
            const response = await this.apiCall('GET', '/roles');
            this.state.roles = response.roles || [];
            console.log(`📋 Loaded ${this.state.roles.length} roles`);
        } catch (error) {
            console.error('❌ Failed to load roles:', error);
            this.showNotification('Failed to load roles', 'warning');
        }
    },
    
    // Generic API call wrapper
    apiCall: async function(method, endpoint, data = null) {
        const url = `${this.config.apiBaseUrl}${endpoint}`;
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            }
        };
        
        if (data) {
            options.body = JSON.stringify(data);
        }
        
        let retries = 0;
        while (retries < this.config.maxRetries) {
            try {
                const response = await fetch(url, options);
                
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                
                return await response.json();
            } catch (error) {
                retries++;
                if (retries >= this.config.maxRetries) {
                    throw error;
                }
                
                // Wait before retry
                await new Promise(resolve => setTimeout(resolve, 1000 * retries));
            }
        }
    },
    
    // Show notification/toast
    showNotification: function(message, type = 'info', duration = 5000) {
        // Create toast element
        const toastId = 'toast_' + Date.now();
        const toastHtml = `
            <div id="${toastId}" class="toast align-items-center text-white bg-${type}" role="alert">
                <div class="d-flex">
                    <div class="toast-body">
                        <i class="fas fa-${this.getIconForType(type)} me-2"></i>
                        ${message}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" 
                            data-bs-dismiss="toast"></button>
                </div>
            </div>
        `;
        
        // Add to toast container (create if doesn't exist)
        let toastContainer = document.getElementById('toastContainer');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.id = 'toastContainer';
            toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
            document.body.appendChild(toastContainer);
        }
        
        toastContainer.insertAdjacentHTML('beforeend', toastHtml);
        
        // Show toast
        const toastElement = document.getElementById(toastId);
        const toast = new bootstrap.Toast(toastElement, { delay: duration });
        toast.show();
        
        // Auto-remove after hide
        toastElement.addEventListener('hidden.bs.toast', () => {
            toastElement.remove();
        });
    },
    
    // Get appropriate icon for notification type
    getIconForType: function(type) {
        const icons = {
            'success': 'check-circle',
            'warning': 'exclamation-triangle',
            'danger': 'exclamation-circle',
            'info': 'info-circle',
            'primary': 'info-circle'
        };
        return icons[type] || 'info-circle';
    },
    
    // Setup toast notification system
    setupToastNotifications: function() {
        // Enable all tooltips
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
        
        // Enable all popovers
        const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
        popoverTriggerList.map(function(popoverTriggerEl) {
            return new bootstrap.Popover(popoverTriggerEl);
        });
    },
    
    // Setup form validations
    setupFormValidations: function() {
        // Add Bootstrap validation to all forms
        const forms = document.querySelectorAll('.needs-validation');
        Array.from(forms).forEach(form => {
            form.addEventListener('submit', event => {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            });
        });
    },
    
    // Setup keyboard shortcuts
    setupKeyboardShortcuts: function() {
        document.addEventListener('keydown', (event) => {
            // Ctrl/Cmd + G for generator
            if ((event.ctrlKey || event.metaKey) && event.key === 'g') {
                event.preventDefault();
                window.location.href = '/generator';
            }
            
            // Ctrl/Cmd + D for deliverables
            if ((event.ctrlKey || event.metaKey) && event.key === 'd') {
                event.preventDefault();
                window.location.href = '/deliverables';
            }
            
            // Ctrl/Cmd + S for status
            if ((event.ctrlKey || event.metaKey) && event.key === 's') {
                event.preventDefault();
                window.location.href = '/status';
            }
            
            // Escape to close modals
            if (event.key === 'Escape') {
                const openModals = document.querySelectorAll('.modal.show');
                openModals.forEach(modal => {
                    const modalInstance = bootstrap.Modal.getInstance(modal);
                    if (modalInstance) {
                        modalInstance.hide();
                    }
                });
            }
        });
    },
    
    // Start periodic health check
    startHealthCheck: function() {
        const checkHealth = async () => {
            try {
                const health = await this.apiCall('GET', '/health');
                this.updateHealthIndicator(health);
            } catch (error) {
                console.warn('Health check failed:', error);
                this.updateHealthIndicator({ status: 'unhealthy' });
            }
        };
        
        // Initial check
        checkHealth();
        
        // Periodic checks every 30 seconds
        setInterval(checkHealth, 30000);
    },
    
    // Update health indicator in UI
    updateHealthIndicator: function(health) {
        const indicators = document.querySelectorAll('.health-indicator');
        const statusClass = health.status === 'healthy' ? 'status-healthy' : 'status-error';
        
        indicators.forEach(indicator => {
            indicator.className = `status-indicator ${statusClass}`;
            indicator.title = `System ${health.status} - Last checked: ${new Date().toLocaleTimeString()}`;
        });
    },
    
    // Poll job status
    pollJobStatus: async function(jobId, callback) {
        const poll = async () => {
            try {
                const job = await this.apiCall('GET', `/jobs/${jobId}`);
                callback(job);
                
                if (job.status === 'completed' || job.status === 'failed') {
                    return; // Stop polling
                }
                
                // Continue polling
                setTimeout(poll, this.config.pollInterval);
            } catch (error) {
                console.error('Error polling job status:', error);
                callback({ status: 'failed', message: 'Failed to get job status' });
            }
        };
        
        poll();
    },
    
    // Format file size
    formatFileSize: function(bytes) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },
    
    // Format duration
    formatDuration: function(startTime, endTime = null) {
        const start = new Date(startTime);
        const end = endTime ? new Date(endTime) : new Date();
        const duration = end - start;
        
        const seconds = Math.floor(duration / 1000);
        const minutes = Math.floor(seconds / 60);
        const hours = Math.floor(minutes / 60);
        
        if (hours > 0) {
            return `${hours}h ${minutes % 60}m ${seconds % 60}s`;
        } else if (minutes > 0) {
            return `${minutes}m ${seconds % 60}s`;
        } else {
            return `${seconds}s`;
        }
    },
    
    // Copy text to clipboard
    copyToClipboard: async function(text) {
        try {
            await navigator.clipboard.writeText(text);
            this.showNotification('Copied to clipboard', 'success');
        } catch (error) {
            console.error('Failed to copy to clipboard:', error);
            this.showNotification('Failed to copy to clipboard', 'warning');
        }
    },
    
    // Download file
    downloadFile: function(filename) {
        const link = document.createElement('a');
        link.href = `/api/download/${filename}`;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    },
    
    // Debounce function for search inputs
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    // Loading state management
    setLoading: function(isLoading, element = null) {
        this.state.isLoading = isLoading;
        
        if (element) {
            if (isLoading) {
                element.disabled = true;
                const originalText = element.textContent;
                element.dataset.originalText = originalText;
                element.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
            } else {
                element.disabled = false;
                element.textContent = element.dataset.originalText || 'Submit';
            }
        }
    },
    
    // Validate form data
    validateFormData: function(formData, requiredFields) {
        const errors = [];
        
        requiredFields.forEach(field => {
            if (!formData[field] || formData[field].toString().trim() === '') {
                errors.push(`${field.replace('_', ' ').toUpperCase()} is required`);
            }
        });
        
        return errors;
    }
};

// Initialize application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    DSCG.init();
});

// Global utility functions
window.DSCG = DSCG;

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DSCG;
}
