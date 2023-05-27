import keepalive
import pickle
import discord
from discord.ext import commands
import token

intents = discord.Intents.all()
client = commands.Bot(command_prefix="-", intents=intents)


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='Evangelion'))
    print("Bot launched")


@client.event
async def on_raw_reaction_add(payload):
    print('Nouvelle reaction')
    membre=payload.member
    guild=membre.guild
    user=client.get_user(payload.user_id)
    print(str(membre.name) + ' a déréagit avec : ' + str(payload.emoji))
    if user is None:  # Maybe the user isn't cached?
        user = await client.fetch_user(payload.user_id)
    channel=discord.utils.get(guild.channels, id=payload.channel_id)
    if payload.message_id == 954073980128591872 and str(payload.emoji) == "🔻":
        print('Le role : ' + str(discord.utils.get(guild.roles, id=951532125532880956).name) + ' va lui etre ajouté')
        await membre.add_roles(discord.utils.get(guild.roles, id=951532125532880956))
        print('Réussi\n')

@client.event
async def on_raw_reaction_remove(payload):
    print('Nouvelle déreaction')
    guild = await client.fetch_guild(payload.guild_id)
    membre = await guild.fetch_member(payload.user_id)
    user=client.get_user(payload.user_id)
    if user is None:  # Maybe the user isn't cached?
        user = await client.fetch_user(payload.user_id)
    print(str(membre.name) + ' a déréagit avec : ' + str(payload.emoji))
    if payload.message_id == 954073980128591872 and str(payload.emoji) == "🔻":
        print('Le role : ' + str(discord.utils.get(guild.roles, id=951532125532880956).name) + ' va lui etre retiré')
        await membre.remove_roles(discord.utils.get(guild.roles, id=951532125532880956))
        print('Réussi\n')




@client.command()
async def hello(ctx, arg):
    await ctx.send(arg)


@client.command()
async def aide(ctx):
    embed = discord.Embed(
        title='Aide',
        description="Liste des commandes",
        color=discord.Color.blurple()
    )
    embed.add_field(name="Préfixe", value="Toutes les commandees commencent par le préfixe \"-\"", inline=True)
    embed.add_field(name="-points", value="Si une personne est mentionnée directemet après, cela donne le nombre de points de cette personne, sinon cela renvoie les tiens", inline=True)
    embed.add_field(name="-serveur", value="Affiche plein d'infos sur le serveur", inline=True)
    rolemodo = discord.utils.get(ctx.guild.roles, name="Modérateur")
    rolesecr = discord.utils.get(ctx.guild.roles, name="Secrétaire")
    roleadmin = discord.utils.get(ctx.guild.roles, name="Admin")
    if rolemodo in ctx.message.author.roles or rolesecr in ctx.message.author.roles or roleadmin in ctx.message.author.roles:
        embed.add_field(name="-purge", value="Supprime le nombre de message donné après (la commande non incluse)",
                        inline=True)
        embed.add_field(name="-set mention(s) nb", value="Met les points de la/les mention(s) à nb", inline=True)
        embed.add_field(name="-add mention(s) nb", value="Ajoute nb points à la mention", inline=True)
    await ctx.send(embed=embed)

@client.command()
async def echo(ctx, *args):
    for arg in args:
        await ctx.send(arg)

@client.command()
async def purge(ctx, arg):
    rolemodo = discord.utils.get(ctx.guild.roles, name="Modérateur")
    rolesecr = discord.utils.get(ctx.guild.roles, name="Secrétaire")
    roleadmin = discord.utils.get(ctx.guild.roles, name="Admin")
    if rolemodo in ctx.message.author.roles or rolesecr in ctx.message.author.roles or roleadmin in ctx.message.author.roles:
        await ctx.channel.purge(limit=int(arg))
    else:
        await ctx.channel.send("Vous n'avez pas la permission de faire cela")

@client.command()
async def add(ctx, *args):
    with open('donnees','rb') as donnees:
        fulldata=pickle.load(donnees)
    lipoints=fulldata[0]
    rolemodo = discord.utils.get(ctx.guild.roles, name="Modérateur")
    rolesecr = discord.utils.get(ctx.guild.roles, name="Secrétaire")
    roleadmin = discord.utils.get(ctx.guild.roles, name="Admin")
    if rolemodo in ctx.message.author.roles or rolesecr in ctx.message.author.roles or roleadmin in ctx.message.author.roles:
        valeur=int(args[-1])
        limentionnes=ctx.message.mentions
        for personne in limentionnes:
            a_points=False
            for elt in lipoints:
                if elt[0]==int(personne.id):
                    a_points=True
                    elt[1]+=valeur
                    print('ajout de ' + str(valeur) + ' points à ' + personne.name)
                    break
            if not(a_points):
                print('nouvelle personne ' + personne.name + ' a obtenu ' + str(valeur) +' points')
                lipoints.append([personne.id, valeur])
            await ctx.channel.send(str(valeur) + ' points ont été donnés à ' + personne.name)
    else:
        await ctx.channel.send("Vous n'avez pas la permission de faire cela")
    fulldata[0]=lipoints
    with open('donnees','wb') as donnees:
        pickle.dump(fulldata, donnees)

@client.command()
async def set(ctx, *args):
    with open('donnees','rb') as donnees:
        fulldata=pickle.load(donnees)
    lipoints=fulldata[0]
    rolemodo = discord.utils.get(ctx.guild.roles, name="Modérateur")
    rolesecr = discord.utils.get(ctx.guild.roles, name="Secrétaire")
    roleadmin = discord.utils.get(ctx.guild.roles, name="Admin")
    if rolemodo in ctx.message.author.roles or rolesecr in ctx.message.author.roles or roleadmin in ctx.message.author.roles:
        valeur=int(args[-1])
        limentionnes=ctx.message.mentions
        for personne in limentionnes:
            a_points=False
            for elt in lipoints:
                if elt[0]==int(personne.id):
                    a_points=True
                    elt[1]=valeur
                    print('Le membre ' + personne.name + ' a maintenant ' + str(valeur) + ' points.')
                    break
            if not(a_points):
                print('nouvelle personne ' + personne.name + ' a obtenu ' + str(valeur) +' points')
                lipoints.append([int(personne.id), valeur])
            await ctx.channel.send(personne.name + ' a maintenant ' + str(valeur) + ' points' )
    else:
        await ctx.channel.send("Vous n'avez pas la permission de faire cela")
    fulldata[0] = lipoints
    with open('donnees', 'wb') as donnees:
        pickle.dump(fulldata, donnees)


@client.command()
async def points(ctx):
    with open('donnees','rb') as donnees:
        fulldata=pickle.load(donnees)
    lipoints=fulldata[0]
    if ctx.message.mentions==[]:
        personne=ctx.message.author
    else:
        personne=ctx.message.mentions[0]
    apoints=False
    for elt in lipoints:
        if elt[0] == int(personne.id):
            await ctx.channel.send("Le membre "+ str(personne.name) +' a ' + str(elt[1]) + ' points!')
            apoints=True
            break
    if not(apoints):
        await ctx.channel.send('Le membre ' + str(personne.name) + ' n\'a pas encore de points')
    fulldata[0] = lipoints
    with open('donnees', 'wb') as donnees:
        pickle.dump(fulldata, donnees)






@client.command()
async def serveur(ctx):
    nom = str(ctx.guild.name)
    description = str(ctx.guild.description)
    owner = str(ctx.guild.owner)
    id = str(ctx.guild.id)
    region = str(ctx.guild.region)
    membercount = str(ctx.guild.member_count)
    icon = str(ctx.guild.icon_url)
    creation=str(ctx.guild.created_at)[:10]
    #banner = str(ctx.guild.banner_url)
    print('1')
    embed = discord.Embed(
        title='Le serveur : '+ nom,
        description="Informations sur le serveur",
        color=discord.Color.blurple()
    )
    print(icon)
    embed.set_thumbnail(url=icon)
    print('3')

    #embed.add_field(name="Bannière", value=banner, inline=True)

    embed.add_field(name="Propriétaire", value=owner, inline=True)
    embed.add_field(name="Id serveur", value=id, inline=True)
    embed.add_field(name="Date de création", value=creation, inline=True)
    embed.add_field(name="Nombre de membres", value=membercount, inline=True)
    print('5')
    await ctx.send(embed=embed)

keepalive.keep_alive()

client.run(token.token)