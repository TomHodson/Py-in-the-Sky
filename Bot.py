import Skype4Py
debug = False
import Queue
import threading

messagequeue = Queue.Queue()

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
        self.ops = set((name.strip() for name in open('ops').read().split('\n') if name))

        print "attached!" if self.skype.AttachmentStatus == 0 else "Couldn't attach to skype"
        
    def getmessage(self, message, status):
        "this method gets attached to skype and called whenever a message comes in"
        global messagequeue;
        parsedmessage = self.commands.parse_message(message, self)
        if parsedmessage: #parsed message returns false if it's not a command
            messagequeue.put(parsedmessage)

    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        self.skype.UnregisterEventHandler('MessageStatus', self.getmessage)
        self.commands.write_auth()
        del self.skype

class Worker(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self):
        while True:
            function, args = self.queue.get()
            function(*args)
            self.queue.task_done()


if __name__ == '__main__':
    from Commands import DefaultCommands as Commands
    import time

    with  open('./allowed', 'r+') as auth:
        with BotSkypeinterface(Commands(auth)) as Bot:
            workers = [Worker(messagequeue) for _ in range(3)]
            for t in workers:
                t.setDaemon(True)
                t.start()
            while True:
                time.sleep(10)

                