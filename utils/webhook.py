from discord import Webhook, AsyncWebhookAdapter
import aiohttp

async def send(webhook_url, message_content, embed=None, username=None, avatar_url=None):
	if username == None:
		username = client.user.name
	if avatar_url == None:
		avatar_url = "https://cdn.discordapp.com/avatars/363725802652696577/8dbc0473e8f512a22ba0742f6dba31c6.png"
		
	async with aiohttp.ClientSession() as session:
		webhook = Webhook.from_url(webhook_url, adapter=AsyncWebhookAdapter(session))
		await webhook.send(message_content, embed, username=username, avatar_url=avatar_url)