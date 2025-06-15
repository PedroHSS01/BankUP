 // Recupera o nome do usuário do localStorage
const username = localStorage.getItem('username');
if (username) {
    document.getElementById('username').textContent = username;
} else {
    // Redireciona para a página de login se ñ tiver nome armazenado
    window.location.href = '/';
}

// Adiciona o evento de clique ao botão de sair
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM completamente carregado e analisado");
    const sairBtn = document.getElementById('sairBtn');
    if (sairBtn) {
        console.log("Botão Sair encontrado no DOM");
        sairBtn.addEventListener('click', function() {
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
    } else {
        console.error("Botão Sair não encontrado no DOM");
    }
});


document.addEventListener("DOMContentLoaded", function() {
    fetch("http://localhost:5000/cotacoes")
        .then(response => response.json())
        .then(data => {
            document.getElementById("dolar").querySelector(".moeda-valor").textContent = 
                `R$ ${parseFloat(data.dolar).toFixed(2)}`;
            document.getElementById("euro").querySelector(".moeda-valor").textContent = 
                `R$ ${parseFloat(data.euro).toFixed(2)}`;
            document.getElementById("bitcoin").querySelector(".moeda-valor").textContent = 
                `R$ ${parseFloat(data.bitcoin).toFixed(2)}`;
        })
        .catch(error => {
            console.error("Erro ao buscar cotações:", error);
            document.querySelectorAll(".moeda-valor").forEach(el => {
                el.textContent = "Erro ao carregar";
            });
        });
});