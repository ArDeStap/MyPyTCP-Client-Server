import sqlite3
import json

def db(database_name='DataBase/Server_DB.db'):
    return sqlite3.connect(database=database_name)
    
    
def sqlite_query_to_json(query, args=(), one=False):
    cur = db().cursor()
    cur.execute(query, args)
    r = [dict((cur.description[i][0], value) \
                for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.connection.close()
    return (r[0] if r else None) if one else r


def processCommand(JSONData):

    if 'name' in JSONData:
        return f'Hello, {JSONData['name']}'.encode()
    elif 'authorization' in JSONData:
        regreq = authorizationRequest(JSONData)
        if regreq == None:
            return returnJSON(3, regreq).encode()
        elif 'Query_exception' in regreq:
            return returnJSON(5, regreq).encode()
        else:
            return returnJSON(10, regreq).encode()                                
    else:
        return returnJSON(0, regreq).encode() 



def returnJSON(status = 0, JSONData = ""):
    try:
        JSONData = json.loads(str(JSONData))
        JSONResponse = {"status": status}
        JSONResponse["call_Return"] = JSONData
    except ValueError as e:
        JSONResponse = {"Status": status,
                    "return_data": JSONData,
                    "encode_exception": e}
    
    return str(JSONResponse)


def registrationRequest(DataArray):
    try:
        QueryResult = sqlite_query_to_json(f'INSERT INTO users (userName, userSecondName, userLogin, userPassword, userRules) VALUES ("{DataArray[0]}","{DataArray[1]}", "{DataArray[2]}", "{DataArray[3]}", "{DataArray[4]}")')
    
    except ValueError as e:
        QueryResult = {"Query_exception": e} 

    return QueryResult

def authorizationRequest(DataArray):
    try:
        QueryResult = sqlite_query_to_json(f'SELECT * FROM users WHERE userLogin = "{DataArray["authorization"][0]}" AND userPassword = "{DataArray['authorization'][1]}"', (), True)

    except ValueError as e:
        QueryResult = {"Query_exception": e} 

    return QueryResult