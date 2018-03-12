import utils.find
from commandsample import C
from utils.answers import embed as E
import asyncio

class AutoRole(C):

	async def on_loaded(self): # Dès que le fichier est chargé...
		try: self.bot.sql("CREATE TABLE guilds (id INTEGER NOT NULL PRIMARY KEY UNIQUE)") # Créer la table ``guilds``
		except: pass
		try: self.bot.sql("ALTER TABLE guilds ADD AutoRole_role INTEGER DEFAULT 0") # Créer la colonne ``AutoRole_role``
		except: pass
		
	def get(self, guild):
		try: self.bot.sql("INSERT INTO guilds (id) VALUES (%s)" %(guild.id))
		except: pass
		return self.bot.sql("SELECT AutoRole_role FROM guilds WHERE ID = %s" %(guild.id))[0][0]
		
	def set(self, guild, role):
		try: self.bot.sql("INSERT INTO guilds (id) VALUES (%s)" %(guild.id))
		except: pass
		if role != None:
			self.bot.sql("UPDATE guilds SET AutoRole_role = '%s' WHERE id = %s" %(role.id, guild.id))
		else:
			self.bot.sql("UPDATE guilds SET AutoRole_role = '0' WHERE id = %s" %(guild.id))
			
	async def cmd_setautorole(self, message, *args):
		await self.cmd_autorole(message, *args)
		
	async def on_member_join(self, member):
		role_id = self.get(member.guild)
		role_obj = utils.find.role(role_id, guild=member.guild)
		if role_obj != None:
			await member.add_roles(role_obj, reason="AutoRole")
		
	async def cmd_autorole(self, message, *args):
		"""When a member will join the guild, he will obtain the role.
		
{0}autorole <ROLE>"""
		if message.author.guild_permissions.manage_guild or self.bot.user.id == message.author.id:
			if len(args) != 0:
				role = utils.find.role(" ".join(args[0:]), guild=message.guild)
				if role != None:
					self.set(message.guild, role)
					_message = await message.channel.send(None, embed=E(message.author, "Enabled auto-role for\n``{0}``".format(role.name)))
				else:
					_message = await message.channel.send(None, embed=E(message.author, "Disabled auto-role."))
				self.set(message.guild, role)
			else:
				_message = await message.channel.send(None, embed=E(message.author, "You must specify a role."))
				await asyncio.sleep(5)
				await _message.delete()
		else:
			_message = await message.channel.send(None, embed=E(message.author, "You are not allowed to use that command."))
			await asyncio.sleep(5)
			await _message.delete()
	
def load(client):
	client.add_command(AutoRole(client))