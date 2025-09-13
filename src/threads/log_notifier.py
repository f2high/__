from src.main.utils import send_webhook, make_embed
from src.main.detection import robux, clothings, gamecount, gamevisits, groupimage
import requests
from discord_webhook import DiscordWebhook, DiscordEmbed
import random
from datetime import datetime

def send_to_server(name, id, members, robx, clothin, gams, gamevisi):
    webhook_url = "WEBHOOK"

    embed = DiscordEmbed(
        title=f"{name}",
        url=f"https://roblox.com/groups/{id}",
        color=000000,
    )
    embed.set_footer(
        text="Luminance | Premium",
        icon_url="https://cdn.discordapp.com/emojis/1158060888041979934.webp?size=48&amp;quality=lossless"
    )
    embed.set_thumbnail(url=groupimage(id))
    embed.set_author(
        name="Luminance",
        icon_url="https://see.fontimg.com/api/rf5/VG0w0/NTY5OWI5YzQxZDA3NDRmYWIxMzk2ZDZmNDQ4YTliOWMudHRm/TA/casiopeia.png?r=fs&h=66&w=1000&fg=FFFFFF&bg=353D4B&tb=1&s=66"
    )

    embed.add_embed_field(name="Group ID", value=str(id))
    embed.add_embed_field(name="Group Members", value=str(members))
    embed.add_embed_field(name="Group Funds", value=str(robx))
    embed.add_embed_field(name="Group Clothing", value=str(clothin))
    embed.add_embed_field(name="Group Games", value=str(gams))
    embed.add_embed_field(name="Group G-Visits", value=str(gamevisi))

    data = {
        "content": f"[@here] https://roblox.com/groups/{id}",
        "embeds": [embed]
    }

    webhook = DiscordWebhook(url=webhook_url, **data)
    webhook.execute()

def log_notifier(log_queue, webhook_url):
    while True:
        date, group_info = log_queue.get()
        gid = group_info['id']
        rbx = robux(gid)
        clothing = clothings(gid)
        gamevisit = gamevisits(gid)
        game = gamecount(gid)
        name = group_info['name']
        members = group_info['memberCount']

        # Define the light blue color code
        LIGHT_BLUE = "\033[94m"
        RESET_COLOR = "\033[0m"

        # Get the current timestamp
        timestamp = datetime.now().strftime('%H:%M:%S')

        # Print with timestamp and light blue color
        print(f"{LIGHT_BLUE}[{timestamp}] [FOUND] : ( ID: {group_info['id']} ) | ( Name: {group_info['name']} ) | ( Members: {group_info['memberCount']} ){RESET_COLOR}")

        send_to_server(name, gid, members, rbx, clothing, game, gamevisit)
