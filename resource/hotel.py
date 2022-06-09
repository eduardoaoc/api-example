from importlib.resources import path
from flask_restful import Resource, Api, reqparse
from models.hotel import *
from flask_jwt_extended import *
import sqlite3


#seta os valores como padrão, caso o usuário envie algum valor ele sera substituido
def normalize_path_params(cidade=None,
estrelas_min=0, 
estrelas_max=5,
diaria_min=0,
diaria_max=1000,
limit=50,
offset=0, **dados):

    if cidade:
        return {
            'estrelas_min': estrelas_min,
            'estrelas_max': estrelas_max,
            'diaria_min': diaria_min,
            'diaria_max': diaria_max,
            'cidade': cidade,
            'limit': limit,
            'offset': offset
        }
    return {
            'estrelas_min': estrelas_min,
            'estrelas_max': estrelas_max,
            'diaria_min': diaria_min,
            'diaria_max': diaria_max,
            'limit': limit,
            'offset': offset
        }

#caminho path / hoteis?cidade=MinasGerais&estrelas_min=4&diaria_max=400
path_params= reqparse.RequestParser() 
path_params.add_argument('cidade', type=str)
path_params.add_argument('estrelas_min', type=float)
path_params.add_argument('estrelas_max', type=float)
path_params.add_argument('diaria_min', type=float)
path_params.add_argument('diaria_max', type=float)
#quantidade de intens a ser exibidos por página. /limit
path_params.add_argument('limit', type=float) 
#quantidade de elementos que deseja ser pulado
path_params.add_argument('offset', type=float)


#primeiro recurso da api
class Hoteis(Resource): 
    def get(self):
        connection= sqlite3.connect('banco.db')
        cursor= connection.cursor()
        
        #recebe todos os parametros desejados do path
        dados= path_params.parse_args()
        #rece o valor da chave para cada chave em dados se o valor da chave não for NONE
        dados_validos= {chave:dados[chave] for chave in dados if dados[chave] is not None}
        #retorna um dicionário com o valor padrão ou valor modificado
        parametros= normalize_path_params(**dados_validos)

        if not parametros.get('cidade'):
            #se a pessoa definir qual é o minimo será necessário retornar tudo que for maior que minimo, o mesmo ocorre ao contrário no maximo
            consulta= "SELECT * FROM hoteis WHERE (estrelas >= ? and estrelas <= ?) \
                and (diaria >= ?  and diaria <= ?) LIMIT ? OFFSET ?"
            #quando colocamos o dicionário e a chave dele pegamos somente os valores do dicionário    
            tupla= tuple([parametros[chave] for chave in parametros])
            resultado= cursor.execute(consulta, tupla)
        else:
            consulta= "SELECT * FROM hoteis WHERE (estrelas >= ? and estrelas <= ?) \
                and (diaria >= ?  and diaria <= ?) and cidade = ? LIMIT ? OFFSET ?"  
            tupla= tuple([parametros[chave] for chave in parametros])
            resultado= cursor.execute(consulta, tupla)
        #lista
        hoteis= []
        #pra cada linha do resultado no banco de dados, será criado um dicinário 
        for linha in resultado:
            hoteis.append({
            'hotel_id': linha[0],
            'nome': linha[1],
            'estrelas': linha[2],
            'diaria': linha[3],
            'cidade': linha[4]
            })
        #SELECT * FROM hoteis
        return {'Hoteis': hoteis} #transforma para json

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
    # pesquisa tudo que tem dentro
    def get(self, hotel_id):
        hotel= HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'Message': 'Hotel not found.'}, 404        
    
    #inserção de dados
    @jwt_required() #faz com que todas as operações que o usuário queira mudar e necessário estar logado
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"Message": "Hotel id '{}'' already exists.".format(hotel_id)}, 404  #not found

        #chaves e valores dos argumentos passados, colhe os dados
        dados= Hotel.argumentos.parse_args()
        #desempacota todos os dados **dados, ele define a chave e o valor pra cada dado que tiver, instancia novo hotel
        hotel= HotelModel(hotel_id, **dados)
        try:
            #salva o hotel no banco de dados e substitui
            hotel.save_hotel()
        except:
            return {'Message': 'An internal error ocurred trying to save.'}, 500 #internal server erro    
        return hotel.json()       
    #atualização de dados
    @jwt_required()
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
            return {'Message': 'An internal error ocurred trying to save.'}, 500 #internal server erro      
        return hotel.json(), 201   

    @jwt_required()
    def delete(self, hotel_id):
        hotel= HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'Message': 'An error ocurred trying to delete.'}, 500      
            return {'Message': 'Hotel deleted.'}
        return {'Message': 'Hotel not found.'}, 404
