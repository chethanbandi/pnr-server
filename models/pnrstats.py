import psycopg2

def save(pnr):
   conn = psycopg2.connect("dbname=pnr user=pnr")
   cur = conn.cursor()

   cur.execute("insert into pnr_stats(pnr) values(%s)", (pnr,))
   conn.commit()

   cur.close()
   conn.close()

if __name__ == '__main__':
   save(1234567890)
