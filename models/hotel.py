from sql_alchemy import banco

class HotelModel(banco.Model):
    #mapeamento para que essa classe seja entendida como uma tabela no banco de dados
    __tablename__= 'hoteis'

    hotel_id= banco.Column(banco.String, primary_key=True)
    nome= banco.Column(banco.String(80))
    estrelas= banco.Column(banco.Float(precision=1)) #precision define quantas casas terá após a vírgula
    diaria= banco.Column(banco.Float(precision=2))
    cidade= banco.Column(banco.String(40))

    def __init__(self, hotel_id, nome, estrelas, diaria, cidade):
        self.hotel_id= hotel_id
        self.nome= nome
        self.estrelas= estrelas
        self.diaria= diaria
        self.cidade= cidade

    def json(self):
        return {
            'hotel_id': self.hotel_id,
            'nome': self.nome,
            'estrelas': self.estrelas,
            'diaria': self.diaria,
            'cidade': self.cidade
        }   

    @classmethod
    def find_hotel(cls, hotel_id):
        #faz a consulta do banco, SELECT * FROM hoteis WHERE hotel_id = hotel_id que esta sendo passado
        hotel= cls.query.filter_by(hotel_id=hotel_id).first()
        if hotel:
            return hotel
        return None

    #abre uma conexão com o banco e adiciona o proprio obj ao banco, ele sabe quais foram os argumentos passado e adiciona.
    def save_hotel(self):
        banco.session.add(self)        
        banco.session.commit()

    def update_hotel(self, nome, estrelas, diaria, cidade):
        self.nome= nome
        self.estrelas= estrelas
        self.diaria= diaria
        self.cidade= cidade  

    #função criada para deletar hotel
    def delete_hotel(self):
        banco.session.delete(self)    
        banco.session.commit()
        