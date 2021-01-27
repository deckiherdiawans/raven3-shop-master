from helpers.database import Database

def executeQuery(sp):
    db = Database()
    conn = db.koneksi()
    cursor = conn.cursor()
    cursor.execute("SET NOCOUNT ON")

    if not conn:
        return False
    else:    
        sql = "exec %s" % sp
        cursor.execute(sql)
        data = cursor.fetchall()

        if len(data) > 0:
            return data
        else:
            return {}
