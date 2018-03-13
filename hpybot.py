import discord, asyncio, json, os, aiohttp, random, textwrap, io, importlib, sys, sqlite3, inspect
from contextlib import redirect_stdout
from discord import Webhook, AsyncWebhookAdapter

class Context(discord.abc.Messageable):

	"""This class is based on 
	https://github.com/Rapptz/discord.py/blob/rewrite/discord/ext/commands/context.py
	"""

	def __init__(self, **kwargs):
	
		#
		self.client = kwargs.get('client')
		self.bot = self.client
		
		#
		self.message = kwargs.get('message')
		self.prefix = kwargs.get('prefix')
		self.command = kwargs.get('command')
		self.function = kwargs.get('function')
		self.args = kwargs.get('args', [])
		self._state = self.message._state
		
		#
		self._get_channel = lambda: self.message.channel
		self._get_guild = lambda: self.message.guild
		self.channel = self.message.channel
		self.guild = self.message.guild
		self.me = self.message.guild.me if self.message.guild != None else self.client.user
		
		# Can't be different than the default value for the moment
		self.view = None
		self.invoked_with = None
		self.invoked_subcommand = None
		self.subcommand_passed = None
		self.command_failed = False
		
	def _reply(self, content, tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None):
		return self.client.loop.create_task(self.send(content, tts=tts, embed=embed, file=file, files=files, delete_after=delete_after, nonce=nonce))
	async def reply(self, content, tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None):
		return await self.send(content, tts=tts, embed=embed, file=file, files=files, delete_after=delete_after, nonce=nonce)
	async def send(self, content, tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None):
		_return = None
		if nonce == None:
			nonce = random.randint(400000000000000000, 500000000000000000)
		try:
			_return = await self.message.channel.send(content, tts=tts, embed=embed, file=file, files=files, delete_after=delete_after, nonce=nonce)
		except:
			try:
				_return = await self.message.author.send(content, tts=tts, embed=embed, file=file, files=files, delete_after=delete_after, nonce=nonce)
			except:
				pass
		return _return
		
	async def _get_channel(self):
		return self.channel
		
	async def invoke(self, *args, **kwargs):
		print('→ invoke is not supported...')
		
	async def reinvoke(self, *args, **kwargs):
		print('→ invoke is not supported...')

class DiscordBot(discord.Client):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		class Table(dict):
			pass
		self.discord = discord
		self.loaded = False
		self.config = configuration # BOT CONFIGURATION (ONLY FOR BOT TOKEN 👀)
		self.db = None # DATABASE
		self._ = Table()
		self._.files = []
		self._.commands = []
		self._G = Table()
		
	def sql(self, statement, *args, **kwargs):
		if self.db == None:
			self.db = sqlite3.connect(self.config.get('database', "databases/hpybot.db"))
		cursor = self.db.cursor()
		cursor.execute(statement, *args)
		self.db.commit()
		liste = cursor.fetchall()
		if len(liste) != 0:
			return liste
		
	def add_cog(self, objet):
		self.add_command(objet)
	def add_command(self, objet):
		self._.commands.append(objet)
		self._.files.append(inspect.getmodule(object))
		try:
			if hasattr(objet, "on_loaded"):
				self.loop.create_task(objet.on_loaded())
		except Exception as e:
			self.log('[{}] {}: {}'.format(objet.__class__.__name__, type(e).__name__, e))
		return True
		
	def load_file(self, objet):
		if objet.__class__ == str:
			command = importlib.import_module("commands."+objet)
			if not hasattr(command, 'load'):
				if not hasattr(command, 'setup'):
					self.log("Missing load() function for "+command.__name__[9:]+".py")
					del command
					del sys.modules["commands."+objet]
				else:
					command.setup(self)
					self.log("[EXPERIMENTAL] Loaded cog {0}".format(command.__name__[9:]+".py"))
			else:
				command.load(self)
				self.log("Loaded file {0}".format(command.__name__[9:]+".py"))
		else:
			objet.load(self)
			self.log("Loaded file {0}".format(objet.__name__[9:]+".py"))
		return objet
			
	def unload_file(self, object):
		if object.__class__ == str:
			for command in self._.files[:]:
				if command != None:
					command_name = command.__name__.split(".")[1]
					if object.lower() in command_name.lower():
						for _class in self._.commands:
							module = inspect.getmodule(_class)
							if module != None:
								if module.__name__ == command.__name__:
									del self._.commands[self._.commands.index(_class)]
									del self._.files[self._.files.index(command)]
							_class = None
						if sys.modules.get(command.__name__) != None:
							del sys.modules[command.__name__]
						del command
						self.log("Unloaded file %s.py" %(command_name))

	def log(self, message, me=False):
		if me == True:
			texte = "* {0} {1}".format(str(self.user), str(message))
		else:
			texte = "[{0}] {1}".format(str(self.user), str(message))
		print(texte)
		return True
		
	async def on_connect(self):
		self.log("is now logged in Discord.", me=True)
		self.log("| ID: {0.id}".format(self.user), me=True)
		
		self.on_loaded_bot()
		
	def on_loaded_bot(self):
		if self.loaded == False: # Premier démarrage ?
			self.loaded = True # Premier démarrage accompli.
		
			for file in os.listdir("commands"):
				if file.endswith('.py'):
					try:
						self.load_file(file[:-3])
					except Exception as e:
						self.unload_file(file[:-3])
						self.log('La ou le groupe de commande(s) {} n\'a pas pu être chargé.'.format(file))
						self.log('→ {}: {}'.format(type(e).__name__, e))

	async def on_ready(self):	
		for command in self._.commands:
			if hasattr(command, "on_ready"):
				self.loop.create_task(command.on_ready())
				break
		
	async def on_guild_join(self, guild):
		self.log("joined the guild {0} owned by {1}".format(
			str(guild.name),
			str(guild.owner)
		), me=True)
		
		for command in self._.commands:
			if hasattr(command, "on_guild_join"):
				self.loop.create_task(command.on_guild_join(guild))
		
	async def on_guild_remove(self, guild):
		self.log("leaved the guild {0} owned by {1}".format(
			str(guild.name),
			str(guild.owner)
		), me=True)
		
		for command in self._.commands:
			if hasattr(command, "on_guild_remove"):
				self.loop.create_task(command.on_guild_remove(guild))
			
	async def on_guild_update(self, before, after):
		for command in self._.commands:
			if hasattr(command, "on_guild_update"):
				self.loop.create_task(command.on_guild_update(before, after))
		
	async def on_member_join(self, member):
		for command in self._.commands:
			if hasattr(command, "on_member_join"):
				self.loop.create_task(command.on_member_join(member))
		
	async def on_member_remove(self, member):
		for command in self._.commands:
			if hasattr(command, "on_member_remove"):
				self.loop.create_task(command.on_member_remove(member))
			
	async def on_command(self, _message, _command, *args, **kwargs):
		for command in self._.commands:
			if hasattr(command, "cmd_"+_command.lower()):
				function = getattr(command, "cmd_"+_command.lower())
				self.loop.create_task(function(_message, *args))
			if hasattr(command, "ctx_"+_command.lower()):
				function = getattr(command, "ctx_"+_command.lower())
				function_kwargs = kwargs
				function_kwargs['command'] = _command.lower()
				function_kwargs['function'] = function
				self.loop.create_task(function(Context(**function_kwargs), *args))
				
		for command in self._.commands:
			if hasattr(command, "on_command"):
				self.loop.create_task(command.on_command(_message, _command, *args))
		
	async def fire_command(self, _message, specific_prefix=None):
		command = None
		args = None
		_kwargs = {}
		def check(m, prefix):
			words = m.content[len(prefix):].split(" ")
			if len(words) != 0:		
				command = words[0]			
				if len(words) > 1:			
					args = words[1:]			
				else:			
					args = []
			if command != None:
				_kwargs['prefix'] = prefix
				_kwargs['message'] = m
				_kwargs['args'] = args
				_kwargs['client'] = self
			return command, args
		if specific_prefix == None:
			for prefix in self.config["prefixs"]:
				if _message.content.startswith(prefix):
					command, args = check(_message, prefix)
					break
		else:
			if _message.content.startswith(specific_prefix):
				command, args = check(_message, specific_prefix)
		
		if command != None:
			await self.on_command(_message, command, *args, **_kwargs)
			
	async def on_message(self, message):
		for command in self._.commands:
			if hasattr(command, "on_message"):
				self.loop.create_task(command.on_message(message))
			
		if self.user.bot:
			if not message.author.bot:
				await self.fire_command(message)
		else:
			if self.user.id == message.author.id:
				await self.fire_command(message)
					
	async def on_message_edit(self, before, after):
		for command in self._.commands:
			if hasattr(command, "on_message_edit"):
				self.loop.create_task(command.on_message_edit(before, after))
			
		await self.fire_command(after)
			
	async def on_message_delete(self, message):
		for command in self._.commands:
			if hasattr(command, "on_message_delete"):
				self.loop.create_task(command.on_message_delete(message))
			
	async def on_guild_channel_pins_update(self, channel, last_pin):
		for command in self._.commands:
			if hasattr(command, "on_guild_channel_pins_update"):
				self.loop.create_task(command.on_guild_channel_pins_update(channel, last_pin))
		
	async def on_member_update(self, before, after):		
		for command in self._.commands:
			if hasattr(command, "on_member_update"):
				self.loop.create_task(command.on_member_update(before, after))
			
# Chargement et vérification de la configuration
with open("config.json", "r", encoding="utf8") as content:
	configuration = json.load(content)
if configuration["token"] in ["YOUR_TOKEN_HERE", "token", "", None]:
	print("[•] /!\ Please edit the config.json")
	while 1:
		input("")
			
# Démarrage du bot
print("""
	The owner of this bot is Danny Hpy#9766. (215634007306534912)
""")
client = DiscordBot()
client.run(configuration["process.env.TOKEN"], bot=not configuration["selfbot"])
