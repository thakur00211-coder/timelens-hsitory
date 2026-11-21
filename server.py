"""TimeLens educational prototype. Python 3.10+, no third-party dependencies."""
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse,parse_qs
import sqlite3,json,os,mimetypes
ROOT=Path(__file__).resolve().parent
DB=ROOT/'timelens.db'
def connect():
    c=sqlite3.connect(DB);c.row_factory=sqlite3.Row;return c
def init():
    with connect() as c:
        c.executescript("""CREATE TABLE IF NOT EXISTS places(id INTEGER PRIMARY KEY,name TEXT NOT NULL,region TEXT NOT NULL,description TEXT NOT NULL,lat REAL,lon REAL);CREATE TABLE IF NOT EXISTS records(id INTEGER PRIMARY KEY,place_id INTEGER NOT NULL REFERENCES places(id),year INTEGER NOT NULL,title TEXT NOT NULL,description TEXT NOT NULL,image TEXT NOT NULL,source TEXT NOT NULL,kind TEXT NOT NULL);""")
        if not c.execute('SELECT COUNT(*) FROM places').fetchone()[0]:
            c.execute('INSERT INTO places VALUES(1,?,?,?,?,?)',('Heritage Square','Illustrative location','A fictional public square created to demonstrate TimeLens. The dates and scenes are illustrative, not historical claims.',30.9,75.85))
            c.executemany('INSERT INTO records VALUES(?,?,?,?,?,?,?,?)',[(1,1,1920,'Market square, early era','Illustrative market stalls, stone roads and early streetscape.','/static/assets/scene-1920.svg','Original illustrative artwork','illustration'),(2,1,1960,'Growing town center','Illustrative mid-century streetscape with a bus and shopfronts.','/static/assets/scene-1960.svg','Original illustrative artwork','illustration'),(3,1,2020,'Contemporary square','Illustrative contemporary plaza with trees and modern buildings.','/static/assets/scene-2020.svg','Original illustrative artwork','illustration')])
class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT),**kw)
    def send_json(self,obj,status=200):
        data=json.dumps(obj).encode();self.send_response(status);self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Content-Length',str(len(data)));self.send_header('Access-Control-Allow-Origin','*');self.end_headers();self.wfile.write(data)
    def do_GET(self):
        u=urlparse(self.path)
        if u.path=='/api/health':return self.send_json({'status':'ok','database':'sqlite'})
        if u.path=='/api/places':
            with connect() as c:return self.send_json([dict(r) for r in c.execute('SELECT * FROM places ORDER BY name')])
        if u.path=='/api/records':
            raw=parse_qs(u.query).get('place_id',['1'])[0]
            try: pid=int(raw)
            except ValueError:return self.send_json({'error':'Invalid place_id'},400)
            with connect() as c:return self.send_json([dict(r) for r in c.execute('SELECT * FROM records WHERE place_id=? ORDER BY year',(pid,))])
        if u.path=='/':self.path='/index.html'
        return super().do_GET()
    def do_POST(self):
        if urlparse(self.path).path!='/api/records':return self.send_json({'error':'Not found'},404)
        try:
            n=int(self.headers.get('Content-Length','0'))
            if n<1 or n>10000:return self.send_json({'error':'Invalid body length'},400)
            d=json.loads(self.rfile.read(n));year=int(d.get('year',0));pid=int(d.get('place_id',1))
            title=str(d.get('title','')).strip();description=str(d.get('description','')).strip();source=str(d.get('source','')).strip()
            if not (1000<=year<=2100 and 2<=len(title)<=120 and 5<=len(description)<=1000 and 2<=len(source)<=180):raise ValueError('Check year, title, description and source')
            # Only bundled images may be referenced; no arbitrary URLs or file paths.
            image=str(d.get('image',''))
            if image not in ['/static/assets/scene-1920.svg','/static/assets/scene-1960.svg','/static/assets/scene-2020.svg']:raise ValueError('Choose a bundled illustration')
            with connect() as c:
                if not c.execute('SELECT 1 FROM places WHERE id=?',(pid,)).fetchone():raise ValueError('Unknown place')
                cur=c.execute('INSERT INTO records(place_id,year,title,description,image,source,kind) VALUES(?,?,?,?,?,?,?)',(pid,year,title,description,image,source,'user-submitted'))
                return self.send_json({'id':cur.lastrowid,'message':'Record saved'},201)
        except (ValueError,TypeError,json.JSONDecodeError) as e:return self.send_json({'error':str(e)},400)
if __name__=='__main__':
    init();port=int(os.getenv('PORT','8000'));print(f'TimeLens running at http://localhost:{port}',flush=True);ThreadingHTTPServer(('127.0.0.1',port),Handler).serve_forever()
