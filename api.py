from http.server import *
from urllib.parse import urlparse, parse_qs  
import json
import logging
import sqlite3

class Handler(BaseHTTPRequestHandler):
    
    # creating a function for Get Request
    def do_GET(self):
        (host,port) = self.client_address
        path = self.path
        url = "http://"+host+":"+str(port)+path
        parsed_url = urlparse(url)
        print("url",parsed_url)
        query = parse_qs(parsed_url.query)
        print("query",query)
        response = "{}"

        if "depo_home1" in path and "product_index" in query and len(query)==1 :
            cursor = conn.cursor()
            product_index = query["product_index"][0]
            print("product for product_index=",product_index)
            cursor.execute("select * from depo_home1 where product_index=?",[product_index])
            rows = cursor.fetchall()

            rows_list = []            
            
            for row in rows:
                result_dict = {}
                for key in row.keys():
                    result_dict[key] = row[key]
    #            print ("response",result,result.keys())
#                 row_dict = json.dumps(result_dict)
                rows_list.append(result_dict)

            response = json.dumps(rows_list)
            cursor.close()
        
        if "depo_home1" in path and "title" in query and len(query) == 1:
            cursor = conn.cursor()
            title = query["title"][0]
            print("product for title=",title)
            cursor.execute("select * from depo_home1 where depo_home1.title like ?",('%'+title+'%',))
            rows = cursor.fetchall()

            rows_list = []            
            
            for row in rows:
                result_dict = {}
                for key in row.keys():
                    result_dict[key] = row[key]
    #            print ("response",result,result.keys())
#                 row_dict = json.dumps(result_dict)
                rows_list.append(result_dict)

            response = json.dumps(rows_list)
            cursor.close()

        
        self.send_response(200)
        # Type of file that we are using for creating our
        # web server.
        self.send_header('content-type', 'application/json')
        self.send_header('content-length', str(len(response)))
        self.end_headers()
        self.flush_headers()
        # what we write in this function it gets visible on our
        # web-server
        self.wfile.write(bytes(response,"UTF-8"))
    def log_message(a,b,c,d,e):
        # print("logging",a,b,c,d,e)
        pass



if __name__ == "__main__":   
    try:
        logging.basicConfig( encoding='utf-8', level=logging.CRITICAL)  
        # this is the object which take port 
        # number and the server-name
        # for running the server
        conn = sqlite3.connect('depo-home.db', uri=True)
        conn.row_factory = sqlite3.Row

        # server = ThreadingHTTPServer(('', 5555), Handler)
        server = HTTPServer(('', 5555), Handler)


        
        # this is used for running our 
        # server as long as we wish
        # i.e. forever
        server.serve_forever()
    except KeyboardInterrupt as k:
        if conn:
            conn.close()
        server.server_close()
