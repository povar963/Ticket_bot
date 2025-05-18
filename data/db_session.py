from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

BaseModel = declarative_base()

__factory = None


def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = create_engine(conn_str, echo=False)
    __factory = sessionmaker(bind=engine)

    from . import __all_models

    BaseModel.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
