import discord, pyscreenshot, time, os
from pynput.keyboard import Controller, Key

client = discord.Client()
keyboard = Controller()

import src.nds as platform
keys = platform.keys(Key)

message = None
channel = 952371099801378839

@client.event
async def on_ready():
  await client.wait_until_ready()
  activity = discord.Game(name="games! | https://discord.gg/HyUeFkNseb")
  
  await client.change_presence(activity=activity)
  print(f"Logged in as {client.user.name}")

  global message
  
  message = await client.get_channel(channel).send("React with anything to begin...")
  for key in keys.keys(): await message.add_reaction(key)

@client.event
async def on_reaction_add(reaction, user):
  if reaction.message.author != client.user: return
  if user == client.user: return

  global message
  
  channel_obj = message.channel
  await message.delete()
  
  keyboard.press(keys[reaction.emoji])
  time.sleep(0.25)
  
  keyboard.release(keys[reaction.emoji])
  time.sleep(2.55)

  now = int(time.time())
  pyscreenshot.grab(bbox=platform.coords()).save(f"./img/{now}.png")
  
  attachment = discord.File(f"./img/{now}.png", f"{now}.png")
  
  message = await channel_obj.send(file=attachment)  
  for key in keys.keys(): await message.add_reaction(key)

client.run("token")
