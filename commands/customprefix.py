from commandsample import C
from utils.answers import embed as E
import asyncio

class CustomPrefix(C):

	async def on_loaded(self):
		self.default = ""
		try: self.bot.sql("CREATE TABLE guilds (id INTEGER NOT NULL UNIQUE PRIMARY KEY)")
		except: pass
		try: self.bot.sql("ALTER TABLE guilds ADD CustomPrefix_prefix varchar(20) DEFAULT ''")
		except: pass
		
	def get(self, guild):
		if guild != None:
			try: self.bot.sql("INSERT INTO guilds (id) VALUES (%s)" %(guild.id))
			except: pass
			return self.bot.sql("SELECT CustomPrefix_prefix FROM guilds WHERE id = %s" %(guild.id))[0][0]
		else:
			return ""
		
	def set(self, guild, value):
		self.get(guild)
		self.bot.sql("UPDATE guilds SET CustomPrefix_prefix = '%s' WHERE id = %s" %(value, guild.id))
		
	async def cmd_setprefix(self, message, *args):
		"""Edit the prefix for the server."""
		if self.bot.user.bot:
			if message.author.guild_permissions.manage_guild:
				if len(args) > 0:
					value = " ".join(args)
					value = value.replace("{space}", " ") # Replace {space} by a space
					if value in ["off","disable","f4ck","stop","nope"]:
						value = ""
					self.set(message.guild, value)
					await message.add_reaction("✅")
				else:
					_message = await message.channel.send(None, embed=E(message.author, "**Actual prefix** : ``%s``\nDo %ssetprefix [new] to edit the prefix" %(get(message.guild), self.bot.config["prefixs"][0])))
					await asyncio.sleep(5)
					await _message.delete()
			else:
				_message = await message.channel.send(None, embed=E(message.author, "You are not allowed to use that command."))
				await asyncio.sleep(5)
				await _message.delete()
		else:
			_message = await message.channel.send(None, embed=E(message.author, "Selfbots can't do that."))
			await asyncio.sleep(5)
			await message.delete()
			await _message.delete()
			
	async def on_message(self, _message):
		prefix = self.get(_message.guild)
		if prefix != "":
			await self.bot.fire_command(_message, specific_prefix=prefix)
			
	async def on_message_edit(self, before, after):
		prefix = self.get(after.guild)
		if prefix != "":
			await self.bot.fire_command(after, specific_prefix=prefix)
				
def load(client):
	client.add_command(
			CustomPrefix(client)
		)