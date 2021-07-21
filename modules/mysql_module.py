import pymysql 

class SQL():
    #create connect based on db name
    def __init__(self, host,user,password,database):
        self.conn_kwargs = {
            'host':host,
            'user':user,
            'password': password
        }
        self.db_name = database

    # connect
    def db_connect(self):
        conn = pymysql.connect(db = self.db_name, **self.conn_kwargs)
        cur = conn.cursor()
        return conn, cur

    # connect and return dict
    def db_dict_connect(self):
        conn = pymysql.connect(db = self.db_name, **self.conn_kwargs)
        cur = conn.cursor(pymysql.cursors.DictCursor)
        return conn, cur
    
    def fetch_list(self, sql_sentence,*values, fetch_method = 'all'):
        conn, cur = self.db_connect()
        cur.execute(sql_sentence, values)
        if fetch_method == 'all':
            result = cur.fetchall()
        elif fetch_method == 'one':
            result = cur.fetchone()
        conn.close()
        return result
    
    def fetch_dict(self, sql_sentence,*values ,fetch_method = 'all'):
        conn, cur = self.db_dict_connect()
        cur.execute(sql_sentence, values)
        if fetch_method == 'all':
            result = cur.fetchall()
        elif fetch_method == 'one':
            result = cur.fetchone()
        conn.close()
        return result

    def execute(self, sql_sentence, *values):
        conn, cur = self.db_dict_connect()
        cur.execute(sql_sentence, values)
        conn.commit()
        conn.close()
    
    def bulk_execute(self, sql_sentence,values):
        conn, cur = self.db_dict_connect()
        cur.executemany(sql_sentence,values)
        conn.commit()
        conn.close()
    
