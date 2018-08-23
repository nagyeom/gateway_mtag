import pymysql

class MySQLSet():
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='123456', db='mysql', charset='utf8')
        self.select_curs = self.conn.cursor(pymysql.cursors.DictCursor)
        #self.insert_curs = self.conn.cursor()

    def selectTotalGPS(self):
        sql = "select * from gps_log"
        self.select_curs.execute(sql)
        rows = self.select_curs.fetchall()

        #self.conn.close()
        return rows

    def insertGPS(self,tag_id,lat,lon,time):
        sql = "insert into gps_log(tag_id,lat,lon,time) values (%s, %s, %s, %s)"
        self.select_curs.execute(sql,(tag_id,lat,lon,time))
        self.conn.commit()
        #self.conn.close()

    def closeDB(self):
        self.conn.close()



if __name__ == '__main__':
    db = MySQLSet()
    rows2 = db.insertGPS('A2','35.23178866','129.0828611','2018-08-21 16:07:33')
    rows = db.selectTotalGPS()
    print(rows)
    db.closeDB()
