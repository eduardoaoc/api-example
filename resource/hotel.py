from flask_restful import Resource, Api, reqparse
from models.hotel import *

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
        #SELECT * FROM hoteis
        return {'Hoteis': [hotel.json() for hotel in HotelModel.query.all()]}

class Hotel(Resource):
    #recebe os argumentos da requisição feita.
    argumentos= reqparse.RequestParser()     
    #seleciona o argumento que será adicionado, 
    #só aceita os argumentos que foram mencionados abaixo
    #mesmo que tente adionar qualquer outro argumento que não esteja citado abaixo, ele não rece
    #recebe apenas os argumentos citados 
    argumentos.add_argument('nome', type=str, required=True, help="The field 'nome' cannot be left blank.")
    argumentos.add_argument('estrelas', type=float, required= True, help="The field 'estrelas' cannot be left blank.")
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    def get(self, hotel_id):
        hotel= HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'Message': 'Hotel not found.'}, 404        
    

    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message: " "Hotel id '{}'' already exists.".format(hotel_id)}, 404  #not found

        #chaves e valores dos argumentos passados, colhe os dados
        dados= Hotel.argumentos.parse_args()
        #desempacota todos os dados **dados, ele define a chave e o valor pra cada dado que tiver, instancia novo hotel
        hotel= HotelModel(hotel_id, **dados)
        try:
            #salva o hotel no banco de dados e substitui
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save.'}, 500 #internal server erro    
        return hotel.json()       

    def put(self, hotel_id):
        #chaves e valores dos argumentos passados, colhe os dados
        dados= Hotel.argumentos.parse_args()    
        #novo_hotel= {'hotel_id' : hotel_id, **dados}
        hotel_encontrado= HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            #função criada para atualizar o hotel caso ele exista, 200 sucesso
            #desempacota todos os dados **dados, ele define a chave e o valor pra cada dado que tiver  
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200 
        hotel= HotelModel(hotel_id, **dados)    
        #se não existir, o hotel será criado/adicionado com o comando abaixo, 201 código de criado
        try:
            #salva o hotel no banco de dados e substitui
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save.'}, 500 #internal server erro      
        return hotel.json(), 201   

    def delete(self, hotel_id):
        hotel= HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'Message': 'An error ocurred trying to delete.'}, 500      
            return {'Message': 'Hotel deleted.'}
        return {'Message': 'Hotel not found.'}, 404
