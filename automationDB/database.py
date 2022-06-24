# -*- coding: utf-8 -*-
# Non-UTF-8 code starting with '\xeb' in file 해결방법: file 의 encoding을 utf-8로 바꾸는 것을 소스코드 맨 위에 추가.
import pymysql
import os
import datetime

import logging

from pymysql import MySQLError

class DB():
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = '123456'
        self.db = 'ac'
        self.conn = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db, charset='utf8')

        self.logger = logging.getLogger("DATABASE log")
        fileHandler = logging.FileHandler("D:\\Master\\log\\Program log.log")

        formatter = logging.Formatter('[%(asctime)s][%(levelname)s|%(filename)s:%(lineno)s] in <%(funcName)s> %(name)s >> %(message)s')
        fileHandler.setFormatter(formatter)

        self.logger.addHandler(fileHandler)
        self.logger.setLevel(level=logging.DEBUG)

    def SQL(self, sql_query):
        try:
            with self.conn.cursor() as curs:
                sql = sql_query
                curs.execute(sql)
                rs = curs.fetchall()

                self.logger.debug("#SQL SELF QUERY running <{}>".format(sql_query))
                self.logger.info("$SQL SELF QUERY result ==> [{}]".format(rs))
                return rs

        except Exception as e:
            print(e)
            self.logger.error("!SQL SELF QUERY Exception Handling <{}>".format(e))
            return "error"
            try:
                print("SQL Exception -> connection close")
                # self.conn.close()
            except Exception as e:
                print(e)
                print("SQL Exception\ndatabase Exception: Connection is already closed!")

    def SELECT(self, columns, table, where=None, orderBy=None, fetchone=False):
        try:
            with self.conn.cursor() as curs:
                # 컬럼 수 가져오기
                # sql = "SELECT COUNT(*) FROM information_schema.columns WHERE table_name='{}' and table_schema='ac';".format(table)
                # curs.execute(sql)
                # rs = curs.fetchone()
                # cols = rs[0]

                sql = "SELECT {} FROM {}".format(columns, table)

                if where == None:
                    where = "None"
                    pass
                else:
                    sql += " WHERE {}".format(where)

                if orderBy == None:
                    pass
                else:
                    sql += " ORDER BY {}".format(orderBy)

                sql += ";"

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

                if columns == "*":
                    columns = "all attribute"
                
                self.logger.debug("#SQL SELECT running <{}>".format(sql))
                # 테이블 새로고침 시에는 출력 X
                if where != "None":
                    self.logger.info("$SQL SELECT result ==> [TABLE|{}]에서 [COLUMNS|{}]검색. 조건[WHERE|{}]\n[RESULT|{}]".format(table, columns, where, rs))
                return rs

        except Exception as e:
            print(e)
            self.logger.error("!SQL SELECT Exception Handling <{}>".format(e))
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
                self.logger.debug("#SQL INSERT running <{}>".format(sql))
                self.logger.info("$SQL INSERT result ==> [TABLE|{}]에 [VALUES|{}]삽입\n[RESULT|NULL]".format(table, values))

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
            self.logger.error("!SQL INSERT Exception Handling <{}>".format(e))
            MySQLError.with_traceback()
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
                self.logger.debug("#SQL DELETE running <{}>".format(sql))
                self.logger.info("$SQL DELETE result ==> [TABLE|{}]에서 조건: [WHERE|{}]인 데이터 삭제".format(table, where))

        except Exception as e:
            print(e)
            self.logger.error("!SQL DELETE Exception Handling <{}>".format(e))
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
                self.logger.debug("#SQL UPDATE running <{}>".format(sql))
                self.logger.info("$SQL UPDATE result ==> [TABLE|{}]에서 [WHERE|{}]인 데이터를 [SET|{}](으)로 변경".format(table, where, modified))

        except Exception as e:
            print(e)
            self.logger.error("!SQL UPDATE Exception Handling <{}>".format(e))
            return "error"
            try:
                print("UPDATE Exception -> connection close")
                # self.conn.close()
            except Exception as e:
                print(e)
                print("UPDATE Exception\ndatabase Exception: Connection is already closed!")

    def dDayCheck(self, doc_type, isDeadline=False):
        try:
            with self.conn.cursor() as curs:
                if isDeadline == True:
                    if doc_type == "개강보고":
                        comparison = "startDate"
                        # 개강보고는 개강 후 3일 이내에 보고해야 하기 때문에 d-day에 3일을 더해준다.
                        sql = "select *, TIMESTAMPDIFF(DAY, startDate, CURDATE()) as 'D-day' from lecture where TIMESTAMPDIFF(DAY, startDate, CURDATE()) <= 2"

                    elif doc_type == "대체실습 실시보고":
                        comparison = "startDate"
                        sql = "select *, TIMESTAMPDIFF(DAY, startDate, CURDATE()) as 'D-day' from temptraining where TIMESTAMPDIFF(DAY, startDate, CURDATE()) <= 0"

                    elif doc_type == "대체실습 수료보고":
                        comparison = "endDate"
                        sql = "select *, TIMESTAMPDIFF(DAY, endDate, CURDATE()) as 'D-day' from temptraining where TIMESTAMPDIFF(DAY, endDate, CURDATE()) <= 2"

                    elif doc_type == "응시원서 접수시작":
                        comparison = "startAcceptance"
                        sql = "select *, TIMESTAMPDIFF(DAY, startAcceptance, CURDATE()) as 'D-day' from exam where TIMESTAMPDIFF(DAY, startAcceptance, CURDATE()) <= 0"

                    elif doc_type == "응시원서 접수마감":
                        comparison = "endAcceptance"
                        sql = "select *, TIMESTAMPDIFF(DAY, endAcceptance, CURDATE()) as 'D-day' from exam where TIMESTAMPDIFF(DAY, endAcceptance, CURDATE()) <= 0"

                    elif doc_type == "응시표 출력":
                        comparison = "announceDate"
                        sql = "select *, TIMESTAMPDIFF(DAY, announceDate, CURDATE()) as 'D-day' from exam where TIMESTAMPDIFF(DAY, announceDate, CURDATE()) <= 2"

                    elif doc_type == "시험 합격자 서류":
                        comparison = "submitDate"
                        sql = "select *, TIMESTAMPDIFF(DAY, submitDate, CURDATE()) as 'D-day' from exam where TIMESTAMPDIFF(DAY, submitDate, CURDATE()) <= 0"

                    sql +=  " and TIMESTAMPDIFF(DAY, {}, CURDATE()) >= -7".format(comparison)
                        # 합격자 명단 + 3서류
                else:
                    if doc_type == "개강보고":
                        comparison = "startDate"
                        # 개강보고는 개강 후 3일 이내에 보고해야 하기 때문에 d-day에 3일을 더해준다.
                        sql = "select *, TIMESTAMPDIFF(DAY, startDate, CURDATE()) as 'D-day' from lecture where TIMESTAMPDIFF(DAY, startDate, CURDATE()) <= -8"

                    elif doc_type == "대체실습 실시보고":
                        comparison = "startDate"
                        sql = "select *, TIMESTAMPDIFF(DAY, startDate, CURDATE()) as 'D-day' from temptraining where TIMESTAMPDIFF(DAY, startDate, CURDATE()) <= -8"

                    elif doc_type == "대체실습 수료보고":
                        comparison = "endDate"
                        sql = "select *, TIMESTAMPDIFF(DAY, endDate, CURDATE()) as 'D-day' from temptraining where TIMESTAMPDIFF(DAY, endDate, CURDATE()) <= -8"

                    elif doc_type == "응시원서 접수시작":
                        comparison = "startAcceptance"
                        sql = "select *, TIMESTAMPDIFF(DAY, startAcceptance, CURDATE()) as 'D-day' from exam where TIMESTAMPDIFF(DAY, startAcceptance, CURDATE()) <= -8"

                    elif doc_type == "응시원서 접수마감":
                        comparison = "endAcceptance"
                        sql = "select *, TIMESTAMPDIFF(DAY, endAcceptance, CURDATE()) as 'D-day' from exam where TIMESTAMPDIFF(DAY, endAcceptance, CURDATE()) <= -8"

                    elif doc_type == "응시표 출력":
                        comparison = "announceDate"
                        sql = "select *, TIMESTAMPDIFF(DAY, announceDate, CURDATE()) as 'D-day' from exam where TIMESTAMPDIFF(DAY, announceDate, CURDATE()) <= -8"

                    elif doc_type == "시험 합격자 서류":
                        comparison = "passDate"
                        sql = "select *, TIMESTAMPDIFF(DAY, passDate, CURDATE()) as 'D-day' from exam where TIMESTAMPDIFF(DAY, passDate, CURDATE()) <= -8"

                    sql +=  " and TIMESTAMPDIFF(DAY, {}, CURDATE()) > -100".format(comparison)

                sql += ";"
                curs.execute(sql)
                rs = curs.fetchall()

                return rs;



        except Exception as e:
            print(e)
            return "error"

    def dropDatabase(self, db_name):
        sql = "drop database " + db_name
        # try:
        with self.conn.cursor() as curs:
            curs.execute(sql)

        # except Exception as e:
        #     print(e)
        #     print("error!")

    def createDatabase(self, db_name):
        sql = "create database " + db_name
        # try:
        with self.conn.cursor() as curs:
            curs.execute(sql)

        # except Exception as e:
        #     print(e)
        #     print("error!")

    def dumpDatabase(self, file_path=None, daily=False):
        today = datetime.date.today().strftime("%Y-%m-%d")
        os.chdir(r"C:\Bitnami\wampstack-8.1.1-0\mariadb\bin")
        if daily == True:
            if os.path.exists(r"C:\Bitnami\wampstack-8.1.1-0\mariadb\bin\database_dump\ac_bak_{}.sql".format(today)):
                return
            # os.system("mysqldump -u root -p123456 --default-character-set=utf8 --databases ac > C:/Bitnami/wampstack-8.1.1-0/mariadb/bin/database_dump/ac_bak_{}.sql".format(today))
            os.system("mysqldump -u root -p123456 --databases ac > C:/Bitnami/wampstack-8.1.1-0/mariadb/bin/database_dump/ac_bak_{}.sql".format(today))

        save_path = "C:/Bitnami/wampstack-8.1.1-0/mariadb/bin/database_dump/ac_bak_{}.sql".format(today)
        if file_path != None:
            save_path = file_path

        # os.system("mysqldump -u root -p123456 --default-character-set=utf8 --databases ac > {}".format(save_path))
        os.system("mysqldump -u root -p123456 --databases ac > {}".format(save_path))
        self.logger.info("$SQL DUMP DB ==> [{}]파일 저장 완료(자동저장 X)".format(file_path))

    def applyDatabase(self, dump_file_path):
        self.dropDatabase("ac")
        self.createDatabase("ac")
        os.chdir(r"C:\Bitnami\wampstack-8.1.1-0\mariadb\bin")
        try:
            # os.system("mysqldump -u root -p123456 --default-character-set=utf8 --databases ac < {}".format(dump_file_path))
            os.system("mysql -u root -p123456 ac < {}".format(dump_file_path))
            self.logger.info("$SQL APPLY DB ==> [{}]파일로 DB 변경".format(dump_file_path))
            return True
        except:
            return False


        # finally는 DBGUI에서 구현!
        # finally:
        #     self.conn.close()

if __name__ == "__main__":
    db = DB()
    # db.dumpDatabase()