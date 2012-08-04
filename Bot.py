#!/usr/bin/env python
import Skype4Py
debug = False
import threading
import time

class BotSkypeinterface(object):
    def __init__(self, commands, threading):
        self.skype = Skype4Py.Skype(Transport='x11')
        if not self.skype.Client.IsRunning:
            print 'You need to start skype'
            exit()
        self.threading = threading
        self.skype.FriendlyName = 'Py-in-the-Sky'
        self.skype.RegisterEventHandler('MessageStatus', self.getmessage)
        self.skype.Attach()
        self.commands = commands
        self.ops = set((name.strip() for name in open('ops').read().split('\n') if name))

        print "attached!" if self.skype.AttachmentStatus == 0 else "Couldn't attach to skype"
        
    def getmessage(self, message, status):
        "this method gets attached to skype and called whenever a message comes in"
        parsedmessage = self.commands.parse_message(message, self)
        snippet = message.Body[1:21]
        if parsedmessage: #parsed message returns false if it's not a command
            function, args = parsedmessage
            t = threading.Thread(target=function, args=args, name=snippet)
            t.start_time = time.time()
            t.setDaemon(True)
            t.start()

    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        self.skype.UnregisterEventHandler('MessageStatus', self.getmessage)
        self.commands.write_auth()
        del self.skype

if __name__ == '__main__':
    from Commands import DefaultCommands as Commands

    with  open('./allowed', 'r+') as auth:
        with BotSkypeinterface(Commands(auth), threading) as Bot:
            while True: 
                time.sleep(10)

                