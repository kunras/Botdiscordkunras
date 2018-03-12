class UnsupportedType(Exception):
	pass
	
class GuildNotDefined(Exception):
	pass

def user(abc, guild=None):
	if abc.__class__ == int:
		if guild == None:
			return client.get_user(abc)
		else:
			return guild.get_member(abc)
	elif abc.__class__ == str:
		abd = ""
		for letter in abc:
			if letter.isdigit():
				abd += letter
		try:
			abd = int(abd)
			if guild == None:
				return client.get_user(abd)
			else:
				return guild.get_member(abd)
		except:
			pass
		if guild == None:
			for member in bot.users:
				if abc.lower() in str(member).lower():
					return member
		else:
			for member in guild.members:
				if abc.lower() in str(member).lower():
					return member
	else:
		raise UnsupportedType("Type {0} unsupported.".format(abc.__class__.__name__))

def role(abc, guild=None):
	if guild == None:
		raise GuildNotDefined("Guild not defined.")
	else:
		if abc.__class__ == int:
			for role in guild.roles:
				if abc == role.id:
					return role
			return None
		elif abc.__class__ == str:
			role_id_str = ""
			for char in abc:
				if char.isdigit():
					role_id_str += char
			try: role_id = int(role_id_str)
			except: role_id = 0
			for role in guild.roles:
				if role_id == role.id:
					return role
			for role in guild.roles:
				if abc.lower() in role.name.lower():
					return role
			return None
		else:
			raise UnsupportedType("Type {0} unsupported.".format(abc.__class__.__name__))