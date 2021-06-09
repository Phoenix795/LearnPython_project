from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.session import Session

DBMS_LINK = "mysql+pymysql://root:Mysql123@localhost:3306/atlassiandb"

engine = create_engine(DBMS_LINK)
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property