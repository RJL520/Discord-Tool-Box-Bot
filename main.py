import discord
from discord import Option,PermissionOverwrite,Embed
from discord.ui import View,Button
import os
from keep_alive import keep_alive

TOKEN = os.environ['TOKEN']
bot = discord.Bot()

commands= [
  ["`/role_and_channel`","Creates privates channels and corresponding roles faster\n*If both Forum channels and Stage channels fails, please check that community options are enabled on your server*"]
         ]


@bot.event
async def on_ready():
  print(f"{bot.user} is online")


@bot.slash_command(name="role_and_channel", description="Create a private channel for a specified role [role having @everyone's permissions].")
async def role_and_channel(ctx,
                           role_name:Option(str,"How will be the role named ?",required=True),
                           channel_name:Option(str,"How will be the channels named ? [default=role_name]",required=False),
                           text:Option(bool,"Do you want a text channel ?",required=False,default=False),
                           nsfw_text:Option(bool,"Should text channels be nsfw ?",required=False,default=False),
                           voice:Option(bool,"Do you want a voice channel ?",required=False,default=False),
                           forum:Option(bool,"Do you want a forum channel ?",required=False,default=False),
                           nsfw_forum:Option(bool,"Should text channels be nsfw ?",required=False,default=False),
                           stage:Option(bool,"Do you want a stage channel ?",required=False,default=False)):
  
  if channel_name == None:
    channel_name=role_name
  category = ctx.channel.category

  role= await ctx.guild.create_role(name=role_name,permissions=ctx.guild.default_role.permissions,reason=f"Created by {ctx.user} using /role_and_channel")
  
  if text:
    try:
      await ctx.guild.create_text_channel(name=channel_name,
                                          category=category,
                                          nsfw=nsfw_text,
                                          reason=f"Created by {ctx.user} using /role_and_channel",
                                          overwrites={role:PermissionOverwrite(view_channel=True),
                                                     ctx.guild.default_role:PermissionOverwrite(view_channel=False)})
    except:
      text_verify="💢"
    else:
      text_verify="✅"
  else:
    text_verify="📴"

  if voice:
    try:
      await ctx.guild.create_voice_channel(name=channel_name,
                                          category=category,
                                          reason=f"Created by {ctx.user} using /role_and_channel",
                                          overwrites={role:PermissionOverwrite(view_channel=True),
                                                     ctx.guild.default_role:PermissionOverwrite(view_channel=False)})
    except:
      voice_verify="💢"
    else:
      voice_verify="✅"
  else:
    voice_verify="📴"

  if forum:
    try:
      await ctx.guild.create_forum_channel(name=channel_name,
                                          category=category,
                                          nsfw=nsfw_forum,
                                          reason=f"Created by {ctx.user} using /role_and_channel",
                                          overwrites={role:PermissionOverwrite(view_channel=True),
                                                     ctx.guild.default_role:PermissionOverwrite(view_channel=False)})
    except:
      forum_verify="💢"
    else:
      forum_verify="✅"
  else:
    forum_verify="📴"
    
  if stage:
    try:
      await ctx.guild.create_stage_channel(name=channel_name,
                                          category=category,
                                           topic=channel_name,
                                          reason=f"Created by {ctx.user} using /role_and_channel",
                                          overwrites={role:PermissionOverwrite(view_channel=True),
                                                     ctx.guild.default_role:PermissionOverwrite(view_channel=False)})
    except:
      stage_verify="💢"
    else:
      stage_verify="✅"
  else:
    stage_verify="📴"


  await ctx.respond(embed=Embed(title="Log",description=f"Text: {text_verify}\nVoice: {voice_verify}\nForum: {forum_verify}\nStage: {stage_verify}"), ephemeral=True)

@bot.slash_command(name="help", description="Get some help !")
async def help(ctx):
  HelpEmbed = Embed(title="Help Menu",description="Get some help !")
  HelpEmbed.add_field(name="All Help",value="List of all commands and explainations",inline=False)
  HelpEmbed.add_field(name="Support server",value="Join our support server to be helped by the ones who made it !",inline=False)
  HelpEmbed.add_field(name="Invite Bot",value=f"Invite {bot.user} to your server !",inline=False)
  HelpEmbed.add_field(name="Source code",value=f"Get acess to the open source python code of {bot.user} !",inline=False)
  SuportButton = Button(label="Suport server",emoji="👾",url="https://discord.gg/7H3XTqMT4y")
  InviteButton = Button(label="Invite me !",emoji="🚀",url="https://discord.com/api/oauth2/authorize?client_id=1068940882214125699&permissions=8&scope=bot")
  SourceButton = Button(label="The code !",emoji="💻",url="https://replit.com/@jl10141516/Discord-Tool-Box-Bot?v=1")
  HelpAllButton = Button(label="All help",style=discord.ButtonStyle.green)
  
  HelpAllEmbed = Embed(title="Help Menu",description="Get some help !")
  for command in commands:
    HelpAllEmbed.add_field(name=command[0],value=command[1],inline=True)

  
  async def buttoning(ctx):
    await ctx.response.edit_message(embed=HelpAllEmbed,view=View(SuportButton,InviteButton,SourceButton))
  HelpAllButton.callback = buttoning

  
  await ctx.response.send_message(ephemeral=True,embed=HelpEmbed,view=View(HelpAllButton,SuportButton,InviteButton,SourceButton))



keep_alive()
bot.run(TOKEN)
