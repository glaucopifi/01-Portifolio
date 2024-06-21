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

## Comparação e Melhorias do Código de Sistema Bancário

## Introdução

Este documento descreve as mudanças, melhorias e implementações realizadas no código de um sistema bancário simples. As principais alterações incluem simplificação de classes, ajustes em métodos, aprimoramento da lógica de transações, e adição de novas funcionalidades.

## Mudanças Gerais

### Importações

- Removido `abstractproperty` e `abstractclassmethod` desnecessários.
- Mantido `ABC` e `abstractmethod` para classes abstratas.

### Classe Cliente

- Adicionado atributo `contas` para armazenar múltiplas contas.
- Removido `ContaCorrente` e `ContaPoupanca` como atributos diretos.
- Mantido método `realizar_transacao` para registrar transações em contas específicas.
- Simplificado método `adicionar_conta` para adicionar qualquer tipo de conta à lista de contas do cliente.

### Classe PessoaFisica

- Mantida a inicialização de atributos: `nome`, `data_nascimento`, `cpf`, `endereco`.
- Herdado da classe `Cliente` e aproveitada a estrutura existente.

### Classe Conta

- Removidos atributos `_limite`, `_limite_saques` e `_valor_saques` (movidos para `ContaCorrente`).
- Simplificado método `sacar` para verificar apenas o saldo.
- Mantido método `depositar` com verificação de valor válido.
- Adicionado método `nova_conta` para criar novas instâncias de conta.

### Classe ContaCorrente

- Adicionados atributos `_limite` e `_limite_saques` para controle específico de contas correntes.
- Aprimorado método `sacar` para verificar limite de valor e número de saques.
- Mantido método `__str__` para exibição de informações da conta.

### Classe ContaPoupanca

- Implementado método `__str__` para exibição de informações da conta poupança.
- Mantido método `tipo_conta` para retornar o tipo de conta.

### Classe Historico

- Mantida a estrutura básica com método para adicionar transações.
- Adicionado método `adicionar_transacao` para registrar transações no histórico.

### Classe Transacao

- Simplificado para usar `abstractmethod` apenas para `valor` e `registrar`.
- Definido `valor` como propriedade abstrata e `registrar` como método abstrato.

### Classes Saque e Deposito

- Mantida lógica de inicialização e registro de transações.
- Implementado método `registrar` para registrar as respectivas transações em uma conta.

## Melhorias Específicas

### Funções do Sistema

- Exibido menu principal e de tipo de conta de forma clara.
- Simplificado método `recuperar_conta_cliente` para retornar a primeira conta encontrada, com uma observação de melhoria futura.
- Mantido fluxo para criação de cliente e conta, garantindo a associação correta.
- Implementada verificação para permitir apenas uma conta de cada tipo por cliente.

### Função main

- Mantido loop principal com opções de depósito, saque, extrato, criação de conta e cliente, e listagem de contas.

## Implementações

### Função menu

- Definido um menu para interação do usuário com opções de depósito, saque, extrato, nova conta, listar contas, novo usuário e sair.

### Função filtrar_cliente

- Implementado filtro de cliente pelo CPF para buscar e retornar um cliente específico da lista de clientes.

### Função recuperar_conta_cliente

- Adicionado método para recuperar a conta de um cliente baseado na lista de contas associadas ao cliente.
- Observação: Atualmente, retorna a primeira conta encontrada. Há espaço para melhoria, permitindo o cliente escolher entre múltiplas contas.

### Função depositar

- Implementado fluxo para realizar um depósito, incluindo entrada do CPF do cliente, valor do depósito e registro da transação na conta do cliente.

### Função sacar

- Implementado fluxo para realizar um saque, incluindo entrada do CPF do cliente, valor do saque e registro da transação na conta do cliente.

### Função exibir_extrato

- Definido método para exibir o extrato de uma conta, listando todas as transações realizadas e o saldo atual.

### Função criar_cliente

- Implementado fluxo para criar um novo cliente, incluindo entrada de CPF, nome, data de nascimento e endereço.

### Função criar_conta

- Definido método para criar uma nova conta para um cliente existente, associando a conta ao cliente e adicionando à lista de contas.

### Função criar conta

- Definido método para criar uma nova conta para um cliente existente, associando a conta ao cliente e adicionando à lista de contas.
- Implementada verificação para garantir que um cliente possa ter apenas uma conta corrente e uma conta poupança.

### Função listar_contas

- Implementado fluxo para listar todas as contas existentes, exibindo informações detalhadas de cada conta.

## Conclusão

As mudanças, melhorias e implementações realizadas visam simplificar o código, melhorar a estrutura das classes e métodos, e garantir um fluxo mais eficiente e claro para as operações bancárias. Estas alterações proporcionam um sistema mais robusto e fácil de manter, além de facilitar futuras expansões e melhorias.
