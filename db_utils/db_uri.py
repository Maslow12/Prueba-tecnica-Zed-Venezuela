import os
from dotenv import load_dotenv

load_dotenv()

host = os.getenv("MYSQL_HOST")
port = 3306
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
database = os.getenv("MYSQL_DATABASE")

def mariadb_uri_2():
    uri = "mysql+pymysql://test_user:admin@db:3306/test_db"
    print(uri)
    return uri
