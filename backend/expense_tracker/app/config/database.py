from sqlmodel import SQLModel, Session, create_engine
from app.config.settings import DATABASE_URL

# Connection string with no modification (sslmode=disable already included in the .env)
connection_string = str(DATABASE_URL)

engine = create_engine(
    connection_string, pool_recycle=300
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    
def get_session():
    with Session(engine) as session:
        yield session
