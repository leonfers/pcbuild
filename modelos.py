class Product:

    def __init__(self):
        self.nome = ''
        self.descricao = ''
        self.url = ''
        self.avista = ''
        self.parcelado = ''
        self.loja = ''

    def build(self, json):
        self.nome = json['name']
        self.descricao = json['longDescription']
        self.url = json['url']
        self.avista = json['finalPrice']
        self.parcelado = json['finalInstallmentPrice']
        self.loja = json['storeName']

    def __str__(self):
        return f'{self.nome} {self.descricao} {self.url} {self.avista} {self.parcelado} {self.loja}'
