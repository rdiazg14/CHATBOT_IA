import discord
llave = "ODkwMDQzNDgyODUxNDAxNzk5.YUqDlg.xkvK6aeom4GTxdHR5YH-hPY9HWw"

cliente = discord.Client()
@cliente.event
async def on_message(mensaje):
	if mensaje.content.find("!hola-mundo")!=-1:
		await mensaje.channel.send("Hola! desde discord")
cliente.run(llave)