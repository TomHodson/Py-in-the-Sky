import Skype4Py
import math
import time
from CatchSTDout import CatchSTDOut
sandbox_globals = {}
sandbox_locals = {'the_answer':42}
messagequeue = set()

class BotSkypeinterface(object):
    def __init__(self):
        self.skype = Skype4Py.Skype(Transport='x11')
        if not self.skype.Client.IsRunning:
            self.skype.Client.Start()
        self.skype.FriendlyName = 'Skype4Py_Example'
        self.skype.RegisterEventHandler('MessageStatus', self.getmessage)
        self.skype.Attach()
        print "attached!" if self.skype.AttachmentStatus == 0 else "hmm some error"
        
    def getmessage(self, message, status):
        global messagequeue
        if self.iscommand(message):
            if (not messagequeue) or message in messagequeue:
                messagequeue.add(message)
            else: print "dupe"
    def iscommand(self, message):
        return message.Body.startswith('>')
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        self.skype.UnregisterEventHandler('MessageStatus', self.getmessage)
        del self.skype
        
with BotSkypeinterface() as Bot:
    while True:
        if messagequeue:
            message = messagequeue.pop()
            command = message.Body[1:]
            if  command != '>exit()':
                out = []
                err = []
                def send(text):
                    text = str(text)
                    if text and text != '\n' and text != "(None, None, None)":
                        message.Chat.SendMessage(text)
                with CatchSTDOut(out, err, send):
                    exec command in sandbox_globals, sandbox_locals
        else:
            #print "I'm alive"
            time.sleep(0.5)
        