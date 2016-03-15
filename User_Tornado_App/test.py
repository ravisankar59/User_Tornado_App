from tornado import httpserver
from tornado import gen
from tornado.ioloop import IOLoop
import sqlite3 as sqlite
import tornado.web
import json


def execute(query):

        connection = sqlite.connect('User')
        cursorobj = connection.cursor()
        # print('EXECUTE ')
        try:
            cursorobj.execute(query)
            result = cursorobj.fetchall()
                # print(result)
            connection.commit()
        except Exception:
                        raise
        connection.close()
        return result


def UserDatabase():
    conn = sqlite.connect('User')
    c = conn.cursor()
    try:
        c.execute('SELECT * FROM user')
        # print(c.fetchall())
        print('Table already exists')
    except:
        # print("table does not exist")
        print('Creating table \'user\'')
        c.execute('CREATE TABLE user (\
            ID INTEGER PRIMARY KEY AUTOINCREMENT,\
            firstname text,\
            lastname text,\
            mobilenumber text,\
            address text)')
        print('Successfully created table \'user\'')
    conn.commit()
    conn.close()

class AddUser(tornado.web.RequestHandler):
    def get(self):
        query = '''SELECT * FROM user'''
        result = execute(query)
        
        self.write(json.dumps(dict(result=result)))

    def post(self):
        data = json.loads(self.request.body)
        fname = data.get('firstname')
        lname = data.get('lastname')
        phno = data.get('mobilenumber')
        address = data.get('address')
        query = ''' insert into user (firstname,lastname,mobilenumber,address) values ("{0}","{1}","{2}","{3}") '''.format(fname,lname,phno,address) ;
        result = execute(query)
        self.write(json.dumps(dict(result="Success")))

class SingleUserHandler(tornado.web.RequestHandler):

    def get(self, uid):
        query = '''select * from user where ID = "{0}"'''.format(uid);
        result = execute(query)
        self.write(json.dumps(dict(result=result)))

    # def put(self, uid):
    #     print "In PUT"
    #     data = json.loads(self.request.body)
    #     uid = data.get('id')
    #     fname = data.get('firstname')
    #     lname = data.get('lastname')
    #     phno = data.get('mobilenumber')
    #     address = data.get('address')
    #     query = ''' update user1 set address="kadapa" where id="{0}"'''.format(uid);
    #     result = execute(query)
    #     print result
    #     self.write(json.dumps(dict(result="Success")))

    # def delete(self, uid):
    #     # print("IN DEL")
    #     query = '''delete  from user1 where id = "{0}"'''.format(uid);
    #     print("i am here")
    #     result = execute(query)
        # print(result)
        # self.write(json.dumps(dict(result=result)))

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/users" ,AddUser),
            (r"/users/([^\/]+)", SingleUserHandler)
        ]
        tornado.web.Application.__init__(self, handlers)

def main():

    # Verify the database exists and has the correct layout
    UserDatabase()

    app = Application()
    app.listen(8000)
    IOLoop.instance().start()

if __name__ == '__main__':
    main()