document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    try {
        const response = await fetch('http://localhost:5000/api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();
        
        if (response.ok) {
            // Store the token
            localStorage.setItem('token', data.token);
            // Redirect to home page
            window.location.href = '../HTML/home.html';
        } else {
            alert(data.message || 'خطأ في تسجيل الدخول');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('حدث خطأ في الاتصال بالخادم');
    }
});