from abc import ABC, abstractmethod
from datetime import datetime

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return list(self._transacoes)

    def adicionar_transacao(self, tipo, valor):
        registro = {
            "tipo": tipo,
            "valor": valor,
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self._transacoes.append(registro)


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta._depositar(self.valor)
        if sucesso:
            conta._historico.adicionar_transacao("Deposito", self.valor)
        return sucesso


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta._sacar(self.valor)
        if sucesso:
            conta._historico.adicionar_transacao("Saque", self.valor)
        return sucesso


class Conta:
    def __init__(self, cliente, numero, agencia="0001"):
        self._cliente = cliente
        self._numero = numero
        self._agencia = agencia
        self._saldo = 0.0
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        conta = cls(cliente, numero)
        cliente.adicionar_conta(conta)
        return conta

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

    def _sacar(self, valor):
        if 0 < valor <= self._saldo:
            self._saldo -= valor
            return True
        return False

    def _depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            return True
        return False


class ContaCorrente(Conta):
    def __init__(self, cliente, numero, agencia="0001", limite=500.0, limite_saques=3):
        super().__init__(cliente, numero, agencia)
        self.limite = limite
        self.limite_saques = limite_saques
        self.saques_realizados = 0

    def _sacar(self, valor):
        disponivel = self.saldo + self.limite
        if valor <= 0 or valor > disponivel:
            return False
        if self.saques_realizados >= self.limite_saques:
            return False

        self.saques_realizados += 1
        self._saldo -= valor
        return True

    def __str__(self):
        return (
            f"Agência: {self.agencia}\n"
            f"Conta:   {self.numero}\n"
            f"Titular: {self.cliente.nome}"
        )


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def realizar_transacao(self, conta, transacao):
        return transacao.registrar(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf