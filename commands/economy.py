from commandsample import C
from utils.find import user as U
from utils.answers import embed as E
from random import choice as random
from random import randint

### COMMANDS ARE BELOW ###

class Economy(C):
	
	async def on_loaded(self):
	
		class Profile:
			def __init__(this, user):
			
				class Inventory:
					def __init__(that, user):
						if not user in [None, int, str]:
							that.user = user
						else:
							raise TypeError("Incorrect type given for the Profile.Inventory in Economy module")
							
					def set(that, inventory):
						that.get()
						self.bot.sql("UPDATE users SET inventory = ? WHERE id = ?", (str(inventory), that.user.id))
						
					def edit(that, item_id, dict={}):
						Inventory = that.get()
						Object = None
						Object_NUM = 0
						for InventoryObject in Inventory:
							if InventoryObject != None:
								if InventoryObject.get("_id") == item_id:
									Object = InventoryObject
									Object_NUM = Inventory.index(InventoryObject)
									break
						if Object != None:
							Object.update(dict)
							Object.update({"_id": item_id})
							Inventory[Object_NUM] = Object
						that.set(Inventory)
							
					def use(that, item_id):
						inventory = that.get()
						objets = []
						if item_id != list:
							objets = [item_id]
						else:
							objets = item_id
						for objet in inventory:
							if objet != None:
								if objet.get("_id", "undefined") in objets:
									print(objet.get("_name"), objet.get("_id"))
									inventory[inventory.index(objet)] = None
						that.set(inventory)
						return True
						
					def add(that, item, times=1, dict={}, tags=None):
						if tags == None:
							tags = [item]
						inventory = that.get()
						objet = {
							"_name": item,
							"_tags": tags
						}
						objet.update(dict)
						objet.update({
							"_id": len(inventory)+1
						})
						for i in range(times):
							inventory.append(objet)
						that.set(inventory)
						
					def get(that, item=None):
						a = self.bot.sql("SELECT inventory FROM users WHERE id = {0}".format(this.user.id))
						if item == None:
							if a != None:
								return eval(a[0][0])
							return []
						else:
							if a != None:
								inventory = eval(a[0][0])
								retourner = []
								for objet in inventory:
									if objet != None:
										if item in objet.get("_tags", []):
											retourner.append(objet)
								return retourner
							return []
						
				if not user in [None, int, str]:
					this.user = user
					this.inventory = Inventory(user)
				else:
					raise TypeError("Incorrect type given for the Profile machin in Economy module")
					
			def get_money(this):
				a = self.bot.sql("SELECT money FROM users WHERE id = {0}".format(this.user.id))
				if a == None:
					return 0
				else:
					return int(a[0][0])
					
			def set_money(this, amount):
				acc = self.bot.sql("SELECT money FROM users WHERE id = {0}".format(this.user.id))
				if acc == None:
					self.bot.sql("INSERT INTO users (id) VALUES ({0})".format(this.user.id))
				self.bot.sql("UPDATE users SET money = ? WHERE id = ?", (amount, this.user.id))
					
		self.get_profile = Profile
		self.bot.sql("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY NOT NULL UNIQUE)")
		retour = self.bot.sql("PRAGMA table_info('users')")
		if not "money" in [x[1] for x in retour]:
			self.bot.sql("ALTER TABLE users ADD money INTEGER DEFAULT '0'")
		if not "inventory" in [x[1] for x in retour]:
			self.bot.sql("ALTER TABLE users ADD inventory TEXT DEFAULT '{}'")
		if not "last_hourly" in [x[1] for x in retour]:
			self.bot.sql("ALTER TABLE users ADD last_hourly INTEGER DEFAULT '0'")
			
	async def cmd_hourly(self, message, *args):
		await self.cmd_hr(message, *args)
	async def cmd_hr(self, message, *args):
		bonus = 60
		destinataire = message.author
		b = False
		if len(args) > 0:
			_destinataire = ""
			for letter in args[0]:
				if letter.isdigit():
					_destinataire += letter
			try:
				if self.bot.user.bot:
					destinataire = await bot.get_user_info(int(_destinataire))
				else:
					destinataire = await bot.get_user_profile(int(_destinataire)).user
			except:
				destinaire = None
				try:
					await message.channel.send(None, embed=E(message.author, "Unable to find the user."))
				except:
					await message.author.send(f":warning: Insufficient permission in the channel {channel.mention}...")
					await message.author.send(None, embed=E(message.author, "Unable to find the user."))
		if message.created_at.timestamp() - message.author.created_at.timestamp() < 604800:
			try:
				await message.channel.send(None, embed=E(message.author, "Your account must be older than 7 days to execute that command."))
			except:
				await message.author.send(f":warning: Insufficient permission in the channel {channel.mention}...")
				await message.author.send(None, embed=E(message.author, "Your account must be older than 7 days to execute that command."))
			destinataire = None
		if destinataire != None:
			a = self.bot.sql("SELECT last_hourly FROM users WHERE id = {0}".format(message.author.id))
			if a == None:
				self.bot.sql("INSERT INTO users (id) VALUES (%s)" %(message.author.id))
				b = True
			else:
				calcul = message.created_at.timestamp()-int(a[0][0])
				if calcul > 3600:
					b = True
				else:
					try:
						await message.channel.send(None, embed=E(message.author, "You will be able to do that in {0} minutes.".format(int((3600-calcul)/60)+1)))
					except:
						await message.author.send(f":warning: Insufficient permission in the channel {message.channel.mention}...")
						await message.author.send(None, embed=E(message.author, "You will be able to do that in {0} minutes.".format(int((3600-calcul)/60)+1)))
		if b:
			self.bot.sql("UPDATE users SET last_hourly = ? WHERE id = ?", (message.created_at.timestamp(), message.author.id))
			profile = self.get_profile(destinataire)
			currentMoney = profile.get_money()
			profile.set_money(currentMoney + bonus)
			if destinataire.id == message.author.id:
				try:
					await message.channel.send(None, embed=E(message.author, "Reward received. Come back in 60 minutes! :wave:"))
				except:
					await message.author.send(f":warning: Insufficient permission in the channel {message.channel.mention}...")
					await message.author.send(None, embed=E(message.author, "Reward received. Come back in 60 minutes! :wave:"))
			else:
				try:
					await message.channel.send(None, embed=E(message.author, "Reward given to {0} ({1}).".format(str(user), user.mention)))
				except:
					await message.author.send(f":warning: Insufficient permission in the channel {message.channel.mention}...")
					await message.author.send(None, embed=E(message.author, "Reward given to {0} ({1}).".format(str(user), user.mention)))
			
	async def cmd_give(self, message, *args):
		if len(args) == 0:
			await message.channel.send(None, embed=E(message.author, "You must specify a user."))
		else:
			user = U(args[0], guild=message.guild)
			if user != None:
				if len(args) > 1:
					amount = args[1]
					if amount.endswith("µ"):
						amount = amount[:-1]
					if amount.isdigit():
						amount = int(amount)
						if amount > 0:
							profile = self.get_profile(message.author)
							profile2 = self.get_profile(user)
							if profile.get_money() < amount:
								await message.channel.send(None, embed=E(message.author, "This amount is superior to your balance."))
							else:
								profile.set_money(profile.get_money()-amount)
								profile2.set_money(profile2.get_money()+amount)
								await message.add_reaction("📤")
								await profile2.user.send(f"📥 {str(profile.user)}/{profile.user.mention} gived you **{amount}µ** in the following guild **{message.guild.name}**/{message.channel.mention}")
						else:
							await message.channel.send(None, embed=E(message.author, "You must specify an amount."))
					else:
						await message.channel.send(None, embed=E(message.author, "You must specify an amount."))
				else:
					await message.channel.send(None, embed=E(message.author, "You must specify an amount."))
			else:
				await message.channel.send(None, embed=E(message.author, "You must specify a user."))
			
	async def cmd_profile(self, message, *args):
		if len(args) == 0:
			user = message.author
		else:
			user = U(" ".join(args[0:]), guild=message.guild)
		if user != None:
			profile = self.get_profile(user)
			__inv = ""
			_inv = {}
			inventory = profile.inventory.get()
			__badges = "[**"+random(["Under construction", "Coming soon!", "It's a future feature! :+1:"])+"**]"
			if len(inventory) == 0:
				__inv = "[**Empty inventory**]"
			else:
				for element in inventory:
					if element != None:
						el_name = element.get("_name", "undefined")
						if _inv.get(el_name):
							_inv[el_name] += 1
						else:
							_inv[el_name] = 1
				for element in _inv:
					__inv += "**"+str(_inv[el_name])+"x** "+el_name+"\n"
					if __inv == "":
						__inv = '[**Empty inventory**]'
			embed = E(message.author, "`"+str(user)+"`")
			embed.set_thumbnail(url=user.avatar_url_as(format="png"))
			embed.title = "▬ PROFILE ▬"
			embed.add_field(name="Balance", value=str(profile.get_money())+"**µ**", inline=False)
			embed.add_field(name="Inventory", value=__inv, inline=False)
			embed.add_field(name="Badges", value=__badges, inline=False)
			await message.channel.send(message.author.mention, embed=embed)
		else:
			embed = E(message.author, "**Unknown user.**")
			await message.channel.send(message.author.mention, embed=embed)
			
def load(client):
	client.add_command(Economy(client))