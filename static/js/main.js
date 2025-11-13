// Main JavaScript for API Performance Monitor

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Generic AJAX function
    function ajaxRequest(url, method, data, callback) {
        const xhr = new XMLHttpRequest();
        xhr.open(method, url, true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    callback(null, JSON.parse(xhr.responseText));
                } else {
                    callback(new Error('Request failed with status ' + xhr.status));
                }
            }
        };
        xhr.send(JSON.stringify(data));
    }
    
    // Update metrics periodically
    function updateMetrics() {
        // In a real implementation, this would fetch data from your backend
        console.log('Updating metrics...');
    }
    
    // Set interval to update metrics every 30 seconds
    setInterval(updateMetrics, 30000);
    
    // Handle sidebar navigation
    const sidebarLinks = document.querySelectorAll('.sidebar .nav-link');
    const currentPage = window.location.pathname;
    
    sidebarLinks.forEach(link => {
        // Remove active class from all links
        link.classList.remove('active');
        
        // Add active class to current page link
        if (link.getAttribute('href') === currentPage) {
            link.classList.add('active');
        }
        
        // Add click event listener
        link.addEventListener('click', function(e) {
            // Remove active class from all links
            sidebarLinks.forEach(l => l.classList.remove('active'));
            // Add active class to clicked link
            this.classList.add('active');
        });
    });
    
    // Handle mobile menu toggle
    const menuToggle = document.querySelector('.navbar-toggler');
    if (menuToggle) {
        menuToggle.addEventListener('click', function() {
            const sidebar = document.querySelector('.sidebar');
            if (sidebar) {
                sidebar.classList.toggle('show');
            }
        });
    }
    
    // Export functionality
    const exportButtons = document.querySelectorAll('[data-export]');
    exportButtons.forEach(button => {
        button.addEventListener('click', function() {
            const format = this.getAttribute('data-export');
            alert(`Exporting data as ${format.toUpperCase()}...`);
            // In a real implementation, this would trigger the actual export
        });
    });
});

// Utility functions
function formatDate(date) {
    return new Date(date).toLocaleString();
}

function formatResponseTime(ms) {
    if (ms < 1000) {
        return `${Math.round(ms)}ms`;
    } else {
        return `${(ms / 1000).toFixed(2)}s`;
    }
}

function getStatusBadgeClass(statusCode) {
    if (statusCode >= 200 && statusCode < 300) {
        return 'status-success';
    } else if (statusCode >= 400 && statusCode < 500) {
        return 'status-error';
    } else if (statusCode >= 500) {
        return 'status-error';
    } else {
        return 'status-warning';
    }
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.role = 'alert';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    // Add to body
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 5000);
}

// Function to refresh monitored APIs in sidebar
function refreshSidebarApis() {
    // This function will be called from other pages to refresh the sidebar
    if (typeof loadMonitoredApisSidebar === 'function') {
        loadMonitoredApisSidebar();
    }
}