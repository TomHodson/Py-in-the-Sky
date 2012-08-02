import Skype4Py
import math
import time
from CatchSTDOut import CatchSTDOut
sandbox_globals = {}
sandbox_locals = {'the_answer':42}
messagequeue = set()
debug = False
allowed = set((name.strip() for name in open("./allowed").read().split('\n') if name))
if debug: print "allowed: ", allowed

class BotSkypeinterface(object):
    def __init__(self):
        self.skype = Skype4Py.Skype(Transport='x11')
        if not self.skype.Client.IsRunning:
            print 'You need to start skype'
            exit()
        self.skype.FriendlyName = 'Py-in-the-Sky'
        self.skype.RegisterEventHandler('MessageStatus', self.getmessage)
        self.skype.Attach()
        print "attached!" if self.skype.AttachmentStatus == 0 else "Couldn't attach to skype"
        
    def getmessage(self, message, status):
        global messagequeue; global allowed
        if self.iscommand(message):
            messagequeue.add((self.iscommand(message),message,hash(self)))
    def iscommand(self, message):
        "return the sanitised version of the text if it's a command"
        return message.Body[1:] if message.Body.startswith('>') else None
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        self.skype.UnregisterEventHandler('MessageStatus', self.getmessage)
        del self.skype
        
with BotSkypeinterface() as Bot:
    while True:
        if messagequeue:
            message = messagequeue.pop()
            command = message[0]
            if  message[1].Sender.Handle in allowed:
                out = []
                err = []
                sandbox_locals['message'] = message[1]
                with CatchSTDOut(out, err):
                    exec command in sandbox_globals, sandbox_locals
                response = str(err[0]) if err[0] else " ".join(out)
                if debug: response = response + "\nInstanceId:" + str(message[2])
                message[1].Chat.SendMessage(response)
            else:
                message[1].Chat.SendMessage("{} ({}) not authorised".format(message[1].Sender.FullName,
                                                                            message[1].Sender.Handle
                                                                            ))
        else:
            #print "I'm alive"
            time.sleep(0.5)
        