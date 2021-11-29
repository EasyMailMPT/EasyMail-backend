import sqlalchemy as sqa
import sqlalchemy.orm as orm

#Definicje
Base = orm.declarative_base()
engine = sqa.create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)


# Funkcje
def add_user(session : orm.Session, username, hashed_passwd, user_email ):
    session.add(User(username=username, passwd=hashed_passwd, user_email=user_email))


def add_query(session : orm.Session, query):
    """Adds query to database"""
    session.add(Query(query=query))
    try:
        session.flush()
    except sqa.exc.IntegrityError:
        print("Error: Such Querry already exist")
        session.rollback()



# Tablice
class User(Base):
    """Definicja tabeli z nazwami użytkownika; Długość nazwy użytkownika to 30 znaków"""
    __tablename__ = 'user_table'

    id = sqa.Column(sqa.Integer, primary_key=True)
    username = sqa.Column(sqa.String(30), nullable=False)
    passwd = sqa.Column(sqa.String(256), nullable=False)
    user_email = sqa.Column(sqa.String)

    def __repr__(self):
        return "id={}, Username = {}, email = {}".format(self.id, self.username, self.user_email)


class Email(Base):
    """Tablica z wynikami sercha emaili"""
    __tablename__ = 'email_table'

    id = sqa.Column(sqa.Integer, primary_key=True)
    query = sqa.Column(sqa.String, sqa.ForeignKey('query_results.query'))
    email = sqa.Column(sqa.String, nullable=False)
    source_url = sqa.Column(sqa.String)

    query_backref = orm.relationship("Query", backref='email_table')

    def __repr__(self):
        return " Query = {}, email = {}, source = {} ".format(self.query, self.email, self.source_url)


class Query(Base):
    """Zapytania do silnika"""
    __tablename__ = 'query_results'

    id = sqa.Column(sqa.Integer, primary_key=True)
    query = sqa.Column(sqa.String, nullable=False, unique=True)

    def __repr__(self):
        return "Id={}, Query = {}".format(self.id, self.query)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    with orm.Session(engine) as session:
        add_user(session, username='abc', hashed_passwd='password', user_email='email')
        add_query(session, "architekt")
        add_query(session, "architekt2")
        session.commit()


        result = session.execute(sqa.select(Query))
        for row in result:
            print(row)




