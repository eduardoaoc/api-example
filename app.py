from flask import Flask
from flask_restful import  Api
from resource.hotel import *
from resource.usuario import *
from flask_jwt_extended import JWTManager


app= Flask(__name__)
#configuração do caminho do banco de dados
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///banco.db'
app.config['SQLCHEMY_TRACK_MODIFICATIONS']= False
#Chave de autenticação
app.config['JWT_SECRET_KEY']= 'DontTell'
api= Api(app)

jwt= JWTManager(app)

#Depois da primeira requisição cria banco.
@app.before_first_request
def cria_banco():
    banco.create_all()

@app.route('/')
def index():
    return {'status':'running'}

#adiciona o recurso e escolhe o endereço de onde quer ser chamado (link)
api.add_resource(Hoteis, '/hoteis') 
api.add_resource(Hotel, '/hoteis/<string:hotel_id>') 
api.add_resource(User, '/usuarios/<int:user_id>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/login')

if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)
     