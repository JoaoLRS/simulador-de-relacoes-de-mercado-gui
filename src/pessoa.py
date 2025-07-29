class Pessoa:
    def __init__(self, nome, patrimonio, salario):
        self.nome = nome
        self.patrimonio = float(patrimonio)
        self.salario = float(salario)
        self.conforto = 0.0
        self.rendimento_mensal = self.salario