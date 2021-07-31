import sys
import json
import os
import asyncio
import requests
import discord
from discord.ext.commands import cooldown, BucketType
from mojang import MojangAPI
from discord.ext import commands, tasks
from discord import colour
import sqlite3
import datetime
from datetime import date
from datetime import datetime
import pytz
from discord import Embed
from functools import lru_cache
import threading
from natsort import natsorted, ns, humansorted
import schedule
import time
import asyncio
import aioschedule as schedule

bot = commands.Bot(command_prefix="!")
bot.remove_command("help")

conn = sqlite3.connect('bedwars.db')
cursor = conn.cursor()
cursor.execute( """CREATE TABLE IF NOT EXISTS bwexp(exp_before REAL, games_played REAL)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS igns(ign TEXT type UNIQUE, uuid BLOB type UNIQUE)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS expnow(exp_current REAL, games_now REAL)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS bedwars(event_or_no TEXT, date_started REAL, date_ending REAL, runtime REAL)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS prize(prizes BLOB)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS ended(end TEXT)""")
cursor.close()
conn.close()

guild_api = 'https://api.hypixel.net/guild?key=eba433ff-c57e-48ce-ade9-242242be49f9&name=stormfall'
key = 'eba433ff-c57e-48ce-ade9-242242be49f9'


token = token


@tasks.loop(hours=24.0)
async def event_end():
    channel = bot.get_channel(756177435032158294)
    conn = sqlite3.connect('bedwars.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ended(end) VALUES (1)")
    conn.commit()
        
    ign = cursor.execute("SELECT ign from igns").fetchall()
    pastexp = cursor.execute("SELECT exp_before from bwexp").fetchall()
    desc = []
    for member, exp in zip(ign, pastexp):
        str = f'{member}'
        print("MEMBER = ", str)
        split = str.strip("'(),")
        user = MojangAPI.get_uuid(split)
        name = MojangAPI.get_username(user)
        data = requests.get(f'https://api.hypixel.net/player?key={key}&uuid={user}').json()
        bwexp = data["player"]["stats"]["Bedwars"]["Experience"]
        print("BWEXP NOW = ", bwexp)
        str = f"{exp}"
        sp = str.strip("()',")
        print("EXP before = ", sp)
        expnow = int(bwexp) - int(float(sp))
        print("BWEXP AFTER DEDUCTION = ", expnow)
        if expnow == 0:
            continue
        else:
            bam = f'{expnow} - {name}'
            desc.append(bam)
            print(bam)
    else:
        sorted = natsorted(desc)
        first = ""
        second = ""
        third = ""
        fourth = ""
        fifth = ""
        sixth = ""
        seventh = ""
        eigth = ""
        ninth = ""
        tenth = ""
        for place in range(1, 11):    
            try:
                a = sorted[-place]
                aa = f"{a}"
                index = aa.index('-')
                aaaa = aa[:index] # exp lang matitira
                aaa = aa[1 + index:] # name lang matitira
                if place == 1:
                    first += f"**{aaa}** with {aaaa} XP gained"
                if place == 2:
                    second += f"**{aaa}** with {aaaa} XP gained"
                if place == 3:
                    third += f"**{aaa}** with {aaaa} XP gained"
                if place == 4:
                    fourth += f"**{aaa}** with {aaaa} XP gained"
                if place == 5:
                    fifth += f"**{aaa}** with {aaaa} XP gained"
                if place == 6:
                    sixth += f"**{aaa}** with {aaaa} XP gained"
                if place == 7:
                    seventh += f"**{aaa}** with {aaaa} XP gained"
                if place == 8:
                    eigth += f"**{aaa}** with {aaaa} XP gained"
                if place == 9:
                    ninth += f"**{aaa}** with {aaaa} XP gained"
                if place == 10:
                    tenth += f"**{aaa}** with {aaaa} XP gained"
            except IndexError:
                a = "None"
                if place == 1:
                    first += f"{a}"
                if place == 2:
                    second += f"{a}"
                if place == 3:
                    third += f"{a}"
                if place == 4:
                    fourth += f"{a}"
                if place == 5:
                    fifth += f"{a}"
                if place == 6:
                    sixth += f"{a}"
                if place == 7:
                    seventh += f"{a}"
                if place == 8:
                    eigth += f"{a}"
                if place == 9:
                    ninth += f"{a}"
                if place == 10:
                    tenth += f"{a}"
        
        s = bot.get_emoji(835509985169244190)
        t = bot.get_emoji(835510792450474014)
        o = bot.get_emoji(835510792349679626)
        r = bot.get_emoji(835510792392015883)
        m = bot.get_emoji(835510792417706025)
        f = bot.get_emoji(835510792395816991)
        a = bot.get_emoji(835510792441954325)
        l = bot.get_emoji(835511308958957639)
        b = bot.get_emoji(835510792370782208)
        w = bot.get_emoji(835510792299610123)
        e = bot.get_emoji(835510792543535124)
        v = bot.get_emoji(835510792416788510)
        n = bot.get_emoji(835510792429371402)
        fire = bot.get_emoji(835518981674631219)
        em = bot.get_emoji(741496412352544801)
        desc = f"Here are the Final Top 10!\n🥇 {first}\n🥈 {second}\n🥉 {third}\n\n``#4`` {fourth}\n``#5`` {fifth}\n``#6`` {sixth}\n``#7`` {seventh}\n``#8`` {eigth}\n``#9`` {ninth}\n``#10`` {tenth}\n\nCongratulations on winning the event! {em}"
        embed = discord.Embed(title = f"After hours of grinding, the BedWars event has concluded!",
                            url='https://www.hypixel.net/threads/3340014/',
                            description = desc)
        await channel.send(f"───────────────────────────────────────────\n"
        f"   {fire} {s}{t}{o}{r}{m}{f}{a}{l}{l}     {b}{w}{s}     {e}{v}{e}{n}{t} {fire}\n"
        "───────────────────────────────────────────", embed=embed)

        cursor.close()
        conn.close()

async def player_is_in_guild(guild: dict, uuid: str) -> bool:
    for member in guild["guild"]["members"]:
        if member["uuid"] == uuid:
            return True
    return False

@bot.event
async def on_ready():
    print("Bot is online!")

@bot.command()
async def addprize(ctx, *args):
    conn = sqlite3.connect('bedwars.db')
    c = conn.cursor()
    joined = " ".join(args[:])
    c.execute("""INSERT INTO prize(prizes) VALUES (?)""", (joined,))
    conn.commit()
    c.close()
    conn.close()
    print(joined)
    await ctx.send("Bedwars Prizes has been added into the database!")

@bot.command()
@commands.has_permissions(administrator=True)
async def bwstart(ctx, hours):
    ping = '757411587006005401'
    # check kung may on-going event
    conn = sqlite3.connect('bedwars.db')
    c = conn.cursor()
    query = """SELECT event_or_no from bedwars"""
    c.execute(query)
    fetch = c.fetchall()
    feech = len(fetch)
    c.close()
    conn.close()
    # may on going event
    if feech > 0:
        await ctx.send(f'There is already an event on going!')
    # walang on going event
    if feech == 0:
        # GET THE CURRENT DATE AND TIME
        current = datetime.utcnow()
        timestampnow = datetime.timestamp(current)  # timestamp nung current variable
        htos= float(hours) * 3600  # change into seconds ung hours na magrrun ung event

        # ADD H-TO-S TO TIMESTAMPNOW
        ending_timestamp = timestampnow + htos  # kung kelan magtatapos ang event
        ending_date = datetime.fromtimestamp(ending_timestamp)

        # PUT THE DATE VALUES INTO THE DATABASE
        datequery = """INSERT into bedwars(date_started, date_ending, runtime) VALUES (?, ?, ?)"""
        values = (current, ending_date, hours)

        # ADD 1 VALUE TO EVENT_OR_NO DATABASE SO THE SYSTEM WILL FIGURE OUT IF THERE'S AN EVENT RUNNING OR NOT
        conn = sqlite3.connect('bedwars.db')
        c = conn.cursor()
        event_started = """INSERT into bedwars(event_or_no) VALUES (1)"""
        c.execute(datequery, values)
        c.execute(event_started)
        conn.commit()
        # CHANGE DATE FORMAT so we can send
        end = ending_date.strftime('%B %d %Y,  at %I:%M UTC')
        # GET THE BEDWARS XP OF THE REGISTERED PLAYERS
        query = """SELECT ign from igns"""
        c.execute(query)
        fetch = c.fetchall()
        bwx = ""
        print(fetch)
        for member in fetch:
            str = f'{member}'
            split = str.strip("'(),")
            user = MojangAPI.get_uuid(split)
            name = MojangAPI.get_username(user)
            data = requests.get(f'https://api.hypixel.net/player?key={key}&uuid={user}').json()
            bwexp = data["player"]["stats"]["Bedwars"]["Experience"]
            bwgames = data["player"]["stats"]["Bedwars"]["games_played_bedwars"]
            # STORE THE STARTING BEDWARS EXP
            store = """INSERT INTO bwexp(exp_before, games_played) VALUES (?, ?)"""
            st = (bwexp, bwgames)
            c.execute(store, st)
            conn.commit()
        print(bwx)

        # Send info that the event has started
            
        s = bot.get_emoji(835509985169244190)
        t = bot.get_emoji(835510792450474014)
        o = bot.get_emoji(835510792349679626)
        r = bot.get_emoji(835510792392015883)
        m = bot.get_emoji(835510792417706025)
        f = bot.get_emoji(835510792395816991)
        a = bot.get_emoji(835510792441954325)
        l = bot.get_emoji(835511308958957639)
        b = bot.get_emoji(835510792370782208)
        w = bot.get_emoji(835510792299610123)
        e = bot.get_emoji(835510792543535124)
        v = bot.get_emoji(835510792416788510)
        n = bot.get_emoji(835510792429371402)
        fire = bot.get_emoji(835518981674631219)
        # GET PRIZES
        prize = """SELECT prizes from prize"""
        c.execute(prize)
        get = c.fetchone()
        str = f"{get}"
        spl = str.strip("()'',")
        print(spl)

        embed = discord.Embed(title="**The Bedwars XP Event has started!**", 
                              url = "https://www.hypixel.net/threads/3340014/",
                              description = f"Recap of the Event Details:",
                              color = discord.Colour.dark_gold())
        embed.add_field(name=f"Runtime", value=f"**`{hours}` hour(s)** _ _ _ _",inline=True)
        embed.add_field(name=f"Ending Date", value=f"**`{end}`**")
        embed.add_field(name=f"Prizes", value = f"{spl}", inline=False)
        embed.timestamp = ending_date
        embed.set_footer(text=f"Event ending time in your timezone -> ")
        embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/835756938746265601.gif?v=1')
        await ctx.send(f"───────────────────────────────────────────\n"
        f"   {fire} {s}{t}{o}{r}{m}{f}{a}{l}{l}     {b}{w}{s}     {e}{v}{e}{n}{t} {fire}\n"
        "───────────────────────────────────────────", embed=embed)

        await event_end.start()

        c.close()
        conn.close()

@bot.command()
async def cancel(ctx):
    schedule.clear()
    await ctx.send("All jobs canceled.")
@bot.command()
async def reset(ctx):
    msg = await ctx.send('Deleting data...')
    inac = sqlite3.connect('bedwars.db')
    cursor = inac.cursor()
    cursor.execute("""DELETE from prize""")
    cursor.execute("""DELETE from bedwars""")
    cursor.execute("""DELETE from bwexp""")
    cursor.execute("""DELETE from igns""")
    cursor.execute("""DELETE from ended""")
    inac.commit()
    await msg.edit(content=f'Data deleted! Table is now empty.')
    cursor.close()
    inac.close()



@lru_cache(maxsize=5)
@bot.command()
async def bwleaderboards(ctx):
    msg = await ctx.send(f'Gathering information...')
    desc = []
    # GET IGNS
    conn = sqlite3.connect('bedwars.db')
    cursor = conn.cursor()
    ended = cursor.execute("SELECT end from ended").fetchall()
    ends = len(ended)
    if ends > 0:
        await msg.edit(content = "The event has ended! Please check #general for the final leaderboard instead!")
    else:
        ign = cursor.execute("SELECT ign from igns").fetchall()
        pastexp = cursor.execute("SELECT exp_before from bwexp").fetchall()
        try:
            for member, exp in zip(ign, pastexp):
                str = f'{member}'
                print("MEMBER = ", str)
                split = str.strip("'(),")
                user = MojangAPI.get_uuid(split)
                name = MojangAPI.get_username(user)
                data = requests.get(f'https://api.hypixel.net/player?key={key}&uuid={user}').json()
                bwexp = data["player"]["stats"]["Bedwars"]["Experience"]
                print("BWEXP NOW = ", bwexp)
                str = f"{exp}"
                sp = str.strip("()',")
                print("EXP before = ", sp)
                expnow = int(bwexp) - int(float(sp))
                print("BWEXP AFTER DEDUCTION = ", expnow, "\n")
                if expnow == 0:
                    continue
                else:
                    bam = f'{expnow}-{name}'
                    desc.append(bam)
                    print(bam)
        except JSONDecodeError:
            await msg.edit(content="Please wait a second before running this command again! API Ratelimit error reached :D")
        if len(desc) == 0:
            await msg.edit(content = "There's no one in the leaderboards yet!")
        else:
            sorted = natsorted(desc)
            first = ""
            second = ""
            third = ""
            fourth = ""
            fifth = ""
            sixth = ""
            seventh = ""
            eigth = ""
            ninth = ""
            tenth = ""
            for place in range(1, 11):    
                try:
                    a = sorted[-place]
                    aa = f"{a}"
                    index = aa.index('-')
                    aaaa = aa[:index] # exp lang matitira
                    aaa = aa[1 + index:] # name lang matitira
                    if place == 1:
                        first += f"**{aaa}** with {aaaa} XP gained"
                    if place == 2:
                        second += f"**{aaa}** with {aaaa} XP gained"
                    if place == 3:
                        third += f"**{aaa}** with {aaaa} XP gained"
                    if place == 4:
                        fourth += f"**{aaa}** with {aaaa} XP gained"
                    if place == 5:
                        fifth += f"**{aaa}** with {aaaa} XP gained"
                    if place == 6:
                        sixth += f"**{aaa}** with {aaaa} XP gained"
                    if place == 7:
                        seventh += f"**{aaa}** with {aaaa} XP gained"
                    if place == 8:
                        eigth += f"**{aaa}** with {aaaa} XP gained"
                    if place == 9:
                        ninth += f"**{aaa}** with {aaaa} XP gained"
                    if place == 10:
                        tenth += f"**{aaa}** with {aaaa} XP gained"
                except IndexError:
                    a = "None"
                    if place == 1:
                        first += f"{a}"
                    if place == 2:
                        second += f"{a}"
                    if place == 3:
                        third += f"{a}"
                    if place == 4:
                        fourth += f"{a}"
                    if place == 5:
                        fifth += f"{a}"
                    if place == 6:
                        sixth += f"{a}"
                    if place == 7:
                        seventh += f"{a}"
                    if place == 8:
                        eigth += f"{a}"
                    if place == 9:
                        ninth += f"{a}"
                    if place == 10:
                        tenth += f"{a}"
            
            # get first place uuid for embed thumbnail
            
            rep = first.replace("**", "")
            ind = rep.index(' ')
            nam = rep[:ind] # name lang matitira
            uuid = MojangAPI.get_uuid(nam)
            print("name = ", nam)
            print("uuid = ", uuid)

            desc = f"\n🥇 {first}\n🥈 {second}\n🥉 {third}\n\n``#4`` {fourth}\n``#5`` {fifth}\n``#6`` {sixth}\n``#7`` {seventh}\n``#8`` {eigth}\n``#9`` {ninth}\n``#10`` {tenth}\n"
            embed = discord.Embed(title = f"**StormFall Bedwars Top 10 Leaderboard**", 
                                url = "https://www.hypixel.net/threads/3340014/",
                                description = desc, color = discord.Colour.dark_gold())
            embed.set_thumbnail(url=f'https://crafatar.com/renders/body/{uuid}')

            now = datetime.now(pytz.timezone('US/Eastern'))
            dt_string = now.strftime("%b %d %Y, %H:%M:%S %Z")
            embed.set_footer(text=f"As of {dt_string}")
            await msg.edit(embed=embed)
    cursor.close()
    conn.close()


@bot.command()
async def bwregister(ctx, ign):
    # CHECK WHETHER OR NOT AN EVENT IS RUNNING
    msg = await ctx.send(f'Gimme a second... (1/2)')
    conn = sqlite3.connect('bedwars.db')
    c = conn.cursor()
    check = """SELECT event_or_no from bedwars"""
    c.execute(check)
    fetch = c.fetchall()
    feech = len(fetch)
    c.close()
    conn.close()
    # EVENT IS RUNNING
    if feech > 0:
        await msg.edit(content = f"{ctx.author.mention}, you can't register into the event whilst it already is running! Sorry!")

    # EVENT IS NOT RUNNING
    if feech == 0:
        await msg.edit(content = 'Processing information.. (2/2)')

        # CHECK IF IGN IS REAL & CORRECT
        uuid = MojangAPI.get_uuid(ign)
        username = MojangAPI.get_username(uuid)
        print(username)
        if not uuid:
            await msg.edit(
                content=f'{ctx.author.mention}, the IGN does not exist! Please register again.')  # ign does not exist

        else:  # ign exists
            # CHECK IF IGN IS IN THE GUILD
            guild = requests.get(guild_api).json()  # get guild api

            if ign is not None:  # ign is not in guild
                conn = sqlite3.connect('bedwars.db')
                c = conn.cursor()
                try:
                    store = "INSERT INTO igns (ign, uuid) VALUES (?, ?)"
                    a = (username, uuid)
                    c.execute(store, a)
                    conn.commit()
                    c.close()
                    conn.close()
                    await msg.edit(content=f'{ctx.author.mention}, you have successfully registered in the event!')
                except sqlite3.Error as e:
                    await msg.edit(content=f'{ctx.author.mention}, you have already entered in the event!')

@tasks.loop(minutes=1)
async def loopcmd():
    channel = bot.get_channel(756177435032158292)
    print(f"Started at {datetime.now()}")
    await channel.send(f"Started at {datetime.now()}")
@bot.command()
async def testcmd(ctx):
    await ctx.send("Starting the loop in 60 seconds")
    loopcmd.start()
        
bot.run(token)
