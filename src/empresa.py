class Empresa:
    def __init__(self, categoria, nome, produto, custo, qualidade):
        self.categoria = categoria
        self.nome = nome
        self.produto = produto
        self.custo = float(custo)
        self.qualidade = int(qualidade)
        self.margem = 0.05  # 5% de margem inicial
        self.oferta = 10    # Estoque inicial
        self.reposicao = 10
        self.vendas = 0
        self.lucro_total = 0.0
        self.meses_sem_venda = 0  

    def get_preco(self):
        return self.custo * (1 + self.margem)
    
    def calcular_lucro_vendas(self):
        return self.vendas * (self.get_preco() - self.custo)
    
    def vender_produto(self):
        if self.oferta > 0:
            self.vendas += 1
            self.oferta -= 1
            lucro_venda = self.get_preco() - self.custo
            self.lucro_total += lucro_venda
            self.meses_sem_venda = 0
            return True
        return False
    
    def repor_estoque(self):
        self.oferta += self.reposicao
    
    def ajustar_estrategia(self):
        # Se vendeu tudo, aumenta margem e reposição
        if self.oferta == 0:
            self.margem = min(self.margem + 0.01, 0.5)  # Máximo 50% de margem
            self.reposicao += 1
        # Se sobrou muito estoque, diminui margem e reposição
        elif self.oferta > 15:
            self.margem = max(self.margem - 0.01, 0.01)  # Mínimo 1% de margem
            self.reposicao = max(self.reposicao - 1, 1)   # Mínimo 1 de reposição