from commandsample import C
import utils.find
import utils.answers as A

class Avatar(C):

	async def cmd_avatar(self, message, *args):
		"""Get the avatar from an user or the server.
		
{0}avatar <@user OR "server">"""
		if len(args) != 0:
			serverMode = False
			user = (utils.find.user(args[0], guild=message.guild))
			if args[0] in ["server","guild","s","serveur","g"]:
				user = message.guild
				serverMode = True
			if user != None:
				embed = A.embed(message.author, "``{0}``".format(str(user)))
				if serverMode:
					embed.set_image(url=user.icon_url_as(format="png"))
				else:
					embed.set_image(url=user.avatar_url_as(format="png"))
				await message.channel.send(None, embed=embed)
			else:
				await message.channel.send(None, embed=A.embed(message.author, "Unknown user"))
		else:
			embed = A.embed(message.author, None)
			embed.title = "hpybot avatar"
			embed.add_field(name="<:arrowright:403301430695428096> DESCRIPTION", value="**Get the avatar from an user or the server.**", inline=False)
			embed.add_field(name="<:arrowright:403301430695428096> SYNTAX", value="``hpybot avatar [@user OR \"server\"]``", inline=False)
			await message.channel.send(None, embed=embed)
			
def load(client):
	client.add_command(Avatar(client))