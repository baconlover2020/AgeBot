import discord
import os
import shutil
from adicionar_mobis import adicionar_categoria


token = "ODExNjI0NTIwNjE5OTE3MzQ1.YC06PA.udLKKuwfq3_iegtWTSr8RUmbIyM"
client = discord.Client()
pasta_categorias = "temp_categorias"

@client.event
async def on_ready():
    print("Bot logado")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("!addcategoria"):
        for attachment in message.attachments:
            await attachment.save(f"{pasta_categorias}/{attachment.filename}")
            await message.channel.send(f"Baixando: {attachment.filename}")
        for categoria in os.listdir(pasta_categorias):
            if categoria.endswith(".zip"):
                await message.channel.send(f"Descompactando: {categoria}")
                shutil.unpack_archive(os.path.join(pasta_categorias,categoria), pasta_categorias)
                os.remove(os.path.join(pasta_categorias,categoria))
        for categoria in os.listdir(pasta_categorias):
            await message.channel.send(f"Adicionando Categoria: {categoria}")
            adicionar_categoria(os.path.join(pasta_categorias, categoria))
            shutil.move(os.path.join(pasta_categorias, categoria), "adicionados/"+ categoria)
            #shutil.rmtree(os.path.join(pasta_categorias,categoria), ignore_errors=True)
            await message.channel.send(f"A categoria \"{categoria}\" foi adicionada com êxito!")
                
                



client.run(token)
