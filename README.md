# [Prévia] 🏦 Sistema bancário simplificado.💰

O objetivo do projeto é desenvolver um sistema bancário simples, aplicando métodos e ferramentas úteis para um bom desempenho.  A fim de treinar e aplicar programação em um projeto real.

Um sistema bancário funcional desenvolvido como evolução de um projeto acadêmico da DIO. Partindo de um desafio escolar que rodava apenas no terminal, decidi expandir o projeto para um sistema real. 

# Funcionalidades ⚙️
| Funcionalidade               | Descrição                                                                 | Tecnologia Utilizada                     |
|------------------------------|--------------------------------------------------------------------------|------------------------------------------|
| **Autenticação de Usuários**  | Cadastro e login com senhas hasheadas (Armazenamento seguro no banco).    | `argon2` + `Flask session`               |
| **Gestão de Saldo**           | Consulta, depósito e saque (com atualização em tempo real no MySQL).      | `mysql-connector-python` + `Flask`       |
| **Cotações de Moedas**        | Conversão de valores com base em cotações atualizadas (Dólar, Euro, BTC). | `requests` (API externa)                 |
| **Transações Seguras**        | Operações validadas e registradas no banco de dados.                      | MySQL + Rotas protegidas (`Flask`)       |
| **API RESTful**               | Endpoints para integração com frontend ou aplicativos móveis.             | `Flask` + `Flask-CORS`                   |
| **Variáveis de Ambiente**     | Configuração segura de credenciais (Banco de dados e chaves API).         | `python-dotenv`                          |

## 🛠 Tecnologias e Bibliotecas Destacadas

| Biblioteca/Pacote         | Finalidade                                      | Destaque no Projeto                                                                 |
|---------------------------|------------------------------------------------|------------------------------------------------------------------------------------|
| **Flask**                 | Framework web para construir a API              | Rotas, sessões de usuário (`session`), respostas JSON (`jsonify`) e templates (`render_template`) |
| **Flask-CORS**            | Permitir requisições entre domínios diferentes  | Integração com frontends (React, Angular, etc.)                                    |
| **mysql-connector-python**| Conexão com o banco de dados MySQL             | Armazenamento de usuários, saldos e transações                                     |
| **argon2-cffi** (via `argon2`)| Hash seguro de senhas                     | **Proteção** contra vazamentos        |
| **python-dotenv**         | Gerenciamento de variáveis de ambiente         | Armazena credenciais do banco de dados fora do código (`.env`)                     |
| **requests** (implícito em `moedas.py`)| Requisições HTTP para APIs externas | Obter cotações de dólar, euro e Bitcoin (BTC)                                      |


# 💻 Arquitetura

<img src="https://github.com/PedroHSS01/BankUP/blob/main/static/img/arq.png">

---

## Estrutura de pastas atualizada ✅

- `app.py` — entrypoint do Flask (mantido na raiz)
- `bankup/` — pacote com módulos Python (conexao_db, senhas, moedas, requisicoes, etc.)
- `templates/` — arquivos HTML usados pelo Flask
- `static/` — CSS, JS e imagens
- `tamplates/` foi renomeada para `tamplates_deprecated/` (mantida apenas para compatibilidade histórica)

### Como executar

1. Copie `.env.example` para `.env` e preencha as variáveis.
2. Instale dependências: `pip install -r requirements.txt`
3. Rode: `python app.py` ou `flask run`
4. Acesse: `http://127.0.0.1:5000/`

