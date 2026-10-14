import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import subprocess
import socket
import urllib.request
import time

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Autentificarea a avut loc cu succes! {bot.user} este pregatit pentru utilizare.')

@bot.command(name='ping-ip')
async def ping_ip(ctx, ip_address: str):
    if not ctx.author.guild_permissions.administrator:
        return
    
    message = await ctx.send(embed=discord.Embed(title="📡 Ping in desfasurare...", color=discord.Color.orange()))

    try:
        result = subprocess.run(['ping', '-c', '4', ip_address], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            statistici = '\n'.join(result.stdout.split('\n')[-3:])
            embed = discord.Embed(title=f"✅ Rezultat Ping: {ip_address}", color=discord.Color.green())
            embed.add_field(name="Statistici Rețea", value=f"```\n{statistici}\n```", inline=False)
            await message.edit(embed=embed)
        else:
            await message.edit(embed=discord.Embed(title=f"❌ Host Inaccesibil: {ip_address}", color=discord.Color.red()))
    except Exception as e:
        pass

@bot.command(name='check-port')
async def check_port(ctx, ip_address: str, port: int):
    if not ctx.author.guild_permissions.administrator:
        return
    
    message = await ctx.send(embed=discord.Embed(title=f"🔍 Scanez portul {port}...", color=discord.Color.orange()))
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        rezultat = sock.connect_ex((ip_address, port))
        sock.close()
        
        if rezultat == 0:
            embed = discord.Embed(title=f"🔓 Port Deschis: {port}", description=f"Host: `{ip_address}`", color=discord.Color.green())
        else:
            embed = discord.Embed(title=f"🔒 Port Închis / Filtrat: {port}", description=f"Host: `{ip_address}`", color=discord.Color.red())
            
        await message.edit(embed=embed)
    except Exception as e:
        await message.edit(embed=discord.Embed(title="⚠️ Eroare Socket", description=str(e), color=discord.Color.dark_red()))

@bot.command(name='http')
async def check_http(ctx, url: str):
    if not ctx.author.guild_permissions.administrator:
        return
        
    if not url.startswith('http'):
        url = 'https://' + url
        
    message = await ctx.send(embed=discord.Embed(title="🌐 Verific website-ul...", color=discord.Color.orange()))
    
    start_time = time.time()
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}
        req = urllib.request.Request(url, headers=headers)
        
        raspuns = urllib.request.urlopen(req, timeout=5)
        cod_status = raspuns.getcode()
        
        timp_raspuns = int((time.time() - start_time) * 1000) 
        
        embed = discord.Embed(title=f"✅ Site Online: {url}", color=discord.Color.green())
        embed.add_field(name="Cod HTTP", value=f"`{cod_status} OK`", inline=True)
        embed.add_field(name="Timp de răspuns", value=f"`{timp_raspuns} ms`", inline=True)
        await message.edit(embed=embed)
        
    except urllib.error.URLError as e:
        embed = discord.Embed(title=f"❌ Site Offline: {url}", color=discord.Color.red())
        if hasattr(e, 'code'):
            embed.add_field(name="Cod Eroare", value=f"`{e.code}`", inline=True)
        embed.add_field(name="Motiv", value=f"`{e.reason}`", inline=False)
        await message.edit(embed=embed)

bot.run(TOKEN)