import sqlite3

class JSONCommands:
    def processCommand(JSONData):
        try:
            connection = sqlite3.connect('DataBase/Server_DB.db')
            cursor = connection.cursor()
        except:
            return 'DATABASE ERROR'
        
        if 'name' in JSONData:
            return f'Hello, {JSONData['name']}'.encode()
        elif 'authorization' in JSONData:
            query = cursor.execute(f'SELECT id, userName FROM users WHERE userLogin = "{JSONData['authorization'][0]}" AND userPassword = "{JSONData['authorization'][1]}"')
            QueryResult = query.fetchone()
            if QueryResult == None:
                return "wrong login or password".encode()
            else:
                return f"authorization was sucsessful! Hello, {QueryResult[1]}".encode()                                
        else:
            return 'Wrong Data'.encode() 