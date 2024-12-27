import sqlite3
import json

def db(database_name='DataBase/Server_DB.db'):
    return sqlite3.connect(database=database_name)
    
    
def sqlite_query_to_json(query, args=(), one=False):
    try:
        cur = db().cursor()
        cur.execute(query, args)
        r = [dict((cur.description[i][0], value if value != None else str(value)) \
                    for i, value in enumerate(row)) for row in cur.fetchall()]
        cur.connection.close()
        return (r[0] if r else "None") if one else r
    except Exception as e:
        return {"Query_exception": str(e)} 

def processCommand(JSONData):

    if 'name' in JSONData:
        return f'Hello, {JSONData['name']}'.encode()
    elif 'authorization' in JSONData.keys():
         return ProcessReqExcept(sqlite_query_to_json(f'SELECT * FROM users WHERE userLogin = "{JSONData["authorization"][0]}" AND userPassword = "{JSONData['authorization'][1]}"', (), True))
    elif 'get_session' in JSONData.keys():
        return ProcessReqExcept(sqlite_query_to_json(f'SELECT * FROM sessions WHERE user_id = "{JSONData["get_session"]}" AND session_id = "{JSONData["connection"]}"', (), True)) 
    else:
        return returnJSON(0, JSONData).encode() 



def returnJSON(status = 0, JSONData = ""):
    try:
        JSONData = json.loads(str(JSONData))
        JSONResponse = {"status": status}
        JSONResponse["call_Return"] = JSONData
    except ValueError as e:
        JSONResponse = {"Status": status,
                    "return_data": JSONData,
                    "encode_exception": str(e)}
    
    return str(JSONResponse)
 
def ProcessReqExcept(ReqString):
    if ReqString == "None":
        return returnJSON(3, ReqString).encode()
    elif 'Query_exception' in ReqString:
        return returnJSON(5, ReqString).encode()
    else:
        return returnJSON(10, ReqString).encode()   