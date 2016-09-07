import OSC
import time, threading, os
import win32api
import VirtualKeyStroke

server_listent_port = 3000
client_listent_port = 3001
max_page_number = 30

print '''
===remote_ppt_controller===

input message types: /page_up, /page_down, /home
output message types: /page_number + int
'''

c = None
s = OSC.OSCServer(('localhost', server_listent_port))
print s

VirtualKeyStroke.press('F5')

page_number = 0

def send_page_number_back(source):
    global c
    if c is None:
        c = OSC.OSCClient()
        c.connect((source[0], client_listent_port))
        print c

    msg = OSC.OSCMessage("/page_number")
    msg.append(page_number)
    c.send(msg)

# define a message-handler function for the server to call.
def page_up(addr, tags, data, source):
    VirtualKeyStroke.press('page_up')
    global page_number
    page_number -= 1
    if page_number < 0:
        page_number = 0
    send_page_number_back(source)

def page_down(addr, tags, data, source):
    VirtualKeyStroke.press('page_down')
    global page_number
    page_number += 1
    if page_number > max_page_number - 1:
        page_number = max_page_number - 1
    send_page_number_back(source)

def home(addr, tags, data, source):
    VirtualKeyStroke.press('home')
    global page_number
    page_number = 0
    send_page_number_back(source)

s.addMsgHandler("/page_up", page_up)
s.addMsgHandler("/page_down", page_down)
s.addMsgHandler("/homepage", home)
s.addDefaultHandlers()

print "\nStarting OSCServer. Use ctrl-C to quit."
st = threading.Thread(target=s.serve_forever)
st.start()

try:
    while True:
        time.sleep(30)

except KeyboardInterrupt:
    print "\nClosing OSCServer."
    s.close()
    print "Waiting for Server-thread to finish"
    st.join()
    print "Closing OSCClient"
    c.close()
    print "Done"
    
sys.exit(0)