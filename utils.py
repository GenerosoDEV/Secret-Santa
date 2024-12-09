from sqlite3 import Error
import sqlite3, os

os.makedirs("./data", exist_ok=True)

def connectToDatabase():
    caminho = './data/data.db'
    con=None
    try:
        con=sqlite3.connect(caminho, check_same_thread=False)
    except Error as ex:
        print(ex)
    return con

vcon = connectToDatabase()

def dbQuery(sql, params=None):
    conexao = vcon
    c = conexao.cursor()
    if params:
        if isinstance(params, tuple) or isinstance(params, list):
            c.execute(sql, params)
        else:
            c.execute(sql, (params,))
    else:
        c.execute(sql)
    
    resultado = c.fetchall()
    if resultado == []:
        return None
    else:
        return resultado

def dbExec(sql, params=None):
    conexao = vcon
    try:
        c = conexao.cursor()
        if params:
            if isinstance(params, tuple) or isinstance(params, list):
                c.execute(sql, params)
            else:
                c.execute(sql, (params,))
        else:
            c.execute(sql)
        conexao.commit()
    except Exception as ex:
        print(ex)

dbExec("""CREATE TABLE IF NOT EXISTS match (
    raffle_code TEXT NOT NULL
                     REFERENCES raffles (code) ON DELETE CASCADE
                                               ON UPDATE CASCADE,
    gifter_code TEXT NOT NULL,
    gifter      TEXT NOT NULL,
    gifted      TEXT NOT NULL
);
""")

dbExec("""CREATE TABLE IF NOT EXISTS raffles (
    code         TEXT NOT NULL
                      UNIQUE,
    participants TEXT NOT NULL
);
""")