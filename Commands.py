from CatchSTDOut import CatchSTDOut

class BaseCommands(object):
	def __init__(self, authfile):
		self.authorised = set((name.strip() for name in authfile.read().split('\n') if name))
		self.authfile = authfile
		self.sandbox_globals = {}
		self.sandbox_locals = {'the_answer':42}
	
	def parse_message(self, message, bot):
		"return (function, args) if it's a command where function(args) carries out the command"
		for key in self.commandlist:
			if message.Body.startswith(key):
				if message.Sender.Handle not in self.authorised: 
					self.deny(message)
					return False
				else:
					return (self.commandlist[key],  (message,bot))
	def deny(self, message):
		message.Chat.SendMessage("{} ({}) not authorised".format(message.Sender.FullName, message.Sender.Handle))
	def write_auth(self):
		print 'saving to authfile'
		self.authfile.seek(0)
		self.authfile.write("\n".join(self.authorised))
		self.authfile.truncate()

class DefaultCommands(BaseCommands):
	def __init__(self, authfile):
			self.commandlist = {'>':self.run_as_python, '<':self.utils}
			super(DefaultCommands, self).__init__(authfile)

	def run_as_python(self, message, bot):
		out = []
		err = []
		command = message.Body[1:]
		with CatchSTDOut(out, err):
			exec command in self.sandbox_globals, self.sandbox_locals
		response = str(err[0]) if err[0] else " ".join(out)
		message.Chat.SendMessage(response)
	def utils(self, message, bot):
		commandparts = message.Body[1:].split()
		if message.Sender.Handle not in bot.ops:
			deny(message)
			return

		if commandparts[0] == 'auth':
			if commandparts[1] == 'add':
				users = commandparts[2:]
				self.authorised.update(set(users))
				message.Chat.SendMessage("{} authorised".format(', '.join(users)))
			elif commandparts[1] == 'remove':
				users = commandparts[2:]
				self.authorised.difference_update(set(users))
				message.Chat.SendMessage("{} removed".format(', '.join(users)))

			elif commandparts[1] == 'list':
				message.Chat.SendMessage("These people are authorised:\n {}".format(', '.join(self.authorised)))

		elif commandparts[0] == 'threadcount':
			message.Chat.SendMessage(threading.active_count())


if __name__ == '__main__':
	pass
 #TODO: write dummy message and bot objects to test this module with