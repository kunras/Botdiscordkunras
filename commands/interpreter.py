from commandsample import C
from contextlib import redirect_stdout
from io import StringIO
import textwrap, traceback, asyncio
from utils.answers import embed as E

class PythonInterpreter(C):

	async def on_loaded(self):
		if self.bot.user.bot:
			appinfo = await self.bot.application_info()
			self.owner = appinfo.owner
		else:
			self.owner = self.bot.user
			
	async def interpreter(self, message, *args):
		if message.author.id == self.owner.id:
			env = {
				"bot": self.bot,
				"client": self.bot,
				"message": message,
				"discord": self.bot.discord
			}
			env.update(globals())
			_script = " ".join(args)
			if _script.startswith('```') and _script.endswith('```'):
				_script = '\n'.join(_script.split('\n')[1:-1])
			_script = _script.strip('` \n')
			script = 'async def fonction():\n{}'.format(textwrap.indent(_script, "	"))
			try:
				exec(script, env)
			except Exception as e:
				return await message.channel.send(None, embed=E(message.author, '```fix\n{}: {}\n```'.format(e.__class__.__name__, e)))
			fonction = env["fonction"]
			retour = StringIO()
			try:
				with redirect_stdout(retour):
					retour_func = await fonction()
			except Exception as e:
				retour_str = retour.getvalue()
				return await message.channel.send(None, embed=E(message.author, '```\n{}{}\n```'.format(retour_str, traceback.format_exc())))
			else:
				retour_str = retour.getvalue()
				texte = None
				if retour_func == None:
					if retour_str:
						texte = '```\n{}\n```'.format(retour_str)
					else:
						try: texte = '```\n{}\n```'.format(repr(eval(_script, env)))
						except: pass
				else:
					texte = '```\n{}{}\n```'.format(retour_str, retour_func)
			if texte != None:
				try: await message.channel.send(None, embed=E(message.author, texte))
				except: self.bot.log("[%s] Unable to send embeds in this channel" %(__class__.__name__))
			else:
				try: await message.add_reaction("✅")
				except: pass
		else:
			try:
				_message = await message.channel.send(f"{message.author.mention}, you're not allowed to execute that command. :thinking:")
				await asyncio.sleep(5)
				await _message.delete()
			except: pass
		
			
	async def cmd_py(self, message, *args):
		await self.interpreter(message, *args)
	async def cmd_exec(self, message, *args):
		await self.interpreter(message, *args)
	async def cmd_python(self, message, *args):
		await self.interpreter(message, *args)
	async def cmd_eval(self, message, *args):
		await self.interpreter(message, *args)
	async def cmd_do(self, message, *args):
		await self.interpreter(message, *args)
	async def cmd_compile(self, message, *args):
		await self.interpreter(message, *args)
		
def load(client):
	client.add_command(PythonInterpreter(client))