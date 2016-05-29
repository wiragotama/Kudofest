import pandas as pd
import sqlalchemy as sa
import yaml

import pandas as pd
import sqlalchemy as sa
import yaml


class MySQLConnector:

    def __init__(self):
        hostname = "localhost"
        dbName = "kudofest"
        tableName = "ratings"
        usr = "root"
        password = ""
        if (password is None):
            password = ""

        self.connectionName = "mysql+pymysql://"+usr+":"+password+"@"+hostname+"/"+dbName
        self.engine = sa.create_engine(self.connectionName)
        self.data = pd.read_sql(tableName, self.engine)

        print("Read ratings done");

        hostname = "localhost"
        dbName = "kudofest"
        tableName = "users"
        usr = "root"
        password = ""
        if (password is None):
            password = ""

        self.connectionName = "mysql+pymysql://" + usr + ":" + password + "@" + hostname + "/" + dbName
        self.engine = sa.create_engine(self.connectionName)
        self.users = pd.read_sql(tableName, self.engine)

        print("Read users done");

        # movie table preparation
        self.result = []
        for i in range (0, 3953):
            # print(i)
            self.result.append([])
            self.result[i].append(i)
            self.result[i].append(0)

        for idx in range(len(self.data)):
            # print (self.data.iat[idx,1])
            if ((self.users.iat[self.data.iat[idx,0]-1, 2] == 45) or
                (self.users.iat[self.data.iat[idx,0]-1, 2] == 50) or
                (self.users.iat[self.data.iat[idx, 0] - 1, 2] == 59)): # age
                self.result[ self.data.iat[idx,1] ][1]+=1
        print("Data has parsed")

    def all_data(self):
        """
        Return all instances in CSV file

        :return: pandas DataFrame
        """
        return self.data

    def to_csv(self, filename):
        # save to file
        file = open(filename, 'w')
        file.write('id_movie, rater_count\n')
        for idx in range(len(self.result)):
            for j in range(len(self.result[idx])):
                file.write(str(self.result[idx][j]))
                file.write(', ')
            file.write('\n')

con = MySQLConnector()
print (con.to_csv("old_rater.csv"))