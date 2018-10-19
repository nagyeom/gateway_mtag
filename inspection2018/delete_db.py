import DB_func

if __name__ == '__main__':
    db = DB_func.MySQLSet()
    db.deleteGPS()
    db.closeDB()