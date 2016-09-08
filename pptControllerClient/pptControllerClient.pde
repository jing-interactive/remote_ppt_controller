// simulator
// press 1 -> /page_up
// press 2 -> /page_down
// press 3 -> /homepage

import oscP5.*;
import netP5.*;

OscP5 oscP5;
NetAddress myRemoteLocation;

int page_number = 0;

void setup() {
  size(400, 400);
  frameRate(25);
  /* start oscP5, listening for incoming messages at port 12000 */
  oscP5 = new OscP5(this, 3001);

  myRemoteLocation = new NetAddress("192.168.232.1", 3000);
}

void keyReleased() {
  OscMessage m = null;

  if (key == '1') {
    m = new OscMessage("/page_up");
  } else if (key == '2') {
    m = new OscMessage("/page_down");
  } else if (key == '3') {
    m = new OscMessage("/homepage");
  }
  if (m != null) {
    oscP5.send(m, myRemoteLocation);
  }
}

void draw() {
  background(0);

  String info = 
    "press 1 -> /page_up\n" + 
    "press 2 -> /page_down\n" + 
    "press 3 -> /homepage\n\n\n" +
    "/page_number " + page_number;

  text(info, 100, 50);
}

/* incoming osc message are forwarded to the oscEvent method. */
void oscEvent(OscMessage theOscMessage) {
  /* print the address pattern and the typetag of the received OscMessage */
  print("### received an osc message.");
  print(" addrpattern: " + theOscMessage.addrPattern());
  println(" typetag: " + theOscMessage.typetag());

  if (theOscMessage.addrPattern().equals("/page_number")) {
    page_number = theOscMessage.get(0).intValue();
  }
}