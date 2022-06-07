from flask import Flask
from flask_restful import  Api
from resource.hotel import *


app= Flask(__name__)
#configuração do caminho do banco de dados
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///banco.db'
app.config['SQLCHEMY_TRACK_MODIFICATIONS']= False
api= Api(app)

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



if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)
     