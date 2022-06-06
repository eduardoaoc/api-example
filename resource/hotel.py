from flask_restful import Resource, Api

hoteis= ({'hotel_id:''alpha', 'nome:''alpha hotel' 'estrelas:', 4.3,'diaria:' , 420.52},{'hotel_id:''beta', 'nome:''beta hotel' 'estrelas:', 4.0,'diaria:' , 315.52}, 'hotel_id:''gamma', 'nome:''gamma hotel' 'estrelas:', 4.8,'diaria:' , 477.55)


#primeiro recurso da api
class Hoteis(Resource): 
    def get(self):
        return {'Hoteis': hoteis}

class Hotel(Resource):
    def get(self, hotel_id):
        for hotel in hoteis:
          if hotel['hotel_id'] == hotel_id:
              return hotel 
        return {'message':'Hotel not found.'}, 404
        
    def post(self, hotel_id):
        pass
    def put(self, hotel_id):
        pass    
    def delete(self, hotel_id):
        pass