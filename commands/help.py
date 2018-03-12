from commandsample import C
from discord import Embed as E

class ListingCommands(C):

	async def cmd_help(self, message, *args):
		"""Get the list of all commands available
		
{0}help - get the list of all commands available"""
		finalMessage = "" #
		if len(args) == 0: # If no command is asked
			for command in self.bot._.commands: # Check all files
				for element in dir(command): # Check all commands in a file
					function = getattr(command, element) # Get the function of all commands in a file
					if function.__class__.__name__ == "method" and element.startswith("cmd_"): # If it's a "method" and name startswith ("cmd_")
						if function.__doc__ != None: # And if there is a docstring
							finalMessage += "**["+self.bot.config["prefixs"][0]+element[4:]+"](https://github.com/Dannyiy/hpybot)**   •   "+function.__doc__.split("\n")[0]+"\n" # Add the FIRST LINE to the finalMessage
			embed = E()
			embed.description = finalMessage
			embed.set_footer(text=str(message.author), icon_url=message.author.avatar_url_as(format="png"))
			embed.title = "ﾠﾠﾠ▬ ﾠ COMMAND LIST ﾠ ▬"
			embed.colour = 0x32363b
			embed.set_thumbnail(url=self.bot.user.avatar_url_as(format="png"))
			await message.channel.send(None, embed=embed)
		else:
			for command in self.bot.commands:
				for element in dir(command):
					function = getattr(command, element)
					if function.__class__.__name__ == "method" and element == "cmd_"+args[0]:
						if function.__doc__ != None:
							await message.channel.send(None, embed=E(description=function.__doc__.replace("{0}", self.bot.config["prefixs"][0])))
						else:
							await message.channel.send(None, embed=E(description="No description."))
							
def load(client):
	client.add_command(ListingCommands(client))