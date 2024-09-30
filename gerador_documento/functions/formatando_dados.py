from num2words import num2words#pacote para escrever o numero por extenso

'''
Criando um local para formatação, isso vai depender do contexto, caso haja 
alguma necessidade de formatar algo em especial
'''
class FormatAll:#classe onde serão feitas todas as formatações necessárias(no 
    #caso são especiais devido a contexto que esse projeto esta sendo utilizado)
    def __init__(self,request_itens:list) -> None:
        self.dados_dict = {}
        for chave,valor in request_itens:
            valor = valor.strip()
            match chave:
                case 'csrfmiddlewaretoken':
                    continue
                
                case 'HHH':
                    #chaves com letras repetidas para evitar que na 
                    #digitação seja possível escrever elas, é porque o python 
                    #estava separando as palavras  por exemplo NUMERO_FATURA -> 
                    # 'NUMERO' e '_FATURA' 
                    dinheiro_escrito = self.escrever_money(valor)
                    valor = self.format_dinheiro(valor)
                    #elas vão como chaves maiúsculas
                    lista = [['LLL',dinheiro_escrito],[chave.upper(),valor]]
                    self.dados_dict.update(lista)
                    continue
                
                case 'AAA':
                    valor = self.format_date(valor)
                    self.dados_dict.update([(chave.upper(),valor)])
                    continue
                
                case 'XXX':
                    valor = f'Medição n.º {valor}'
                    self.dados_dict.update([(chave.upper(),valor)])
            self.dados_dict.update([(chave.upper(),valor)])


    def format_date(self,date:str):
        if date.count('/') < 2 :
            return date
        meses = {'janeiro':'01', 'fevereiro':'02', 'março':'03', 'abril':'04', 
            'maio':'05', 'junho': '06', 'julho':'07', 'agosto': '08', 
            'setembro':'09', 'outubro':'10', 'novembro':'11', 'dezembro':'12'}
        
        date = date.replace('/', ' de ')
        for mes,numero in meses.items():
            dia_,mes_,ano_ = date.split(' de ')
            if numero in mes_:
                date = ' de '.join([dia_,mes,ano_])
                return date

    def escrever_money(self,dinheiro: str):#Escrevendo o valor por extenso
        dinheiro = dinheiro.replace('.','')#tirando os pontos
        if 'R$' in dinheiro:
            dinheiro = dinheiro.replace('R$','')#e o simbolo
        
        if ',' in dinheiro:
        
            reais,centavos = dinheiro.split(',')
            if 0 != int(centavos):
                reais = num2words(int(reais),lang='pt-br') +' reais e '
                centavos = num2words(int(centavos),lang='pt-br')+ ' centavos'
                dinheiro_escrito: str = reais + centavos
                return dinheiro_escrito
            else:
                dinheiro_escrito = num2words(int(reais),lang='pt-br') + ' reais'
                return dinheiro_escrito

        dinheiro_escrito = num2words(int(dinheiro),lang='pt-br') + ' reais'
        return dinheiro_escrito

    def format_dinheiro(self,dinheiro:str):#Apenas garantindo que tenha R$ e ','  no dinheiro
        dinheiro = dinheiro.strip()
        if 'R$' in dinheiro and ',' in dinheiro:
            return dinheiro
        if ',' not in dinheiro:
            dinheiro = dinheiro.replace('R$', '')
            dinheiro = f'R${dinheiro},00'
            return dinheiro
        
        return f'R$ {dinheiro}'

