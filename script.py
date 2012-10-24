import subprocess 
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

class RequestHandler(BaseHTTPRequestHandler):
    def _writeheaders(self):
        self.send_response(200) 
        self.send_header('Content-type', 'video/ogg')
        self.end_headers()

    def do_HEAD(self):
        self._writeheaders()

    def do_GET(self):
        self._writeheaders()

        DataChunkSize = 10000

        command = 'gst-launch-0.10 v4l2src ! video/x-raw-yuv,width=320,height=240,framerate=4/1 ! theoraenc ! oggmux ! filesink location=/dev/stdout'
        print("running command: %s" % (command, ))
        p = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=-1, shell=True)

        print("starting polling loop.")
        while(p.poll() is None):
            print "looping... "
            stdoutdata = p.stdout.read(DataChunkSize)
            self.wfile.write(stdoutdata)

        print("Done Looping")

        print("dumping last data, if any")
        stdoutdata = p.stdout.read(DataChunkSize)
        self.wfile.write(stdoutdata)

if __name__ == '__main__':
    serveraddr = ('', 8765) 
    srvr = HTTPServer(serveraddr, RequestHandler)
    srvr.serve_forever()
