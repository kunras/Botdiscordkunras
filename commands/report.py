import utils.find
from commandsample import C
from utils.answers import embed as E
import asyncio

class ReportSystem(C):

	async def on_loaded(self):
		try: self.bot.sql("CREATE TABLE guilds (id INTEGER NOT NULL PRIMARY KEY UNIQUE)")
		except: pass
		try: self.bot.sql("ALTER TABLE guilds ADD ReportSystem_Channel INTEGER DEFAULT 0")
		except: pass
		
	def get(self, guild):
		try: self.bot.sql("INSERT INTO guilds (id) VALUES (%s)" %(guild.id))
		except: pass
		return self.bot.sql("SELECT ReportSystem_Channel FROM guilds WHERE ID = %s" %(guild.id))[0][0]
		
	def set(self, guild, channel):
		try: self.bot.sql("INSERT INTO guilds (id) VALUES (%s)" %(guild.id))
		except: pass
		if channel != None:
			self.bot.sql("UPDATE guilds SET ReportSystem_Channel = '%s' WHERE id = %s" %(channel.id, guild.id))
		else:
			self.bot.sql("UPDATE guilds SET ReportSystem_Channel = '0' WHERE id = %s" %(guild.id))
		
	async def cmd_report(self, message, *args):
		"""Report someone in this server.
		
{0}report <@user>"""
		channel_id = self.get(message.guild)
		channel = self.bot.get_channel(channel_id)
		if channel != None:
			if len(args) > 0:
				user = utils.find.user(args[0], guild=message.guild)
				if user != None:
					await channel.send(None, embed=E(message.author, "**{0} reported {1}.\n→ Reason:** ```fix\n{2}\n```".format(message.author.mention, user.mention, " ".join(args[1:]))))
					await message.add_reaction("✅")
				else:
					_message = await message.channel.send(None, embed=E(message.author, "Unknown user."))
					await asyncio.sleep(5)
					await _message.delete()
			else:
				_message = await message.channel.send(None, embed=E(message.author, "You must specify a user."))
				await asyncio.sleep(5)
				await _message.delete()
		else:
			_message = await message.channel.send(None, embed=E(message.author, "No channel defined for report system."))
			await asyncio.sleep(5)
			await _message.delete()
		
	async def cmd_setreportchannel(self, message, *args):
		"""Set the report channel for the reports
		
{0}setreportchannel <off/@mention>"""
		if message.author.guild_permissions.manage_guild or message.author.id == self.bot.user.id:
			if len(args) > 0:
				channel_id = 0
				channel_id_str = ""
				for car in args[0]:
					if car.isdigit():
						channel_id_str += car
				try: channel_id = int(channel_id_str)
				except ValueError: pass
				channel = self.bot.get_channel(channel_id)
				self.set(message.guild, channel)
				await message.add_reaction("✅")
			elif len(args) == 0:
				await message.channel.send(None, embed=E(message.author, "You must specify a channel."))
		else:
			_message = await message.channel.send(None, embed=E(message.author, "**You do not have the permission to execute that command!**"))
			await asyncio.sleep(5)
			await _message.delete()
	
def load(client):
	client.add_command(ReportSystem(client))