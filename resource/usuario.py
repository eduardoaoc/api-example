from flask_restful import Resource, Api, reqparse
from pkg_resources import require
from models.usuario import *
#usados para verificação de senha e usuário
from flask_jwt_extended import create_access_token, jwt_required
from werkzeug.security import safe_str_cmp

#argumentos necessário para usuário fazer cadastro
atributos= reqparse.RequestParser()

atributos.add_argument('login', type=str, required=True, help="The field 'login' cannot be left blank.")
atributos.add_argument('senha', type=str, required=True, help="The field 'senha' cannot be left blank.")

class User(Resource):
    #/usuarios/{user_id}
    def get(self, user_id):
        user= UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'Message': 'User not found.'}, 404        

    @jwt_required()
    def delete(self, user_id):
        user= UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return {'Message': 'An error ocurred trying to delete.'}, 500      
            return {'Message': 'User deleted.'}
        return {'Message': 'User not found.'}, 404

class UserRegister(Resource):
    #/cadastro
    def post(self):
        #coleta os dados passados em atributos
        dados= atributos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {"Message": "The login '{}' already exists." .format(dados['login'])}
        
        user= UserModel(**dados)
        user.save_user()
        return {"Message": "User created successfuly!"}, 201 #CREATED


class UserLogin(Resource):

    @classmethod
    def post(cls):
        #coleta os dados passados em atributos
        dados= atributos.parse_args()
        #encontra o o usuários atráves do login
        user= UserModel.find_by_login(dados['login'])   
        #verificando a senha do usuário no banco de dados
        if user and safe_str_cmp(user.senha, dados['senha']):
            token_de_acesso= create_access_token(identity=user.user_id) 
            return {'access_token': token_de_acesso}, 200
        return {'Message': 'The username or password is incorrect.'}, 401 #Não autorizado