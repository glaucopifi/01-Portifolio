"""
Módulo de sistema bancário simples.

Este módulo contém classes e funções para criar e gerenciar clientes e suas contas bancárias.
Suporta operações de depósito, saque, exibição de extrato e criação de novas contas para clientes.
"""

import textwrap
from abc import ABC, abstractmethod
from datetime import datetime


class Cliente:
    """
    Classe Cliente para armazenar informações sobre os clientes.
    """

    def __init__(self, endereco):
        """
        Inicializa um cliente com endereço e define contas como None.

        :param endereco: Endereço do cliente
        """
        self.endereco = endereco
        self.conta_corrente = None
        self.conta_poupanca = None

    def realizar_transacao(self, conta, transacao):
        """
        Realiza uma transação em uma conta específica.

        :param conta: A conta na qual a transação será realizada
        :param transacao: A transação a ser realizada
        """
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        """
        Adiciona uma conta ao cliente, garantindo que ele só tenha uma conta corrente e uma
        conta poupança.

        :param conta: A conta a ser adicionada
        :return: Booleano indicando se a conta foi adicionada com sucesso
        """
        if isinstance(conta, ContaCorrente):
            if self.conta_corrente is not None:
                print("\n@@@ Cliente já possui uma Conta Corrente! @@@")
                return False
            self.conta_corrente = conta
        elif isinstance(conta, ContaPoupanca):
            if self.conta_poupanca is not None:
                print("\n@@@ Cliente já possui uma Conta Poupança! @@@")
                return False
            self.conta_poupanca = conta
        return True


class PessoaFisica(Cliente):
    """
    Classe PessoaFisica herda de Cliente e adiciona informações específicas de pessoas físicas.
    """

    def __init__(self, nome, data_nascimento, cpf, endereco):
        """
        Inicializa uma pessoa física com nome, data de nascimento, CPF e endereço.

        :param nome: Nome do cliente
        :param data_nascimento: Data de nascimento do cliente
        :param cpf: CPF do cliente
        :param endereco: Endereço do cliente
        """
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta(ABC):
    """
    Classe abstrata Conta define a estrutura básica de uma conta bancária.
    """

    def __init__(self, numero, cliente):
        """
        Inicializa uma conta bancária com número, cliente, saldo inicial e limites.

        :param numero: Número da conta
        :param cliente: Cliente associado à conta
        """
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
        self._limite = 500
        self._limite_saques = 3
        self._valor_saques = 0

    @classmethod
    def nova_conta(cls, cliente, numero):
        """
        Cria uma nova conta para um cliente específico.

        :param cliente: Cliente que será o titular da conta
        :param numero: Número da conta
        :return: Instância da classe Conta
        """
        return cls(numero, cliente)

    @property
    def saldo(self):
        """
        Retorna o saldo da conta.

        :return: Saldo da conta
        """
        return self._saldo

    @property
    def numero(self):
        """
        Retorna o número da conta.

        :return: Número da conta
        """
        return self._numero

    @property
    def agencia(self):
        """
        Retorna a agência da conta.

        :return: Agência da conta
        """
        return self._agencia

    @property
    def cliente(self):
        """
        Retorna o cliente da conta.

        :return: Cliente da conta
        """
        return self._cliente

    @property
    def historico(self):
        """
        Retorna o histórico da conta.

        :return: Histórico da conta
        """
        return self._historico

    def sacar(self, valor):
        """
        Realiza um saque na conta, verificando limites e saldo.

        :param valor: Valor a ser sacado
        :return: Booleano indicando se o saque foi realizado com sucesso
        """
        numero_saques = len(
            [
                transacao
                for transacao in self.historico.transacoes
                if transacao["tipo"] == Saque.__name__
            ]
        )

        excedeu_limite_valor = (self._valor_saques + valor) > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite_valor:
            print(
                "\n@@@ Operação falhou! O valor total dos saques excede o limite de R$ 500. @@@"
            )
        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
        elif valor > self._saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        elif valor > 0:
            self._saldo -= valor
            self._valor_saques += valor
            print("\n=== Saque realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

        return False

    def depositar(self, valor):
        """
        Realiza um depósito na conta.

        :param valor: Valor a ser depositado
        :return: Booleano indicando se o depósito foi realizado com sucesso
        """
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        return True


class ContaCorrente(Conta):
    """
    Classe ContaCorrente herda de Conta e define uma conta corrente.
    """

    def __str__(self):
        """
        Retorna uma representação em string da conta corrente.

        :return: String representando a conta corrente
        """
        return f"""\
Agência:\t{self.agencia}
C/C:\t\t{self.numero}
Titular:\t{self.cliente.nome}
"""

    def tipo_conta(self):
        """
        Retorna o tipo de conta.

        :return: Tipo de conta
        """
        return "Conta Corrente"


class ContaPoupanca(Conta):
    """
    Classe ContaPoupanca herda de Conta e define uma conta poupança.
    """

    def __str__(self):
        """
        Retorna uma representação em string da conta poupança.

        :return: String representando a conta poupança
        """
        return f"""\
Agência:\t{self.agencia}
C/P:\t\t{self.numero}
Titular:\t{self.cliente.nome}
"""

    def tipo_conta(self):
        """
        Retorna o tipo de conta.

        :return: Tipo de conta
        """
        return "Conta Poupança"


class Historico:
    """
    Classe Historico para armazenar o histórico de transações da conta.
    """

    def __init__(self):
        """
        Inicializa o histórico de transações.
        """
        self._transacoes = []

    @property
    def transacoes(self):
        """
        Retorna as transações realizadas na conta.

        :return: Lista de transações
        """
        return self._transacoes

    def adicionar_transacao(self, transacao):
        """
        Adiciona uma transação ao histórico da conta.

        :param transacao: Transação a ser adicionada
        """
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )


class Transacao(ABC):
    """
    Classe abstrata Transacao define a estrutura básica de uma transação.
    """

    @property
    @abstractmethod
    def valor(self):
        """
        Retorna o valor da transação.

        :return: Valor da transação
        """

    @abstractmethod
    def registrar(self, conta):
        """
        Registra a transação na conta.

        :param conta: Conta na qual a transação será registrada
        """
class Saque(Transacao):
    
    """
    Classe Saque herda de Transacao e define uma operação de saque.
    """

    def __init__(self, valor):
        """
        Inicializa um saque com um valor específico.

        :param valor: Valor do saque
        """
        self._valor = valor

    @property
    def valor(self):
        """
        Retorna o valor do saque.

        :return: Valor do saque
        """
        return self._valor

    def registrar(self, conta):
        """
        Registra um saque na conta.

        :param conta: Conta na qual o saque será registrado
        """
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
            print(
                f"\n=== Saque de R$ {self.valor:.2f} realizado na {conta.tipo_conta()} com sucesso! ==="
            )
        else:
            print(
                f"\n@@@ Saque de R$ {self.valor:.2f} falhou na {conta.tipo_conta()}. @@@"
            )


class Deposito(Transacao):
    """
    Classe Deposito herda de Transacao e define uma operação de depósito.
    """

    def __init__(self, valor):
        """
        Inicializa um depósito com um valor específico.

        :param valor: Valor do depósito
        """
        self._valor = valor

    @property
    def valor(self):
        """
        Retorna o valor do depósito.

        :return: Valor do depósito
        """
        return self._valor

    def registrar(self, conta):
        """
        Registra um depósito na conta.

        :param conta: Conta na qual o depósito será registrado
        """
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
            print(
                f"\n=== Depósito de R$ {self.valor:.2f} realizado na {conta.tipo_conta()} com sucesso! ==="
            )
        else:
            print(
                f"\n@@@ Depósito de R$ {self.valor:.2f} falhou na {conta.tipo_conta()}. @@@"
            )


def exibir_menu_principal():
    """
    Exibe o menu principal e retorna a opção escolhida.

    :return: Opção escolhida pelo usuário
    """
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def exibir_menu_tipo_conta():
    """
    Exibe o menu de tipo de conta e retorna a opção escolhida.

    :return: Opção escolhida pelo usuário
    """
    menu = """\n
    ============ TIPO DE CONTA ============
    [cc]\tConta Corrente
    [cp]\tConta Poupança
    => """
    return input(textwrap.dedent(menu))


def filtrar_cliente(cpf, clientes):
    """
    Filtra um cliente pelo CPF e retorna o cliente encontrado ou None.

    :param cpf: CPF do cliente
    :param clientes: Lista de clientes
    :return: Cliente encontrado ou None
    """
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente, tipo_conta):
    """
    Recupera a conta de um cliente baseado no tipo de conta.

    :param cliente: Cliente cujo conta será recuperada
    :param tipo_conta: Tipo de conta (ContaCorrente ou ContaPoupanca)
    :return: Conta do cliente ou None
    """
    if tipo_conta == ContaCorrente:
        return cliente.conta_corrente
    elif tipo_conta == ContaPoupanca:
        return cliente.conta_poupanca
    return None


def depositar(clientes):
    """
    Realiza um depósito em uma conta.

    :param clientes: Lista de clientes
    """
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    tipo_conta = exibir_menu_tipo_conta()
    tipo_conta_class = ContaCorrente if tipo_conta == "cc" else ContaPoupanca

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente, tipo_conta_class)
    if not conta:
        print("\n@@@ Cliente não possui a conta solicitada! @@@")
        return

    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    """
    Realiza um saque de uma conta.

    :param clientes: Lista de clientes
    """
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    tipo_conta = exibir_menu_tipo_conta()
    tipo_conta_class = ContaCorrente if tipo_conta == "cc" else ContaPoupanca

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente, tipo_conta_class)
    if not conta:
        print("\n@@@ Cliente não possui a conta solicitada! @@@")
        return

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    """
    Exibe o extrato de uma conta.

    :param clientes: Lista de clientes
    """
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    tipo_conta = exibir_menu_tipo_conta()
    tipo_conta_class = ContaCorrente if tipo_conta == "cc" else ContaPoupanca

    conta = recuperar_conta_cliente(cliente, tipo_conta_class)
    if not conta:
        print("\n@@@ Cliente não possui a conta solicitada! @@@")
        return

    conta_tipo = (
        "Conta Corrente" if isinstance(conta, ContaCorrente) else "Conta Poupança"
    )

    print(f"\n================ EXTRATO - {conta_tipo} ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")


def criar_cliente(clientes):
    """
    Cria um novo cliente.

    :param clientes: Lista de clientes
    """
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input(
        "Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): "
    )

    cliente = PessoaFisica(
        nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco
    )

    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")


def criar_conta(numero_conta, clientes, contas):
    """
    Cria uma nova conta para um cliente.

    :param numero_conta: Número da nova conta
    :param clientes: Lista de clientes
    :param contas: Lista de contas
    """
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    tipo_conta = exibir_menu_tipo_conta()
    if tipo_conta == "cc":
        conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    elif tipo_conta == "cp":
        conta = ContaPoupanca.nova_conta(cliente=cliente, numero=numero_conta)
    else:
        print("\n@@@ Tipo de conta inválido! @@@")
        return

    sucesso = cliente.adicionar_conta(conta)
    if sucesso:
        contas.append(conta)
        tipo_conta_nome = "Conta Corrente" if tipo_conta == "cc" else "Conta Poupança"
        print(f"\n=== {tipo_conta_nome} criada com sucesso! ===")


def listar_contas(clientes):
    """
    Lista as contas de um cliente.

    :param clientes: Lista de clientes
    """
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    print("\n================ CONTAS ================")
    if cliente.conta_corrente:
        print("\nConta Corrente:")
        print(cliente.conta_corrente)
    if cliente.conta_poupanca:
        print("\nConta Poupança:")
        print(cliente.conta_poupanca)
    if not cliente.conta_corrente and not cliente.conta_poupanca:
        print("Cliente não possui contas.")
    print("========================================")


def main():
    """
    Função principal do programa.
    """
    clientes = []
    contas = []

    while True:
        opcao = exibir_menu_principal()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(clientes)

        elif opcao == "q":
            break

        else:
            print(
                "\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@"
            )


if __name__ == "__main__":
    main()
