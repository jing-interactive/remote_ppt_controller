import OSC
import time, threading, os
import win32api
import VirtualKeyStroke

print "start remote_ppt_controller"

VirtualKeyStroke.press('F5')

s = OSC.OSCServer(('127.0.0.1', 7777))
print s

# define a message-handler function for the server to call.
def page_up(addr, tags, data, source):
    VirtualKeyStroke.press('page_up')

def page_down(addr, tags, data, source):
    VirtualKeyStroke.press('page_down')

def home(addr, tags, data, source):
    VirtualKeyStroke.press('home')

s.addMsgHandler("/page_up", page_up)
s.addMsgHandler("/page_down", page_down)
s.addMsgHandler("/homepage", home)

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