from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from datetime import datetime
from bankup.conexao_db import conectar, fechar_conexao
from bankup.senhas import inserir_usuario, verificar_senha, atualizar_saldo
from mysql.connector import Error as MySQLError
from flask_cors import CORS
from bankup.moedas import obter_cotacoes

app = Flask(__name__)
CORS(app)
app.secret_key = 'P2626h'


@app.route("/cotacoes")
def get_cotacoes():
    cotacoes = obter_cotacoes()
    return jsonify(cotacoes)

#Def's p/ deposito
def depositar(saldo, valor):
    if valor > 0:
        saldo += valor
        print(f'\n¬¬¬ Depósito de R$ {valor:.2f} realizado com sucesso! ¬¬¬')
        return saldo
    else:
        print('\nXXX Operação falhou! O valor informado é inválido. XXX')
        return saldo

# Def's p/ saques
def sacar(saldo, valor):
    excedeu_saldo = valor > saldo
    if excedeu_saldo:
        print('\nXXX Operação falhou! Você não possui saldo suficiênte. XXX')
    elif valor > 0:
        saldo -= valor
        print('\n¬¬¬ Saque realizado com sucesso! ¬¬¬')
        return True
    else:
        print('\nXXX Operação falhou! O valor informado é inválido. XXX')
    return False

# Def's p/ ver extrato
def ver_extrato(saldo, extrato):
    print('\n========== EXTRATO ==========')
    if not extrato:
        print('Não foram realizadas movimentações.')
    else:
        for movimento in extrato:
            print(movimento)
    print(f'\nSaldo atual: R$ {saldo:.2f}')
    print('=============================')

# def p/ fazer transferencia
def transferir(saldo_origem, saldo_destino, valor, extrato_origem, extrato_destino):
    excedeu_saldo = valor > saldo_origem

    if excedeu_saldo:
        print('\nXXX Operação falhou! Saldo insuficiente para transferência. XXX')
    elif valor > 0:
        saldo_origem -= valor
        saldo_destino += valor
        extrato_origem.append(f'Transferência enviada: R$ {valor:.2f}')
        extrato_destino.append(f'Transferência recebida: R$ {valor:.2f}')
        print(f'\n¬¬¬ Transferência de R$ {valor:.2f} realizada com sucesso! ¬¬¬')
    else:
        print('\nXXX Operação falhou! O valor informado é inválido. XXX')
    
    return saldo_origem, saldo_destino, extrato_origem, extrato_destino


# def p/ sair
def sair():
    session.clear()
    return redirect(url_for('index'))


# Rota p/ servir o frontend
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

# Endpoint p/ login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    cpf = data.get('cpf')
    senha = data.get('senha')

    conexao, cursor = conectar()
    if not conexao:
        return jsonify({"message": "Erro ao conectar ao banco de dados"}), 500

    try:
        # Busca o usuário e verifica a senha
        cursor.execute("SELECT * FROM usuarios WHERE cpf = %s", (cpf,))
        cliente = cursor.fetchone()
        
        if cliente and verificar_senha(cpf, senha):
            # Retorna o nome do usuário junto com a mensagem de sucesso
            return jsonify({
                "message": "Login bem-sucedido",
                "usuarios": cliente,
                "nome": cliente[2]
            }), 200
        else:
            return jsonify({"message": "CPF ou senha incorretos"}), 404
    except MySQLError as e:
        return jsonify({"message": f"Erro ao realizar login: {e}"}), 500
    finally:
        fechar_conexao(conexao, cursor)


# Endpoint p/ logout
@app.route('/logout', methods=['POST'])
def logout():
    sair()
    return jsonify({"message": "Logout realizado com sucesso"}), 200

# Endpoint p/ cadastrar novo cliente
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    data = request.json
    cpf = data.get('cpf')
    nome = data.get('nome')
    senha = data.get('senha')

    print("Dados recebidos:", data)

    try:
        inserir_usuario(cpf, nome, senha)
        return jsonify({"message": "Cliente cadastrado com sucesso"}), 201
    except MySQLError as e:
        if e.errno == 1062:
            error_message = 'Cliente já cadastrado'
            status_code = 409
        else:
            error_message = 'Erro ao cadastrar cliente'
            status_code = 400

        print(f'{error_message}: {e}')
        return jsonify({'message': error_message}), status_code
    except Exception as e:
        print(f'Erro ao cadastrar cliente: {e}')
        return jsonify({'message': 'Erro interno no servidor'}), 500

# Endpoint p/ depositar
@app.route('/depositar', methods=['POST'])
def depositar():
    data = request.json
    cpf = data.get('cpf')
    valor = data.get('valor')

    conexao, cursor = conectar()
    if not conexao:
        return jsonify({"message": "Erro ao conectar ao banco de dados"}), 500

    try:
        # Busca o cliente
        cursor.execute("SELECT id FROM usuarios WHERE cpf = %s", (cpf,))
        cliente = cursor.fetchone()
        if not cliente:
            fechar_conexao(conexao, cursor)
            return jsonify({"message": "Cliente não encontrado"}), 404

        # Atualiza o saldo
        atualizar_saldo(cpf, valor)
        fechar_conexao(conexao, cursor)
        return jsonify({"message": "Depósito realizado com sucesso"}), 200
    except MySQLError as e:
        fechar_conexao(conexao, cursor)
        return jsonify({"message": f"Erro ao realizar depósito: {e}"}), 500




if __name__ == '__main__':
    app.run(debug=True)