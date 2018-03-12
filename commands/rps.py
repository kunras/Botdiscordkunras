from commandsample import C
import asyncio
from utils.answers import embed as E
from utils.find import user as U

class RPS(C):
	async def awaitSelection(self, game, player):
		played = False
		message = await player.send("The game has started! What do you want to choose?")
		async def add_reactions(m):
			await m.add_reaction("🌑")
			await m.add_reaction("📰")
			await m.add_reaction("✂")
		self.bot.loop.create_task(add_reactions(message))
		while not played:
			def check(r, u):
				return r.message.id == message.id and u.id != self.bot.user.id
			reaction, user = await self.bot.wait_for("reaction_add", check=check)
			if str(reaction) in ["🌑","📰","✂"]:
				played = True
		if game["players"]["1"]["id"] == player.id:
			game["players"]["1"]["sign"] = str(reaction)
			await game["players"]["2"]["object"].send("``⏲`` **Your opponent has made his choice.**")
			if game["players"]["2"]["sign"] != None:
				game["ready"] = True
		elif game["players"]["2"]["id"] == player.id:
			game["players"]["2"]["sign"] = str(reaction)
			await game["players"]["1"]["object"].send("``⏲`` **Your opponent has made his choice.**")
			if game["players"]["1"]["sign"] != None:
				game["ready"] = True
		if game["ready"]:
			await self.gameReady(game)
			
	async def gameReady(self, game):
		choice1 = game["players"]["1"]["sign"]
		player1 = game["players"]["1"]["object"]
		choice2 = game["players"]["2"]["sign"]
		player2 = game["players"]["2"]["object"]
		winner = None
		if choice1 == "🌑" and choice2 == "✂":
			winner = True
		elif choice1 == "✂" and choice2 == "🌑":
			winner = False
		elif choice1 == "✂" and choice2 == "📰":
			winner = True
		elif choice1 == "📰" and choice2 == "✂":
			winner = False
		elif choice1 == "📰" and choice2 == "🌑":
			winner = True
		elif choice1 == "🌑" and choice2 == "📰":
			winner = False
		if winner != None:
			await game["players"]["1" if winner else "2"]["object"].send(":+1:   **|**   *You won the game!*")
			await game["players"]["1" if not winner else "2"]["object"].send(":-1:   **|**   *You lose the game!*")
		embed = self.bot.discord.Embed()
		embed.title = "GAME | RPS"
		embed.colour = 0x2986B8
		embed.add_field(name=str(player1), value=choice1)
		embed.add_field(name=str(player2), value=choice2)
		for player_id_str in game["players"]:
			if winner == None:
				await game["players"][player_id_str]["object"].send(":ok_hand:   **|**   *Nobody won this game!*")
			await game["players"][player_id_str]["object"].send(game["channel"].mention if game["channel"].__class__ != self.discord.channel.DMChannel else None, embed=embed)
		if game["channel"].__class__ != self.discord.channel.DMChannel:
			await game["channel"].send(None, embed=embed)

	async def cmd_pfc(self, message, *args):
		await self.cmd_rps(message, *args)
	async def cmd_rps(self, message, *args):
		if len(args) > 0:
			user = None
			user_str = ""
			if args[0].startswith("<") and args[0].endswith(">"):
				for letter in args[0]:
					if letter.isdigit():
						user_str += letter
			user = self.bot.get_user(int(user_str))
			invitation_message = " ".join(args[1:])
			for word in invitation_message.split(" "):
				for bannedword in ["discord.me/","discord.gg/","discord.rip/","disco.gg/","discordapp.com/invite/"]:
					if bannedword in word:
						invitation_message = ""
						await message.author.send(":warning: | You can't send a Discord Server with the invitation.")
				if word.startswith('emoji["') and word.endswith('"]'):
					print(word)
					emoji_str = word[7:-2]
					print(emoji_str)
					for emoji in self.bot.emojis:
						if emoji.name == emoji_str:
							invitation_message = invitation_message.replace(word, str(emoji))
							break
			if user != None:
				if user.id != message.author.id:
					if user.bot:
						return
					try: await message.add_reaction("📤")
					except:
						try: await message.channel.send("📤")
						except: await message.author.send("I do not have the permission to talk in this channel: {0}".format(message.channel.mention))
					await message.author.send("📤 - Waiting {0}...".format(user.mention))
					if invitation_message != "":
						embed = self.bot.discord.Embed()
						embed.set_author(name=str(message.author))
						embed.description = invitation_message
						embed.colour = 0x000001
					else:
						embed = None
					#_message = await user.send("📥 - {0} invited you to play RPS.{1}".format(message.author.mention, ("\n```fix\n"+invitation_message+"\n```") if invitation_message != "" else ""))
					_message = await user.send("📥 - {0} invited you to play RPS.".format(message.author.mention), embed=embed)
					async def add_reactions(m):
						await m.add_reaction("✅")
						await m.add_reaction("❎")
					def check(r, u):
						return r.message.id == _message.id and u.id != self.bot.user.id
					self.bot.loop.create_task(add_reactions(_message))
					_reaction, _user = await self.bot.wait_for("reaction_add", check=check)
					if str(_reaction) == "✅":
						game = {
							"players": {
								"1": {
									"id": message.author.id,
									"object": message.author,
									"sign": None
								},
								"2": {
									"id": user.id,
									"object": user,
									"sign": None
								}
							},
							"channel": message.channel,
							"ready": False
						}
						self.bot.loop.create_task(self.awaitSelection(game, message.author))
						self.bot.loop.create_task(self.awaitSelection(game, user))
					else:
						await message.author.send(":x: - {0} denied your request.".format(user.mention))
				else:
					_message = await message.channel.send(None, embed=(
							E(message.author,  "You can't play with yourself!"  )
						))
					await asyncio.sleep(5)
					await _message.delete()
			else:
				_message = await message.channel.send(None, embed=(
						E(message.author,  "No user with that name has been found."  )
					))
				await asyncio.sleep(5)
				await _message.delete()

		else:
			_message = await message.channel.send(None, embed=(
					E(message.author,  "This game can't be played alone."  )
				))
			await asyncio.sleep(5)
			await _message.delete()
		
	
def load(client):
	client.add_command(RPS(client))