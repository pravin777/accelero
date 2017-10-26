from SF_9DOF import IMU
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
#This class will handles any incoming request from
#the browser
import mraa
import sys
import time
#i2c = mraa.I2c(1)
#i2c.address(0x15)
imu = IMU()
imu.initialize()
imu.enable_accel()
imu.accel_range("2G")
PORT_NUMBER = 8000
class myHandler(BaseHTTPRequestHandler):

	#Handler for the GET requests
    def do_GET(self):

        if self.path == '/val':
            self.do_val()
        else:
            self.do_index()
        return

    def do_index(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        if (len(self.path) == 1):
            self.path = "/ed.html"
        f = open(self.path[1:])
        # Send the html message
        self.wfile.write(f.read())
        f.close()
        return

    def do_val(self):
        global data
        global data1
        global data2
        imu.read_accel()
        data = str(imu.ax)
        data1 = str(imu.ay)
        data2 = str(imu.az)
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        # Send the html message
        #valx=float(x.read())
        #valy=float(y.read())
        #valz=float(z.read())
        #print ((valx-331.5)/68*9.8)
        #print ((valx-331.5)/6*9.8)
        #print ((valy-329.5)/68.5*9.8)
        #print ((valy-329.5)/6*9.8)
        #print ((valz-340)/68*9.8)
        #print ((valz-340)/6*9.8)
        #time.sleep(1
        #if data == 3:
        self.wfile.write(data)
        self.wfile.write("<br></br>")
        self.wfile.write(data1)
        self.wfile.write("<br></br>")
        self.wfile.write(data2)
        #elif data == 2:
            #self.wfile.write("Motor is off...")
        #else:
           # self.wfile.write("ALERT: motor might be overloaded")

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER

	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()
