document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const errorMessage = document.getElementById('error-message');
    
    // Coloque aqui a URL base da sua API no PythonAnywhere
    const API_URL = window.location.origin;

    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault(); // Impede o recarregamento da página
        errorMessage.classList.add('d-none'); // Esconde mensagens de erro antigas

        const formData = new URLSearchParams();
        formData.append('username', document.getElementById('username').value);
        formData.append('password', document.getElementById('password').value);

        try {
            const response = await fetch(`${API_URL}/token`, {
                method: 'POST',
                body: formData,
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('accessToken', data.access_token);
                // Redireciona para a página principal de consulta
                window.location.href = 'index.html';
            } else {
                errorMessage.classList.remove('d-none');
            }
        } catch (error) {
            console.error('Erro ao conectar com a API:', error);
            errorMessage.textContent = 'Erro de conexão. Tente novamente mais tarde.';
            errorMessage.classList.remove('d-none');
        }
    });
});