import Skype4Py
debug = False

messagequeue = set()

class BotSkypeinterface(object):
    def __init__(self, commands):
        self.skype = Skype4Py.Skype(Transport='x11')
        if not self.skype.Client.IsRunning:
            print 'You need to start skype'
            exit()

        self.skype.FriendlyName = 'Py-in-the-Sky'
        self.skype.RegisterEventHandler('MessageStatus', self.getmessage)
        self.skype.Attach()
        self.commands = commands
        self.owner = 'tom.c.hodson'

        print "attached!" if self.skype.AttachmentStatus == 0 else "Couldn't attach to skype"
        
    def getmessage(self, message, status):
        "this method gets attached to skype and called whenever a message comes in"
        global messagequeue;
        parsedmessage = self.commands.parse_message(message, self)
        if parsedmessage: #parsed message returns false if it's not a command
            messagequeue.add(parsedmessage)

    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        self.skype.UnregisterEventHandler('MessageStatus', self.getmessage)
        self.commands.write_auth()
        del self.skype

if __name__ == '__main__':
    from Commands import DefaultCommands as Commands
    import time

    with  open('./allowed', 'r+') as auth:
        with BotSkypeinterface(Commands(auth)) as Bot:
            while True:
                if messagequeue:
                    function, args = messagequeue.pop()
                    function(*args)
                else:
                    if debug: print "I'm still alive"
                    time.sleep(0.5)
                