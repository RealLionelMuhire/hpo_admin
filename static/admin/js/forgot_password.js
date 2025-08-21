// Add forgot password link to Django admin login page
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on the admin login page
    const loginForm = document.getElementById('login-form');
    const submitRow = document.querySelector('.submit-row');
    
    if (loginForm && submitRow && window.location.pathname.includes('/admin/login/')) {
        // Create the forgot password link
        const forgotPasswordDiv = document.createElement('div');
        forgotPasswordDiv.style.cssText = `
            text-align: center;
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #eee;
        `;
        
        const forgotPasswordLink = document.createElement('a');
        forgotPasswordLink.href = '/password_reset/';
        forgotPasswordLink.textContent = 'Forgotten your password?';
        forgotPasswordLink.style.cssText = `
            color: #447e9b;
            text-decoration: none;
            font-size: 11px;
            padding: 8px 16px;
            border: 1px solid #447e9b;
            border-radius: 4px;
            display: inline-block;
            transition: all 0.3s ease;
        `;
        
        // Add hover effect
        forgotPasswordLink.addEventListener('mouseenter', function() {
            this.style.backgroundColor = '#447e9b';
            this.style.color = 'white';
        });
        
        forgotPasswordLink.addEventListener('mouseleave', function() {
            this.style.backgroundColor = 'transparent';
            this.style.color = '#447e9b';
        });
        
        forgotPasswordDiv.appendChild(forgotPasswordLink);
        
        // Insert after the submit row
        submitRow.parentNode.insertBefore(forgotPasswordDiv, submitRow.nextSibling);
    }
});
