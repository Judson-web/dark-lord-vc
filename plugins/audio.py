import os
import re
import sys
import ffmpeg
import asyncio
import subprocess
from asyncio import sleep
from pyrogram import Client, filters
from pyrogram.types import Message
from helpers.bot_utils import USERNAME
from config import AUDIO_CALL, VIDEO_CALL
from plugins.video import ydl, group_call
from helpers.decorators import authorized_users_only, sudo_users_only
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery


@Client.on_message(filters.command(["play", f"play@{USERNAME}"]) & filters.group & ~filters.edited)
@authorized_users_only
async def play(client, m: Message):
    msg = await m.reply_text("🔄 `Pʀᴏᴄᴇssɪɴɢ ...`")
    chat_id = m.chat.id
    media = m.reply_to_message
    if not media and not ' ' in m.text:
        await msg.edit("❗ __Sᴇɴᴅ Mᴇ Aɴ Lɪᴠᴇ Sᴛʀᴇᴀᴍ Lɪɴᴋ / YᴏᴜTᴜʙᴇ Vɪᴅᴇᴏ Lɪɴᴋ / Rᴇᴘʟʏ Tᴏ Aɴ Vɪᴅᴇᴏ Tᴏ Sᴛᴀʀᴛ Vɪᴅᴇᴏ Sᴛʀᴇᴀᴍɪɴɢ!__")

    elif ' ' in m.text:
        text = m.text.split(' ', 1)
        query = text[1]
        if not 'http' in query:
            return await msg.edit("❗ __Sᴇɴᴅ Mᴇ Aɴ Lɪᴠᴇ Sᴛʀᴇᴀᴍ Lɪɴᴋ / YᴏᴜTᴜʙᴇ Vɪᴅᴇᴏ Lɪɴᴋ / Rᴇᴘʟʏ Tᴏ Aɴ Vɪᴅᴇᴏ Tᴏ Sᴛᴀʀᴛ Vɪᴅᴇᴏ Sᴛʀᴇᴀᴍɪɴɢ!__")
        regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
        match = re.match(regex, query)
        if match:
            await msg.edit("🔄 `Sᴛᴀʀᴛɪɴɢ YᴏᴜTᴜʙᴇ Aᴜᴅɪᴏ Sᴛʀᴇᴀᴍ ...`")
            try:
                meta = ydl.extract_info(query, download=False)
                formats = meta.get('formats', [meta])
                for f in formats:
                    ytstreamlink = f['url']
                link = ytstreamlink
            except Exception as e:
                return await msg.edit(f"❌ **YᴏᴜTᴜʙᴇ Dᴏᴡɴʟᴏᴀᴅ Eʀʀᴏʀ !** \n\n`{e}`")
                print(e)

        else:
            await msg.edit("🔄 `Sᴛᴀʀᴛɪɴɢ YᴏᴜTᴜʙᴇ Aᴜᴅɪᴏ Sᴛʀᴇᴀᴍ ...`")
            link = query

        vid_call = VIDEO_CALL.get(chat_id)
        if vid_call:
            await VIDEO_CALL[chat_id].stop()
            VIDEO_CALL.pop(chat_id)
            await sleep(3)

        aud_call = AUDIO_CALL.get(chat_id)
        if aud_call:
            await AUDIO_CALL[chat_id].stop()
            AUDIO_CALL.pop(chat_id)
            await sleep(3)

        try:
            await sleep(2)
            await group_call.join(chat_id)
            await group_call.start_audio(link, repeat=False)
            AUDIO_CALL[chat_id] = group_call
            await msg.delete()
            await m.reply_text(f"▶️ **Started [Audio Streaming]({query}) In {m.chat.title} !**",
               reply_markup=InlineKeyboardMarkup(
               [
                   [
                       InlineKeyboardButton(
                          text="⏸",
                          callback_data="pause_callback",
                       ),
                       InlineKeyboardButton(
                          text="▶️",
                          callback_data="resume_callback",
                       ),
                       InlineKeyboardButton(
                          text="⏹️",
                          callback_data="end_callback",
                       ),
                   ],
               ]),
            )
        except Exception as e:
            await msg.edit(f"❌ **Eʀʀᴏʀ Oᴄᴄᴏᴜʀᴇᴅ  !** \n\nError: `{e}`")
            return await group_call.stop()

    elif media.audio or media.document:
        await msg.edit("🔄 `Dᴏᴡɴʟᴏᴀᴅɪɴɢ ...`")
        audio = await client.download_media(media)

        vid_call = VIDEO_CALL.get(chat_id)
        if vid_call:
            await VIDEO_CALL[chat_id].stop()
            VIDEO_CALL.pop(chat_id)
            await sleep(3)

        aud_call = AUDIO_CALL.get(chat_id)
        if aud_call:
            await AUDIO_CALL[chat_id].stop()
            AUDIO_CALL.pop(chat_id)
            await sleep(3)

        try:
            await sleep(2)
            await group_call.join(chat_id)
            await group_call.start_audio(audio, repeat=False)
            AUDIO_CALL[chat_id] = group_call
            await msg.delete()
            await m.reply_text(f"▶️ **Sᴛᴀʀᴛᴇᴅ [Aᴜᴅɪᴏ Sᴛʀᴇᴀᴍɪɴɢ](telegram.me/VAMPIRE_KING_NO_1) Iɴ {m.chat.title} !**",
               reply_markup=InlineKeyboardMarkup(
               [
                   [
                       InlineKeyboardButton(
                          text="⏸",
                          callback_data="pause_callback",
                       ),
                       InlineKeyboardButton(
                          text="▶️",
                          callback_data="resume_callback",
                       ),
                       InlineKeyboardButton(
                          text="⏹️",
                          callback_data="end_callback",
                       ),
                   ],
               ]),
            )
        except Exception as e:
            await msg.edit(f"❌ Aɴ **Eʀʀᴏʀ Oᴄᴄᴏᴜʀᴇᴅ !** \n\nError: `{e}`")
            return await group_call.stop()

    else:
        await msg.edit(
            "💁🏻‍♂️ Dᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ sᴇᴀʀᴄʜ ғᴏʀ ᴀ YᴏᴜTᴜʙᴇ sᴏɴɢ?",
            reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "✅ Yᴇs", switch_inline_query_current_chat=""
                    ),
                    InlineKeyboardButton(
                        "ɴᴏ ❌", callback_data="close"
                    )
                ]
            ]
        )
    )


@Client.on_message(filters.command(["restart", f"restart@{USERNAME}"]))
@sudo_users_only
async def restart(client, m: Message):
    k = await m.reply_text("🔄 `Rᴇsᴛᴀʀᴛɪɴɢ ...`")
    await sleep(3)
    os.execl(sys.executable, sys.executable, *sys.argv)
    try:
        await k.edit("✅ **Rᴇsᴛᴀʀᴛᴇᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ! \nJᴏɪɴ [🎥𝚂𝚃𝙾𝚁𝚈 𝚃𝙸𝙼𝙴 𝙲𝙷𝙰𝙽𝙽𝙴𝙻 #𝙲𝙷𝙰𝚃𝙸𝙽𝙶💬](https://t.me/storytym) Fᴏʀ Mᴏʀᴇ!**")
    except:
        pass
