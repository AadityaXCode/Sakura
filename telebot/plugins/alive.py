import time
from datetime import datetime
import requests
from io import BytesIO
from PIL import Image

from telethon import TelegramClient
from telethon.tl.types import InputMessagesFilterPhotos
from telethon.errors.rpcerrorlist import PhotoInvalidDimensionsError
from telethon.errors import ChatSendStickersForbiddenError

from telebot import ALIVE_NAME, CMD_HELP, telever
from telebot.__init__ import StartTime
from telebot.telebotConfig import Config, Var

# ======CONSTANTS=========#
CUSTOM_ALIVE = (
    Var.CUSTOM_ALIVE
    if Var.CUSTOM_ALIVE
    else "Hey! I'm alive. All systems online and functioning normally!"
)
ALV_PIC = Var.ALIVE_PIC if Var.ALIVE_PIC else None
telemoji = Var.CUSTOM_ALIVE_EMOJI if Var.CUSTOM_ALIVE_EMOJI else "**✵**"
if Config.SUDO_USERS:
    sudo = "Enabled"
else:
    sudo = "Disabled"
# ======CONSTANTS=========#


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "@TeleBotSupport"


@telebot.on(events.NewMessage(outgoing=True, pattern=r"^\.alive"))
async def amireallyalive(alive):
    start = datetime.now()
    myid = await bot.get_me()
    """ For .alive command, check if the bot is running.  """
    end = datetime.now()
    (end - start).microseconds / 1000
    uptime = get_readable_time((time.time() - StartTime))
    if ALV_PIC:
        tele = f"**Welcome To TeleBot **\n\n"
        tele += f"`{CUSTOM_ALIVE}`\n\n"
        tele += (
            f"{telemoji} **Telethon version**: `1.34.0`\n{telemoji} **Python**: `3.10`\n"
        )
        tele += f"{telemoji} **TeleBot Version**: `{telever}`\n"
        tele += f"{telemoji} **More Info**: @TeleBotSupport\n"
        tele += f"{telemoji} **Sudo** : `{sudo}`\n"
        tele += f"{telemoji} **TeleBot Uptime**: `{uptime}`\n"
        tele += f"{telemoji} **Database Status**: `All OK 👌!`\n"
        tele += (
            f"{telemoji} **My pro owner** : [{DEFAULTUSER}](tg://user?id={myid.id})\n\n"
        )
        tele += "    [✨ GitHub Repository ✨](https://github.com/xditya/TeleBot)"
        await alive.delete()
        """ For .alive command, check if the bot is running.  """
        try:
            await alive.respond(tele)
            await bot.send_file(alive.chat_id, ALV_PIC, caption=tele, link_preview=False)
        except ChatSendStickersForbiddenError:
            await alive.respond(tele)
        return
    req = requests.get("https://telegra.ph/file/0670190de8e3bddea6d95.png")
    req.raise_for_status()
    file = BytesIO(req.content)
    file.seek(0)
    img = Image.open(file)
    with BytesIO() as sticker:
        img.save(sticker, "webp")
        sticker.name = "sticker.webp"
        sticker.seek(0)
        try:
            await bot.send_message(
                alive.chat_id,
                f"**Welcome To TeleBot **\n\n"
                f"`{CUSTOM_ALIVE}`\n\n"
                f"{telemoji} **Telethon version**: `1.34.0`\n{telemoji} **Python**: `3.10`\n"
                f"{telemoji} **TeleBot Version**: `{telever}`\n"
                f"{telemoji} **More Info**: @TeleBotSupport\n"
                f"{telemoji} **Sudo** : `{sudo}`\n"
                f"{telemoji} **TeleBot Uptime**: `{uptime}`\n"
                f"{telemoji} **Database Status**: `All OK 👌!`\n"
                f"{telemoji} **My pro owner** : [{DEFAULTUSER}](tg://user?id={myid.id})\n\n"
                "    [✨ GitHub Repository ✨](https://github.com/xditya/TeleBot)",
                link_preview=False,
            )
            await bot.send_file(alive.chat_id, file=sticker)
        except PhotoInvalidDimensionsError:
            await alive.respond(tele)
            await bot.send_file(alive.chat_id, file=sticker)
        except ChatSendStickersForbiddenError:
            await alive.respond(tele)


CMD_HELP.update({"alive": "➟ `.alive`\nUse - Check if your bot is working."})
