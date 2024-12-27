import sqlite3
import json
from datetime import datetime

def db(database_name='DataBase/Server_DB.db'):
    return sqlite3.connect(database=database_name)

def sqlite_query_commit(query, args=()):
    try:
        cur = db().cursor()
        cur.execute(query, args)           
        cur.connection.commit()
        cur.connection.close()
        return {"commit_status": "sucsessful"}
    except Exception as e:
        return {"commit_status": str(e)}

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
        if "Connection" not in JSONData.keys():
            return returnJSON(0, JSONData).encode()
        ClientAuthorization = sqlite_query_to_json(f'SELECT * FROM users WHERE userLogin = "{JSONData["authorization"][0]}" AND userPassword = "{JSONData['authorization'][1]}"', (), True)
        if ClientAuthorization != "None" and "Query_exception" not in ClientAuthorization.keys():
            CurrentDateTime = datetime.today().strftime('%Y%m%d %H%M%S') 
            SessionQuery = sqlite_query_to_json(f'SELECT * FROM sessions WHERE session_id = "{JSONData["Connection"]}"', (), True)
            if SessionQuery == "None":
                SessionUpdate = sqlite_query_commit(f'INSERT INTO sessions (user_id, IsActive, session_data) VALUES ("{ClientAuthorization["id"]}", 1, "{CurrentDateTime}")', ())
                SessionUpdate = { "session_status": SessionUpdate, 
                    "user_id": ClientAuthorization["id"]}
                return ProcessReqExcept(SessionUpdate)   
            elif SessionQuery["IsActive"] == 1:
                SessionQuery["session_exception"] = "Session already active"
                return returnJSON(1, SessionQuery)
            elif SessionQuery["IsActive"] == 0:
                return ProcessReqExcept(sqlite_query_commit(f'UPDATE sessions SET IsActive = 1, session_data = {CurrentDateTime} WHERE user_id = {ClientAuthorization["id"]} AND session_id = "{JSONData["Connection"]}"', ()))   
        else:
            return ProcessReqExcept(ClientAuthorization)           
    elif 'end_session' in JSONData.keys():
        return ProcessReqExcept(sqlite_query_commit(f'UPDATE sessions SET IsActive = 0 WHERE user_id = "{JSONData["get_session"]}" AND session_id = "{JSONData["Connection"]}"', (), True))
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