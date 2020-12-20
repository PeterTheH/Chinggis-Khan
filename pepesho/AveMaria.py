import random
import discord
from discord.ext import commands
import pretty_help

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="~", intents=intents, case_insensitive=True)
muted_individuals = {}
bot.remove_command("help")

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command()
@commands.has_any_role('Handcuffs (Arrest Perms)')  # NOTE: Add mod role here. Can also make a special mod list
async def jail(ctx, member: discord.Member):
    muted_role = discord.utils.get(member.guild.roles, name='Arrested (Mute)')
    if member is None:
        await ctx.send("Pass a valid user bitte")
        return
    roles = [role for role in member.roles if role.name != '@everyone']
    muted_individuals[member.display_name] = roles

    await member.remove_roles(*roles)
    await member.add_roles(muted_role)
    await ctx.send(f"{member.mention} has been sent to hell")


@bot.command()
@commands.has_any_role('Handcuffs (Arrest Perms)')
async def unjail(ctx, member: discord.Member): #muted role can be gotten from outside
    if member is None or member.display_name not in muted_individuals:
        await ctx.send("Pass a valid user bitte")
        return
    muted_role = discord.utils.get(member.guild.roles, name='Arrested (Mute)')
    roles = muted_individuals[member.display_name]
    muted_individuals.pop(member.display_name)

    await member.add_roles(*roles)
    await member.remove_roles(muted_role)
    await ctx.send(f"{member.mention} has been freed from hell")

@bot.command()
async def show_jail(ctx):
    if muted_individuals:
        await ctx.send("```" + "\n".join(muted_individuals) + "```")
    else:
        await ctx.send("Blin where is all the crime")

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Bot Commands", description="Here are the commands bröther", color=0x0088ff)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/785373357310738472/790311526791643142/1608137712164.png")
    embed.add_field(name="jail", value="Jails the treasonous scum (not for long)", inline=False)
    embed.add_field(name="unjail", value="Frees the treasonous scum ", inline=False)
    embed.add_field(name="show_jail", value="shows all the jailed traitors", inline=False)
    embed.set_footer(text="For more info ask the lazy admin swordpepi")
    await ctx.send(embed=embed)



class ChinggisKhan:
    def __init__(self):
        bot_name = bot.user.name

    @bot.event
    async def on_member_join(self, member):
        print("Recognised that a member called " + member.name + " joined")
        state = random.choice(["Balion", 'Avalon', 'Doulant'])
        role = discord.utils.get(member.guild.roles, name=state)
        await member.add_roles(role)




bot.run('BOT TOKEN')
