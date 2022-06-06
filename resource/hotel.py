from flask_restful import Resource, Api, reqparse

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
    def get(self, hotel_id):
        for hotel in hoteis:
          if hotel['hotel_id'] == hotel_id:
              return hotel 
        return 'Message:' 'Hotel not found.', 404        
    

    def post(self, hotel_id):
        argumentos= reqparse.RequestParser() 
        argumentos.add_argument('nome')
        argumentos.add_argument('estrelas')
        argumentos.add_argument('diaria')
        argumentos.add_argument('cidade')

        dados= argumentos.parse_args()
        novo_hotel= {
            'hotel_id' : hotel_id,
            'nome': dados['nome'],
            'estrelas': dados['estrelas'],
            'diaria': dados['diaria'],
            'cidade': dados['cidade']
        }

        hoteis.append(novo_hotel)
        return novo_hotel, 200   
        
    def put(self, hotel_id):
        pass    
    def delete(self, hotel_id):
        pass