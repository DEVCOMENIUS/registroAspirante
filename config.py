import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_key_local")

    # Obtén la URL de MySQL de Railway
    database_url = os.getenv("MYSQL_URL")

    if database_url and database_url.startswith("mysql://"):
        database_url = database_url.replace("mysql://", "mysql+pymysql://", 1)

    # SQLAlchemy usa la URL de Railway si existe
    SQLALCHEMY_DATABASE_URI = database_url or "mysql+pymysql://root:@localhost/sistema_aspirantes"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

 