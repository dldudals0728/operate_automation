# -*- coding: utf-8 -*-
# Non-UTF-8 code starting with '\xeb' in file 해결방법: file 의 encoding을 utf-8로 바꾸는 것을 소스코드 맨 위에 추가.
import pymysql

class DB():
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = '123456'
        self.db = 'ac'
        self.conn = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db, charset='utf8')

    def SQL(self, sql_query):
        try:
            with self.conn.cursor() as curs:
                sql = sql_query
                curs.execute(sql)
                rs = curs.fetchall()

                return rs

        except Exception as e:
            print(e)
            return "error"
            try:
                print("SQL Exception -> connection close")
                # self.conn.close()
            except Exception as e:
                print(e)
                print("SQL Exception\ndatabase Exception: Connection is already closed!")

    def SELECTALL(self, table):
        try:
            with self.conn.cursor() as curs:
                # # 컬럼 수 가져오기
                # sql = "SELECT COUNT(*) FROM information_schema.columns WHERE table_name='{}' and table_schema='ac';".format(table)
                # curs.execute(sql)
                # rs = curs.fetchone()
                # cols = rs[0]

                sql = "SELECT * FROM {};".format(table)
                curs.execute(sql)
                rs = curs.fetchall()
                # for idx, row in enumerate(rs):
                #     connObj.insertRows(connObj.rowCount(), 1)
                #     for i in range(cols):
                #         connObj.setData(connObj.index(idx, i), row[i])
                # for i in range(len(rs)):
                #     connObj.insertRows(connObj.rowCount(), 1)
                #     for j in range(cols):
                #         connObj.setData(connObj.index(i, j), str(rs[i][j]))

                return rs

        except Exception as e:
            print(e)
            return "error"
            try:
                print("SELECTALL Exception -> connection close")
                # self.conn.close()
            except Exception as e:
                print(e)
                print("SELECTALL Exception\ndatabase Exception: Connection is already closed!")

    def SELECT(self, columns, table, where=None, fetchone=False):
        try:
            with self.conn.cursor() as curs:
                # 컬럼 수 가져오기
                # sql = "SELECT COUNT(*) FROM information_schema.columns WHERE table_name='{}' and table_schema='ac';".format(table)
                # curs.execute(sql)
                # rs = curs.fetchone()
                # cols = rs[0]

                if where == None:
                    sql = "SELECT {} FROM {};".format(columns, table)
                else:
                    sql = "SELECT {} FROM {} WHERE {};".format(columns, table, where)
                curs.execute(sql)
                if fetchone == True:
                    rs = curs.fetchone()
                else:
                    rs = curs.fetchall()
                # for idx, row in enumerate(rs):
                #     connObj.insertRows(connObj.rowCount(), 1)
                #     for i in range(cols):
                #         connObj.setData(connObj.index(idx, i), row[i])
                # for i in range(len(rs)):
                #     connObj.insertRows(connObj.rowCount(), 1)
                #     for j in range(cols):
                #         connObj.setData(connObj.index(i, j), str(rs[i][j]))

                return rs

        except Exception as e:
            print(e)
            return "error"
            try:
                print("SELECT Exception -> connection close")
                # self.conn.close()
            except Exception as e:
                print(e)
                print("SELECT Exception\ndatabase Exception: Connection is already closed!")

    def INSERT(self, table, values):
        try:
            with self.conn.cursor() as curs:
                # 컬럼 수 가져오기
                sql = "SELECT COUNT(*) FROM information_schema.columns WHERE table_name='{}' and table_schema='ac';".format(table)
                curs.execute(sql)
                rs = curs.fetchone()
                cols = rs[0]

                sql = "INSERT INTO {} VALUES({});".format(table, values)
                curs.execute(sql)
                self.conn.commit()

                # 데이터 삽입 후 treeview에 입력. 검색이 된 상태에서 삽입 시 문제 발생. delete 구문처럼 처리
                # connObj.insertRows(connObj.rowCount(), 1)
                # list = values.split(", ")
                # for i in range(len(list)):
                #     list[i] = list[i].replace("'", "")
                #     if list[i] == None or list[i] == "" or list[i] == pymysql.NULL:
                #         list[i] == pymysql.NULL

                # for i in range(cols):
                #     connObj.setData(connObj.index(connObj.rowCount() - 1, i), str(list[i]))

        except Exception as e:
            print(e)
            return "error"
            try:
                print("INSERT Exception -> connection close")
                # self.conn.close()
            except Exception as e:
                print(e)
                print("INSERT Exception\ndatabase Exception: Connection is already closed!")

    def DELETE(self, table, where):
        try:
            with self.conn.cursor() as curs:
                sql = "DELETE FROM {} WHERE {};".format(table, where)
                curs.execute(sql)
                self.conn.commit()

        except Exception as e:
            print(e)
            return "error"
            try:
                print("DELETE Exception -> connection close")
                # self.conn.close()
            except Exception as e:
                print(e)
                print("DELETE Exception\ndatabase Exception: Connection is already closed!")

    def UPDATE(self, table, modified, where):
        try:
            with self.conn.cursor() as curs:
                sql = "UPDATE {} SET {} WHERE {};".format(table, modified, where)
                curs.execute(sql)
                self.conn.commit()

        except Exception as e:
            print(e)
            return "error"
            try:
                print("UPDATE Exception -> connection close")
                # self.conn.close()
            except Exception as e:
                print(e)
                print("UPDATE Exception\ndatabase Exception: Connection is already closed!")


        # finally는 DBGUI에서 구현!
        # finally:
        #     self.conn.close()
