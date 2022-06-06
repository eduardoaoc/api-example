from flask_restful import Resource, Api, reqparse
from models.hotel import HotelModel

hoteis= [ 
        {
            'hotel_id':'alpha', 
            'nome':'alpha hotel' ,
            'estrelas': 4.3,
            'diaria': 420.52,
            'cidade':'Santa Catarina'
        },
        {
            'hotel_id':'beta', 
            'nome':'beta hotel',
            'estrelas': 4.0,
            'diaria': 315.52,
            'cidade':'Belo Horizonte'
        },
        {
            'hotel_id':'gama', 
            'nome':'gama hotel',
            'estrelas': 4.7,
            'diaria': 485.77,
            'cidade':'Rio de Janeiro'
        }
]
 
#primeiro recurso da api
class Hoteis(Resource): 
    def get(self):
        return {'Hoteis': hoteis}

class Hotel(Resource):
    #recebe os argumentos da requisição feita.
    argumentos= reqparse.RequestParser()     
    #seleciona o argumento que será adicionado, 
    #só aceita os argumentos que foram mencionados abaixo
    #mesmo que tente adionar qualquer outro argumento que não esteja citado abaixo, ele não rece
    #recebe apenas os argumentos citados 
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')
    def find_hotel(hotel_id):
        #laço de repetição que pesquisa se existe o hotel mencionado, se existir retorna o hotel 
        for hotel in hoteis:
          if hotel['hotel_id'] == hotel_id:
              return hotel 
        return None

    def get(self, hotel_id):
        hotel= Hotel.find_hotel(hotel_id)
        if hotel:
            return hotel
        return 'Message:' 'Hotel not found.', 404        
    

    def post(self, hotel_id):
        #chaves e valores dos argumentos passados, colhe os dados
        dados= Hotel.argumentos.parse_args()
        #desempacota todos os dados **dados, ele define a chave e o valor pra cada dado que tiver
        hotel_objeto= HotelModel(hotel_id, **dados)
        #converte em um dicionário e transforma para JASON
        novo_hotel= hotel_objeto.json()
        #novo_hotel= {'hotel_id' : hotel_id, **dados}
        #comando para adiocionar um elemntos na lista 
        hoteis.append(novo_hotel)
        #retorna um novo hotel e apresenta um código de sucesso 
        return novo_hotel, 200   
        
    def put(self, hotel_id):
        #chaves e valores dos argumentos passados, colhe os dados
        dados= Hotel.argumentos.parse_args()
        #desempacota todos os dados **dados, ele define a chave e o valor pra cada dado que tiver
        hotel_objeto= HotelModel(hotel_id, **dados)
        #converte em um dicionário e transforma para JASON
        novo_hotel= hotel_objeto.json()
        #novo_hotel= {'hotel_id' : hotel_id, **dados}
        hotel= Hotel.find_hotel(hotel_id)
        if hotel:
            #função criada para atualizar o hotel caso ele exista, 200 sucesso
            hotel.update(novo_hotel)
            return novo_hotel, 200 
        #se não existir, o hotel será criado/adicionado com o comando abaixo, 201 código de criado
        hoteis.append(novo_hotel)  
        return novo_hotel, 201 
    
    def delete(self, hotel_id):
        #para fazer a referencia a lista que ja foi criada
        global hoteis
        #retorna hotel para cada hotel dentro da lista hoteis, 
        #se o hotel com id em questão não for igual ao hotel passado.
        #para deletar pegaramos todo os hoteis que nao tenhoa o ID em questão
        #e sera criado uma nova lista sem o hotel que foi passado no delete
        hoteis= [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]
        return 'Message:' 'Hotel deleted.'

