import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv


load_dotenv()

def conectar():
    try:
        conexao = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        cursor = conexao.cursor()
        return conexao, cursor
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None, None

def fechar_conexao(conexao, cursor):
    if cursor:
        cursor.close()
    if conexao:
        conexao.close()