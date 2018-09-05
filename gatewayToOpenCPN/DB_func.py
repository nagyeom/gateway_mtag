import pymysql

class MySQLSet():
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='123456', db='mysql', charset='utf8')
        #select_curs = self.conn.cursor(pymysql.cursors.DictCursor)
        #self.insert_curs = self.conn.cursor()



    def selectGPS(self,sql):
        rows = None
        select_curs = self.conn.cursor(pymysql.cursors.DictCursor)
        #sql = "select * from gps_log"
        try:
            select_curs.execute(sql)
        except:
            pass
        else:
            rows = select_curs.fetchall()
        finally:
            select_curs.close()
            print("==select ok==")
        #self.conn.close()
        return rows


    def insertGPS(self,tag_id,lat,lon,time):
        select_curs = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "insert into gps_log(tag_id,lat,lon,time) values (%s, %s, %s, %s)"
        try:
            select_curs.execute(sql,(tag_id,lat,lon,time))
        except:
            pass
        finally:
            self.conn.commit()
            select_curs.close()
        #self.conn.close()

    def insertDummyGPS(self,sql):
        """
        ready-made gps_log dummy data
        """
        select_curs = self.conn.cursor(pymysql.cursors.DictCursor)
        print(sql)
        try:
            select_curs.execute(sql)
        except:
            pass
        finally:
            self.conn.commit()
            select_curs.close()

    def deleteGPS(self):
        select_curs = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "delete from gps_log"
        select_curs.execute(sql)
        self.conn.commit()
        select_curs.close()

    def closeDB(self):
        self.conn.close()



if __name__ == '__main__':
    db = MySQLSet()
    rows2 = db.insertGPS('A2','35.23178866','129.0828611','2018-08-21 16:07:33')
    rows = db.selectTotalGPS()
    print(rows)
    db.closeDB()
