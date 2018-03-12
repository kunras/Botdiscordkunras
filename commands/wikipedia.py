from commandsample import C
from utils.answers import embed as E
from utils.answers import content as N

class Wikipedia(C):

	async def on_loaded(self):
		try:
			import wikipedia
			self.wikipedia = wikipedia
		except:
			class NotImplementedModule(Exception):
				pass
			raise NotImplementedModule("Please install the \"wikipedia\" module by doing this:   pip install wikipedia")

	async def cmd_wikipedia(self, message, *args):
		"""Search something on Wikipedia.
		
{0}wikipedia <request>"""
		async with message.channel.typing():
			embeddingMethod = False
			article_name = None
			request = None
			if message.guild.me.permissions_in(message.channel).embed_links:
				embeddingMethod = True
			if len(args) == 0:
				article_name = self.wikipedia.random()
			else:
				article_name = " ".join(args)
			try:
				request = self.wikipedia.page(article_name)
			except self.wikipedia.exceptions.PageError:
				if embeddingMethod:
					await message.channel.send(None, embed=E(message.author, "No page with that name was found."))
				else:
					await message.channel.send(N(message.author,"No page with that name was found."))
			except self.wikipedia.exceptions.DisambiguationError as e:
				request = self.wikipedia.page(e.options[0])
			if request != None:
				if embeddingMethod:
					embed = E(message.author, ".".join(request.content.split(".")[0:2])+".\n\n[**See also on Wikipedia**]("+request.url+")")
					embed.set_author(name=request.title.upper(), icon_url="http://upload.wikimedia.org/wikipedia/en/thumb/8/80/Wikipedia-logo-v2.svg/1024px-Wikipedia-logo-v2.svg.png", url=request.url)
					try: embed.set_thumbnail(url=request.images[0])
					except: pass
					await message.channel.send(None, embed=embed)
				else:
					await message.channel.send(N(message.author, request.url))
	
def load(client):
	client.add_command(Wikipedia(client))