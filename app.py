from flask import Flask
from flask_restful import  Api
from resource.hotel import *


app= Flask(__name__)
api= Api(app)

@app.route('/')
def index():
    return {'status':'running'}

#adiciona o recurso e escolhe o endereço de onde quer ser chamado (link)
api.add_resource(Hoteis, '/hoteis') 
api.add_resource(Hotel, '/hoteis/<string:hotel_id>') 



if __name__ == '__main__':
    app.run(debug=True)
     