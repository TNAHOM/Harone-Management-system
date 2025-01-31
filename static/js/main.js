// Form Validation
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
});

// File Upload Preview
document.querySelectorAll('input[type="file"]').forEach(input => {
    input.addEventListener('change', function(e) {
        const fileName = e.target.files[0]?.name;
        const label = e.target.nextElementSibling;
        if (label && fileName) {
            label.textContent = fileName;
        }
    });
});

// Password Confirmation Check
function validatePassword() {
    const password = document.getElementById('password');
    const confirmPassword = document.getElementById('confirm_password');
    
    if (password && confirmPassword) {
        if (password.value !== confirmPassword.value) {
            confirmPassword.setCustomValidity("Passwords don't match");
        } else {
            confirmPassword.setCustomValidity('');
        }
    }
}

// Toast Notifications
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast show bg-${type} text-white`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    toast.innerHTML = `
        <div class="toast-header">
            <strong class="me-auto">Notification</strong>
            <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
        </div>
        <div class="toast-body">
            ${message}
        </div>
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 5000);
}

// Request Status Updates
function updateRequestStatus(requestId, status) {
    const row = document.querySelector(`tr[data-request-id="${requestId}"]`);
    if (row) {
        const statusBadge = row.querySelector('.badge');
        statusBadge.className = `badge bg-${status === 'approved' ? 'success' : 'danger'}`;
        statusBadge.textContent = status.charAt(0).toUpperCase() + status.slice(1);
    }
}

// Document Preview
function previewDocument(url) {
    const modal = document.getElementById('documentPreviewModal');
    const iframe = modal.querySelector('iframe');
    
    if (iframe) {
        iframe.src = url;
    }
    
    const previewModal = new bootstrap.Modal(modal);
    previewModal.show();
}

// Form Reset
function resetForm(formId) {
    const form = document.getElementById(formId);
    if (form) {
        form.reset();
        form.classList.remove('was-validated');
    }
}

// Dynamic Table Sorting
function sortTable(columnIndex) {
    const table = document.querySelector('table');
    const rows = Array.from(table.querySelectorAll('tbody tr'));
    const headers = table.querySelectorAll('th');
    const header = headers[columnIndex];
    const ascending = header.classList.contains('sort-asc');
    
    // Reset all headers
    headers.forEach(h => h.classList.remove('sort-asc', 'sort-desc'));
    
    // Sort rows
    rows.sort((a, b) => {
        const aValue = a.cells[columnIndex].textContent;
        const bValue = b.cells[columnIndex].textContent;
        return ascending ? 
            bValue.localeCompare(aValue) : 
            aValue.localeCompare(bValue);
    });
    
    // Update header class
    header.classList.add(ascending ? 'sort-desc' : 'sort-asc');
    
    // Reorder rows
    rows.forEach(row => table.querySelector('tbody').appendChild(row));
}

// Search/Filter Functionality
function filterTable(input) {
    const searchText = input.value.toLowerCase();
    const table = document.querySelector('table');
    const rows = table.querySelectorAll('tbody tr');
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(searchText) ? '' : 'none';
    });
}

// Export to CSV
function exportToCSV() {
    const table = document.querySelector('table');
    const rows = table.querySelectorAll('tr');
    let csv = [];
    
    rows.forEach(row => {
        const cells = row.querySelectorAll('td, th');
        const rowData = Array.from(cells).map(cell => {
            return `"${cell.textContent.replace(/"/g, '""')}"`;
        });
        csv.push(rowData.join(','));
    });
    
    const csvContent = csv.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.setAttribute('download', 'export.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Responsive Table
function makeTableResponsive() {
    const tables = document.querySelectorAll('table');
    tables.forEach(table => {
        const headers = Array.from(table.querySelectorAll('th')).map(th => th.textContent);
        const rows = table.querySelectorAll('tbody tr');
        
        rows.forEach(row => {
            const cells = row.querySelectorAll('td');
            cells.forEach((cell, index) => {
                cell.setAttribute('data-label', headers[index]);
            });
        });
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    makeTableResponsive();
}); 