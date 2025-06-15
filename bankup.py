import textwrap
import logging
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime


#Configuração o logger para registro em um arquivo .txt
logging.basicConfig(
    filename='C:\\Users\\PICHAU\\Desktop\\BankUP\\log.txt',
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S"',
)

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, trasacao):
        trasacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = '001'
        self._cliente = cliente
        self._historico = Historico()


    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

# Def's para trasações de saques
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print('\nXXX Operação falhou! Você não possui saldo suficiênte. XXX')

        elif valor > 0:
            self._saldo -= valor
            print('\n¬¬¬ Saque realizado com sucesso! ¬¬¬')
            return True

        else:
            print('\nXXX Operação falhou! O valor informado é inválido. XXX')

        return False

#Def's para trasações de deposito
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print('\n¬¬¬ Depósito realizado comsucesso! ¬¬¬')
        else:
            print('\nXXX Operação falhou! O valor informado é inválido XXX')
            return False

        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques =numero_saques >= self._limite_saques

        if excedeu_limite:
            print('\nXXX Operação falhou! Valor do saque excede o limite. XXX')

        elif excedeu_saques:
            print('\nXXX Operação falhou! Número maxido de saques excedido. XXX')

        else:
            return super().sacar(valor)
        return False

    def __str__(self):
        return f"""\
             Agência:\t{self.agencia}
             C/C:\t\t{self.numero}
             Titular:\t{self.cliente.nome}
          """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
            return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),

                }
            )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

#Boas vindas ao usúario do banco!
print('Bem-vindo(a) ao bankup $')

#"Tela" de Menu do banco
def menu():
    menu = """\n
    ¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬ MENU ¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬
     [1]\tDepositar
     [2]\tSacar
     [3]\tExtrato
     [4]\tNovo Usuário
     [5]\tNova Conta
     [6]\tListar Contas
     [7]\tSair
     => """
    return input(textwrap.dedent(menu))

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print('\nXXX Atenção, Cliente Não Possui conta. XXX')
        return
    return cliente.contas[0]

def depositar(clientes):
    cpf = input('Informe o CPF sem vírgula por favor: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('\nXXX Atenção cliente não encontrado XXX')
        return

    valor = float(input('Por favor informe o valor do depósito: '))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Por favor, informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nXXX Atenção, cliente não encontrado! @@@")
        return

    valor = float(input("Por favor, informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(cliente):
    cpf = input('Por favor, Informe o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, cliente)

    if not cliente:
        print('\nXXX Atenção, Cliente Não Encontrado XXX')
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print('\n¬¬¬¬¬¬¬¬¬¬¬¬¬ EXTRATO ¬¬¬¬¬¬¬¬¬¬¬¬¬')
    transacoes = conta.historico.transacoes

    extrato = ''
    if not transacoes:
        extrato = 'Não foram realizadas movimentações hoje.'
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f} - {transacao['data']}"

    print(extrato)
    print(f'\nSaldo:\n\tR$ {conta.saldo:.2f}')
    print('¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬')

def criar_cliente(clientes):
    cpf = input("Informe o CPF sem ponto/vírgula:  ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ CPF já cadastrado.! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")

def criar_conta(numero_conta, clientes, contas):
    cpf = input('Informe o CPF sem ponto/vírgula: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('\nXXX Atenção, cliente não encontrado, fim da operação. XXX')
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print('\n \ 0 / Parabéns, Conta criada com sucesso \ 0 /')


def listar_contas(contas):
    for conta in contas:
        print('=' * 100)
        print(textwrap.dedent(str(conta)))


def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == '1':
            depositar(clientes)

        elif opcao == '2':
            sacar(clientes)

        elif opcao == '3':
            exibir_extrato(clientes)

        elif opcao == '4':
            criar_cliente(clientes)

        elif opcao == '5':
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == '6':
            listar_contas(contas)

        elif opcao == '7':
            break

        else:
            print('\nXXX Operação inválida, por favor selecione novamente a operação desejada. XXX')


main()
