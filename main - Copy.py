import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from nextcord.ext.commands import has_permissions,MissingPermissions
from nextcord import Member
from nextcord import FFmpegOpusAudio,ButtonStyle
from nextcord.ui import Button,View
import datetime
import requests
import os
import sys
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

queues={}

def check_queue(ctx,id):
    if queues[id]!=[]:
        voice=ctx.guild.voice_client
        source=queues[id].pop(0)
        player=voice.play(source)



intents=nextcord.Intents.default()
intents.message_content=True
intents.members=True
client=commands.Bot(command_prefix='>',intents=intents)

@client.event
async def on_ready():
    print("The bot is now ready for use.")
    print("-----------------------------")

    await client.change_presence(status=nextcord.Status.idle,activity=nextcord.Activity(type=nextcord.ActivityType.listening,name='your requests'))
kalaaogeid=1192315897264754818

@client.slash_command(guild_ids=[1192315897264754818])
async def test(interaction: Interaction):
    await interaction.response.send_message("Slashtest")
@client.command()
async def hello(ctx):
    user=ctx.author.display_name
    await ctx.send(f"Hey there, {user} !!:handshake:")
    
@client.command()
async def bye(ctx):
    user=ctx.author.display_name
    await ctx.send(f"Goodbye {user}, See you soon !! :wave:")
@client.event
async def on_member_join(member):
    channel=client.get_channel(1185242223810461727)
    await channel.send("Welcome new member")
@client.event
async def on_member_remove(member):
    channel=client.get_channel(1185242223810461727)
    await channel.send("Bye past member")
@client.command()
async def joke(ctx):
    
    url = "https://jokeapi-v2.p.rapidapi.com/joke/Any"

    querystring = {"format":"json","contains":"","idRange":"0-150","blacklistFlags":"nsfw,racist"}

    headers = {
        "X-RapidAPI-Key": "8ce1649da6msh26dcd3b92f2a1ffp1b2ac8jsn7b955f6d677a",
        "X-RapidAPI-Host": "jokeapi-v2.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    await ctx.send(response.json()['setup']+" "+response.json()['delivery'])

@client.slash_command(name='joke',description='Get a funny(hopefully) joke.',guild_ids=[kalaaogeid])
async def joke(interaction: Interaction):
    
    url = "https://jokeapi-v2.p.rapidapi.com/joke/Any"

    querystring = {"format":"json","contains":"","idRange":"0-150","blacklistFlags":"nsfw,racist"}

    headers = {
        "X-RapidAPI-Key": "8ce1649da6msh26dcd3b92f2a1ffp1b2ac8jsn7b955f6d677a",
        "X-RapidAPI-Host": "jokeapi-v2.p.rapidapi.com"
    }

    response_ = requests.get(url, headers=headers, params=querystring)

    await interaction.response.send_message(response_.json()['setup']+" "+response_.json()['delivery'])

@client.command(pass_context=True)
async def join(ctx):
    user=ctx.author.display_name
    
    if (ctx.author.voice):
        channel=ctx.message.author.voice.channel
        voice=await channel.connect()
        await ctx.send(f"Joined your voice channel, {user}.")
    else:
        await ctx.send("Kindly join a voice channel to use this command.")


@client.slash_command(guild_ids=[kalaaogeid])
async def join(interaction: Interaction):
    usern=interaction.user.display_name
    
    if (interaction.user.voice):
        channel=interaction.user.voice.channel
        voice=await channel.connect()
        await interaction.response.send_message(f"Joined your voice channel, {usern}.")
    else:
        await interaction.response.send_message("Kindly join a voice channel to use this command.")

@client.command(pass_context=True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I left the voice channel")
    else:
        await ctx.send("I am not in a voice channel.")

@client.slash_command(guild_ids=[kalaaogeid])
async def leave(interaction:Interaction):
    if client.voice_clients:
        await interaction.guild.voice_client.disconnect()
        await interaction.send("I left the voice channel")
    else:
        await interaction.send("I am not in a voice channel.")

@client.command(pass_context=True)
async def pause(ctx):
    voice=nextcord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
        await ctx.send('Paused the current track.')
    else:
        await ctx.send('No track is playing at the moment.')


@client.slash_command(guild_ids=[kalaaogeid])
async def pause(interaction: Interaction):
    voice=nextcord.utils.get(client.voice_clients,guild=interaction.guild)
    if voice.is_playing():
        voice.pause()
        await interaction.send('Paused the current track.')
    else:
        await interaction.send('No track is playing at the moment.')

@client.command(pass_context=True)
async def resume(ctx):
    voice=nextcord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
        await ctx.send('Resumed the current track.')
    else:
        await ctx.send('No track is paused at the moment.')

@client.slash_command(guild_ids=[kalaaogeid])
async def resume(interaction:Interaction):
    voice=nextcord.utils.get(client.voice_clients,guild=interaction.guild)
    if voice.is_paused():
        voice.resume()
        await interaction.send('Resumed the current track.')
    else:
        await interaction.send('No track is paused at the moment.')

@client.command(pass_context=True)
async def stop(ctx):
    voice=nextcord.utils.get(client.voice_clients,guild=ctx.guild)
    voice.stop()
    await ctx.send('Stopped the playing track.')

@client.slash_command(guild_ids=[kalaaogeid])
async def stop(interaction:Interaction):
    voice=nextcord.utils.get(client.voice_clients,guild=interaction.guild)
    voice.stop()
    await interaction.send('Stopped the playing track.')

@client.command(pass_context=True)
async def play(ctx, arg):
    voice=ctx.guild.voice_client
    song=('D:\\discordbot\\music\\'+str(arg)+'.mp3')
    source=FFmpegOpusAudio(song)
    player=voice.play(source,after= lambda x=None: check_queue(ctx,ctx.message.guild.id))
    await ctx.send(f'Playing {arg}.')


@client.slash_command(guild_ids=[kalaaogeid])
async def play(interaction: Interaction, song):
    voice=interaction.guild.voice_client
    song_=resource_path('music\\'+str(song)+'.mp3')
    source=FFmpegOpusAudio(song_)
    player=voice.play(source,after= lambda x=None: check_queue(interaction,interaction.guild.id))
    await interaction.send(f'Playing {song}.')


@client.command(pass_context=True)
async def queue(ctx,arg):
    voice=ctx.guild.voice_client
    song=('D:\\discordbot\\music\\'+str(arg)+'.mp3')
    source=FFmpegOpusAudio(song)

    guild_id=ctx.message.guild.id 

    if guild_id in queues:
        queues[guild_id].append(source)
    else:
        queues[guild_id]=[source]

    await ctx.send(f'Added {arg} to the queue.') 

@client.slash_command(guild_ids=[kalaaogeid])
async def queue(interaction: Interaction,song):
    voice=interaction.guild.voice_client
    song_=resource_path('music\\'+str(song)+'.mp3')
    source=FFmpegOpusAudio(song_)

    guild_id=interaction.guild.id 

    if guild_id in queues:
        queues[guild_id].append(source)
    else:
        queues[guild_id]=[source]

    await interaction.send(f'Added {song} to the queue.') 

@client.event
async def on_message(message):
    print(str(message.author) + ': < ' + str(message.content)+" > at "+str(message.created_at.strftime("%Y-%m-%d %H:%M:%S")))
    if 'phrase' in message.content:
        await message.delete()
        await message.channel.send(f'Tameez mein reh le {message.author}.')
    await client.process_commands(message)

@client.command()
@has_permissions(kick_members=True)
async def kick(ctx,member : nextcord.Member,reason):
    await member.kick(reason=reason)
    await ctx.send(f'User {member} has been kicked.')

@kick.error
async def kick_error(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.send('You don\'t have permission to kick members')

coloreddeda=nextcord.Colour(00000000)
@client.command()
@has_permissions(ban_members=True)
async def ban(ctx,member : nextcord.Member,reason):
    await member.ban(reason=reason)
    await ctx.send(f'User {member} has been banned.')

@ban.error
async def ban_error(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.send('You don\'t have permission to ban members')

@client.command()
async def embed(ctx):
    embed=nextcord.Embed(title='Title',url="https://google.com",description="Description",color=coloreddeda)
    embed.set_author(name=ctx.author.display_name,url="https://www.instagram.com/hard1k_k/",icon_url=ctx.author.avatar.url)
    embed.set_thumbnail(url=ctx.author.avatar.url)
    embed.add_field(name="Field 1",value="Value of field 1",inline=True)
    embed.add_field(name="Field 2",value="Value of field 2",inline=True)
    embed.set_footer(text="Footer")
    
    await ctx.send(embed=embed)




client.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.send('You don\'t have the permissions to run this command')

@client.command()
async def dm(ctx,user:nextcord.Member,*,message=None):
    message="Welcome to the server,"
    usern=user.display_name
    embed=nextcord.Embed(title="Welcome",description=f'{message} {usern} :pray:',color=255)
    embed.set_author(name=usern,icon_url=user.avatar.url)
    embed.set_thumbnail(url=ctx.guild.icon.url)
    embed.add_field(name=" Don't forget to choose your preferred roles in the roles channel",value="",inline=True)
    embed.set_footer(text="Enjoy the server.")
    await user.send(embed=embed)

@client.event
async def on_reaction_add(reaction,user):
    channel=reaction.message.channel
    await channel.send(user.display_name+' added '+reaction.emoji)

@client.event
async def on_reaction_remove(reaction,user):
    channel=reaction.message.channel
    await channel.send(user.display_name+' removed '+reaction.emoji)


@client.command(pass_context=True)
@has_permissions(manage_roles=True)
async def addrole(ctx,user: nextcord.Member,*,role: nextcord.Role):
    if role in user.roles:
        await ctx.send(f"{user.display_name} already has the {role} role.")
    else:
        await user.add_roles(role)
        await ctx.send(f"Added role to {user.display_name}")


@client.command(pass_context=True)
@has_permissions(manage_roles=True)
async def removerole(ctx,user: nextcord.Member,*,role: nextcord.Role):
    if role in user.roles:
        await user.remove_roles(role)
        await ctx.send(f"Removed the {role} role from {user.display_name}")
    else:
        await ctx.send(f"{user.display_name} doesn't have the {role} role.")

@client.command(name='button1')
async def button1(ctx):
    object=Button(label='Label',style=ButtonStyle.blurple)
    
    async def button1_callback(interaction):
        await interaction.response.send_message("Button 1 was clicked.")

    object.callback=button1_callback

    myview=View(timeout=180)
    myview.add_item(object)

    await ctx.send('Buttons',view=myview)

@client.slash_command(name='button1',guild_ids=[kalaaogeid])
async def button1(interaction_:Interaction):
    object=Button(label='Label',style=ButtonStyle.blurple)
    
    async def button1_callback(interaction):
        await interaction.response.send_message("Button 1 was clicked.")

    object.callback=button1_callback

    myview=View(timeout=180)
    myview.add_item(object)

    await interaction_.send('Buttons',view=myview)


client.run('<<BOT TOKEN ID>>')
