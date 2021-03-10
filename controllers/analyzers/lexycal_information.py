class LexycalInformation:
    def __init__(self):
        self.token = ""
        self.numerico = ""
        self.estado = 0
        self.token_geral = []
        self.tabela_token = {}
        self.linha = 0
        self.coluna = 0
        self.id_tabela = 0
        self.acumula = ""
