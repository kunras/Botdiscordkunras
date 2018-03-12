from discord import Embed

def embed(author, message):
	if author == None:
		author = client.user
	if message == None:
		message = ""
	embed = Embed()
	embed.colour = 0x32363b
	embed.set_footer(text=str(author), icon_url=author.avatar_url_as(format="png"))
	embed.description = message
	return embed

def content(author, message):
	return author.mention+"     |     "+message