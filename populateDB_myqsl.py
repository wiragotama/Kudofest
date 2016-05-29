import sqlalchemy as sa
import pandas as pd
import yaml
import json
from sqlalchemy import *

dbName = "kudofest"
hostname = "localhost"
usr = "root"
tableName = "youngster_raters"
password = ""

engine_statement = "mysql+pymysql://"+usr+":"+password+"@"+hostname+"/"+dbName
engine = sa.create_engine(engine_statement,)
chunks = pd.read_csv('CSV/youngster_raters.csv')
chunks.to_sql(name=tableName, con=engine, flavor="mysql", index=false, index_label="id_movie", if_exists="replace")

# metadata = MetaData()
# T = Table(tableName, metadata,
#     Column('id_movie', BigInteger, nullable=False),
#     Column('rater_count', Integer, nullable=False, default=0),
#     )
# metadata.create_all(engine)
# L = json.loads(chunks.to_json(orient="records"))
# engine.execute(T.insert(), L)
