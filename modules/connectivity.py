from modules.imagezmq import imagezmq


class Connectivity(object):

    def __init__(self, serverIP):
        self._IP=serverIP
        self.setSender(self._IP)
        self._receiver = imagezmq.ImageHub()

    def sendFrame(self, frame):
        isreceived=self._sender.send_image("frame sent", frame)
        return(isreceived)

    def recieveFrame(self):
        (msg,frame)=self._receiver.recv_image()
        self._receiver.send_reply(b'frame received')
        return frame

    @property
    def getIP(self):
        return self._IP

    def setIP(self, IP):
        self._IP = IP

    def setSender(self,IP):
        self._sender = imagezmq.ImageSender(connect_to="tcp://{}:5555".format(IP))



