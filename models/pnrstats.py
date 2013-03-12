import psycopg2

class PNRStats:
   conn = None

   def __init__(self):
      self.conn = None

   def open(self):
      self.conn = psycopg2.connect("dbname=pnr user=pnr")

   def close(self):
      self.conn.close()

   def save(self, pnr, userAgent, remoteAddress):
      cur = self.conn.cursor()
      cur.execute("insert into pnr_stats(pnr, user_agent, remote_addr) values(%s,%s,%s) returning id", (pnr, userAgent, remoteAddress))
      pnr_stats_id = cur.fetchone()[0]
      self.conn.commit()
      cur.close()

      return pnr_stats_id

   def update(self, pnr_stats_id, code, message):
      cur = self.conn.cursor()
      cur.execute("update pnr_stats set status_code = %s, status_message = %s where id = %s", (code, message, pnr_stats_id))
      self.conn.commit()
      cur.close()

if __name__ == '__main__':
   stats = PNRStats()
   stats.open()
   pnr_stats_id = stats.save(1234567890, "abcd", "127.0.0.1")
   print pnr_stats_id
   stats.update(pnr_stats_id, 0, "Success")
   stats.close()

