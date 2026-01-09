
    // Auto-hide messages
    document.addEventListener('DOMContentLoaded', function() {
        setTimeout(function() {
            let messages = document.getElementById('messages');
            if (messages) {
                messages.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
                messages.style.opacity = '0';
                messages.style.transform = 'translateY(-20px)';
                setTimeout(() => messages.remove(), 500);
            }
        }, 5000);
    });
    
    // Loading overlay functions
    function showLoading() {
        document.getElementById('loadingOverlay').classList.add('show');
    }
    
    function hideLoading() {
        document.getElementById('loadingOverlay').classList.remove('show');
    }
    
    // Show loading on form submissions
    document.addEventListener('submit', function() {
        showLoading();
    });
    
    // Hide loading when page loads
    window.addEventListener('load', function() {
        hideLoading();
    });
    
    // Initialize Select2
    $(document).ready(function() {
        $('.select2').select2({
            theme: 'bootstrap-5',
            placeholder: 'Selecione...'
        });
    });