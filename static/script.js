const container = document.querySelector('.container');
const registerBtn = document.querySelector('.register-btn');
const loginBtn = document.querySelector('.login-btn');
const toggleLeft = document.querySelector('.toggle-left');

if (registerBtn && loginBtn) {
    registerBtn.addEventListener('click', () => {
        container.classList.add('active');
       
        registerBtn.classList.add('hidden');
        toggleLeft.classList.add('hidden');
    });

    loginBtn.addEventListener('click', () => {
        container.classList.remove('active');       
        registerBtn.classList.remove('hidden');
        toggleLeft.classList.remove('hidden');
    });
}

document.getElementById('registerForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const cpf = document.getElementById('registerCpf').value;
    const nome = document.getElementById('registerNome').value;
    const senha = document.getElementById('registerSenha').value;

    console.log("Dados do formulário:", { cpf, nome, senha }); // Log dos dados

    // Fetch p/ o Flask
    fetch('http://127.0.0.1:5000/cadastrar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ cpf: cpf, nome: nome, senha: senha }),
    })
    .then(response => response.json())
    .then(data => {
        console.log("Resposta do servidor:", data);
        alert(data.message);
        if (data.message === "Cliente cadastrado com sucesso") {
            // Redirecionar p/ a tela de login
        }
    })
    .catch((error) => {
        console.error('Erro:', error);
    });
});

document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const cpf = document.getElementById('loginCpf').value;
    const senha = document.getElementById('loginSenha').value;

    console.log("Dados do formulário de login:", { cpf, senha }); // Log dos dados

    // Fetch p/ o Flask so q/ do login
    fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ cpf: cpf, senha: senha }),
    })
    .then(response => response.json())
    .then(data => {
        console.log("Resposta do servidor:", data); // Log da resposta
        if (data.message === "Login bem-sucedido") {
            // Armazena o nome do usuário no localStorage
            localStorage.setItem('username', data.nome);
            // Redireciona p/ a página home
            window.location.href = '/home';
        } else {
            alert(data.message); // Mensagem de erro
        }
    })
    .catch((error) => {
        console.error('Erro:', error);
    });
});

// Sair 
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM completamente carregado e analisado");
    document.getElementById('sairBtn').addEventListener('click', function() {
        console.log("Botão Sair clicado");
        fetch('http://127.0.0.1:5000/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => {
            console.log("Resposta recebida:", response);
            return response.json();
        })
        .then(data => {
            console.log("Resposta do servidor:", data);
            if (data.message === "Logout realizado com sucesso") {
                localStorage.removeItem('username');
                window.location.href = '/';
            } else {
                alert(data.message);
            }
        })
        .catch((error) => {
            console.error('Erro:', error);
        });
    });
});