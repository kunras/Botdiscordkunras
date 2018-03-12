import discord, inspect

class C:
	def __init__(self, client):
		self.bot = client
		self.discord = discord
		self.db = self.bot.db