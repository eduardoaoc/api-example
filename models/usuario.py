from sql_alchemy import banco

class UserModel(banco.Model):
    #mapeamento para que essa classe seja entendida como uma tabela no banco de dados
    __tablename__= 'usuarios'

    user_id= banco.Column(banco.Integer, primary_key=True)
    login= banco.Column(banco.String(40))
    senha= banco.Column(banco.String(40))

    def __init__(self, login, senha):
        self.login= login 
        self.senha= senha    

    def json(self):
        return {
            'user_id': self.user_id,
            'login': self.login       
        }  

    @classmethod
    def find_user(cls, user_id):
        #faz a consulta do banco, SELECT * FROM hoteis WHERE hotel_id = hotel_id que esta sendo passado
        user= cls.query.filter_by(user_id=user_id).first()
        if user:
            return user
        return None

    @classmethod    
    def find_by_login(cls, login):
        #faz a consulta do banco, SELECT * FROM hoteis WHERE hotel_id = hotel_id que esta sendo passado
        login= cls.query.filter_by(login = login).first()
        if login:
            return login
        return None
    #abre uma conexão com o banco e adiciona o proprio obj ao banco, ele sabe quais foram os argumentos passado e adiciona.
    def save_user(self):
        banco.session.add(self)        
        banco.session.commit()

    #função criada para deletar hotel
    def delete_user(self):
        banco.session.delete(self)    
        banco.session.commit()
      