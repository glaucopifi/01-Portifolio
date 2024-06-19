# Desafio: Sistema Bancário em Python

## Descrição do Desafio

O desafio consiste em modelar um sistema bancário utilizando Programação Orientada a Objetos (POO) em Python. O sistema deve incluir funcionalidades básicas como criação de contas, depósitos, saques e transferências. Além disso, deve implementar um histórico de transações para cada conta.

## Diagrama UML

![Esquema do Desafio](Esquema_desafio.png)

### Explicação do Diagrama

#### Classes Principais

1. **Conta**
    - **Atributos**:
        - `saldo: float` - Saldo da conta.
        - `numero: int` - Número da conta.
        - `agencia: str` - Agência da conta.
        - `cliente: Cliente` - Cliente associado à conta.
        - `historico: Historico` - Histórico de transações da conta.
    - **Métodos**:
        - `saldo() -> float` - Retorna o saldo da conta.
        - `nova_conta(cliente: Cliente, numero: int) -> Conta` - Cria uma nova conta para o cliente.
        - `sacar(valor: float) -> bool` - Realiza um saque na conta.
        - `depositar(valor: float) -> bool` - Realiza um depósito na conta.

2. **ContaCorrente** (herda de Conta)
    - **Atributos**:
        - `limite: float` - Limite de crédito da conta corrente.
        - `limite_saques: int` - Limite de saques permitidos.

3. **Historico**
    - **Atributos**:
        - `transacoes: List[Transacao]` - Lista de transações realizadas na conta.
    - **Métodos**:
        - `adicionar_transacao(transacao: Transacao)` - Adiciona uma transação ao histórico.

#### Interfaces

1. **Transacao**
    - **Métodos**:
        - `registrar(conta: Conta)` - Registra a transação em uma conta.

#### Classes Concretas de Transacao

1. **Deposito** (implementa Transacao)
    - **Atributos**:
        - `valor: float` - Valor do depósito.

2. **Saque** (implementa Transacao)
    - **Atributos**:
        - `valor: float` - Valor do saque.

#### Classes Relacionadas a Clientes

1. **Cliente**
    - **Atributos**:
        - `endereco: str` - Endereço do cliente.
        - `contas: list` - Lista de contas do cliente.
    - **Métodos**:
        - `realizar_transacao(conta: Conta, transacao: Transacao)` - Realiza uma transação em uma conta.
        - `adicionar_conta(conta: Conta)` - Adiciona uma nova conta ao cliente.

2. **PessoaFisica** (herda de Cliente)
    - **Atributos**:
        - `cpf: str` - CPF do cliente.
        - `nome: str` - Nome do cliente.
        - `data_nascimento: date` - Data de nascimento do cliente.

## Funcionalidades do Sistema

- **Criar contas**:
  - Conta Corrente
  - Conta Poupança

- **Operações bancárias**:
  - Depósitos
  - Saques
  - Transferências entre contas

- **Gerenciamento de contas**:
  - Adicionar e remover contas do banco
  - Buscar contas por número

## Como Executar o Projeto

1. Clone o repositório para sua máquina local.
2. Navegue até o diretório do projeto.
3. Execute o arquivo `main.py` para iniciar o sistema bancário.



```bash
git clone <URL-do-repositorio>
cd sistema_bancario
python main.py
```
## Contribuição
Sinta-se à vontade para contribuir com este projeto enviando pull requests. Todas as contribuições são bem-vindas!

## Licença
Este projeto está licenciado sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.
