

from pymysql import *

class py_mysql(object):

    def __init__(self, host, port, user, passwd, db, charset):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db
        self.charset = charset
        try:
            print(self.host, self.port, self.user, self.passwd, self.db, self.charset)
            self.conn = connect(host = self.host, port = self.port, user = self.user, passwd = self.passwd, db = self.db, charset = self.charset)
        except Exception as e:
            print(e)
            print('fail!!!')
        else:
            print('connect ok')
            self.curssor = self.conn.cursor()


    def add(self, params=[]):
        sql = 'insert into login values(%s,%s,%s,%s,%s,%s)'
        res = self.curssor.execute(sql, params)

        if res:
            self.conn.commit()
        else:
            self.conn.rollback()
        print (res)

#        self.curssor.close()
#        self.conn.close()

    def delete(self, params):
        sql = 'delete from login where id = %s'
        res = self.curssor.execute(sql, params)

        if res:
            self.conn.commit()
        else:
            self.conn.rollback()
        print(res)

    def update(self, params):
        sql = 'update login set %s = %s where id = %s'
        res = self.curssor.execute(sql, params)

        if res:
            self.conn.commit()
        else:
            self.conn.rollback()
        print(res)

    def select(self, params):
        sql = 'select * from login'

#        print('------%s-----'%params)

        if params[0] == 'one':
            self.curssor.execute(sql)
            result = self.curssor.fetchone()
            print('select one ok')
        elif params[0] == 'all':
            self.curssor.execute(sql)
            result = self.curssor.fetchall()
            print('select all ok')
        else:
            print('command wrong!')
            result = NULL

        return result

    def close(self):
        self.curssor.close()
        self.conn.close()

class Userlogin(py_mysql):
#    def __init__(self, host, port, user, passwd, db, charset):#此处若不定义__init__函数则默认使用父类的__init__函数
#        super(Userlogin,self).__init__(host, port, user, passwd, db, charset)#此处若定义__init__函数可通过此方式调用父类的__init__函数
#  以上调用父类中的__init__函数的作用是使用父类中创建的一些局部变量，该类添加的局部变量可在此处及以下继续添加
    def login(self, user, passwd):
        sql = 'select passwd from login where name = %s'
        params = [user]
        res = self.curssor.execute(sql, params)

        if res:
            result = self.curssor.fetchone()
#            print('----result:%s-----'%result)
            print('select ok....')
        else:
            result = NULL
            print('username wrong!!!')

#        print('---result:%s---passwd:%s---'%(result,passwd))
        if result[0] == passwd:
            print(' login sucess....')
        else:
            print('passwd wrong!!!!')

    def join(self, user, passwd):
        sql = 'select passwd from login where name = %s'
        params = [user]
        res = self.curssor.execute(sql, params)
        if res:
            print('username exists, change it!!')
            return 0
        else:
            print('username can join...')

        sql = 'insert into login(name,passwd) values(%s,%s)'
        params = [user, passwd]

        res = self.curssor.execute(sql, params)
        if res:
            self.conn.commit()
            print('insert ok...')
        else:
            self.conn.rollback()
            print('insert fail!!!')

        return 1
        

if __name__ == '__main__':

#    database = input('please input the database: ')
#    mysql = py_mysql(host = '192.168.31.216', port = 3306, user = 'root', passwd = 'dzy', db = 'python3', charset = 'utf8')

#    params = [0, 'll', '123456', '34567890', 'pudong', 0]
#    mysql.add(params)

#    params = ['all']
#    data = mysql.select(params)
#    print(data)

    login = Userlogin(host = '192.168.31.216', port = 3306, user = 'root', passwd = 'dzy', db = 'python3', charset = 'utf8')
#    login.login('ll', '123456')
    
    result = login.join('ggg','333333')
    if result:
        print('join sucess...')
    else:
        print('join fail !!')

    login.close()

    print('OK!!')
