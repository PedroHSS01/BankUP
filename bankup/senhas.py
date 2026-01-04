from argon2 import PasswordHasher
from .conexao_db import conectar, fechar_conexao
import mysql.connector

# Instância do PasswordHasher
ph = PasswordHasher()

# Inserir um novo usuário
def inserir_usuario(cpf, nome, senha):
    senha_hash = ph.hash(senha)  # Gera o hash da senha
    conexao, cursor = conectar()
    if conexao and cursor:
        try:
            query = """
                INSERT INTO usuarios (cpf, nome, senha_hash)
                VALUES (%s, %s, %s)
            """
            valores = (cpf, nome, senha_hash)
            cursor.execute(query, valores)
            conexao.commit()
            print("Usuário inserido com sucesso!")
        except mysql.connector.Error as err:
            print(f"Erro ao inserir usuário: {err}")
            raise
        finally:
            fechar_conexao(conexao, cursor)

# Verificar a senha do usuário
def verificar_senha(cpf, senha_fornecida):
    conexao, cursor = conectar()
    if conexao and cursor:
        try:
            query = "SELECT senha_hash FROM usuarios WHERE cpf = %s"
            cursor.execute(query, (cpf,))
            resultado = cursor.fetchone()
            if resultado:
                senha_hash = resultado[0]
                try:
                    # Verifica se a senha fornecida corresponde ao hash armazenado
                    return ph.verify(senha_hash, senha_fornecida)
                except:
                    # Caso a senha esteja incorreta ou o hash seja inválido
                    return False
            else:
                return False
        except mysql.connector.Error as err:
            print(f"Erro ao verificar senha: {err}")
            return False
        finally:
            fechar_conexao(conexao, cursor)

# Atualizar o saldo de um usuário
def atualizar_saldo(cpf, novo_saldo):
    conexao, cursor = conectar()
    if conexao and cursor:
        try:
            query = "UPDATE usuarios SET saldo = %s WHERE cpf = %s"
            valores = (novo_saldo, cpf)
            cursor.execute(query, valores)
            conexao.commit()
            print("Saldo atualizado com sucesso!")
        except mysql.connector.Error as err:
            print(f"Erro ao atualizar saldo: {err}")
        finally:
            fechar_conexao(conexao, cursor)
