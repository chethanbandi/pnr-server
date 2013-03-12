import psycopg2

def save(pnr):
   conn = psycopg2.connect("dbname=apps user=apps password=cbandiapps")
   cur = conn.cursor()

   cur.execute("insert into pnr_stats(pnr) values(%s)", (pnr,))
   conn.commit()

   cur.close()
   conn.close()

