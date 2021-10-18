"""
VideoPlayerBot, Telegram Video Chat Bot
Copyright (c) 2021  Asm Safone <https://github.com/AsmSafone>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>
"""

import os
import re
import sys
import time
import ffmpeg
import asyncio
import subprocess
from asyncio import sleep
from plugins.nopm import User
from youtube_dl import YoutubeDL
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import GroupCallFactory
from helpers.bot_utils import USERNAME
from config import AUDIO_CALL, VIDEO_CALL
from youtubesearchpython import VideosSearch
from helpers.decorators import authorized_users_only
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery


ydl_opts = {
        "quiet": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
}
ydl = YoutubeDL(ydl_opts)
group_call = GroupCallFactory(User, GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM).get_group_call()


@Client.on_callback_query(filters.regex("pause_callback"))
async def pause_callbacc(client, CallbackQuery):
    chat_id = CallbackQuery.message.chat.id
    if chat_id in AUDIO_CALL:
        text = f"⏸ Pᴀᴜsᴇᴅ !"
        await AUDIO_CALL[chat_id].set_audio_pause(True)
    elif chat_id in VIDEO_CALL:
        text = f"⏸ Pᴀᴜsᴇᴅ !"
        await VIDEO_CALL[chat_id].set_video_pause(True)
    else:
        text = f"❌ Nᴏᴛʜɪɴɢ ɪs Pʟᴀʏɪɴɢ !"
    await Client.answer_callback_query(
        CallbackQuery.id, text, show_alert=True
    )

@Client.on_callback_query(filters.regex("resume_callback"))
async def resume_callbacc(client, CallbackQuery):
    chat_id = CallbackQuery.message.chat.id
    if chat_id in AUDIO_CALL:
        text = f"▶️ Rᴇsᴜᴍᴇᴅ !"
        await AUDIO_CALL[chat_id].set_audio_pause(False)
    elif chat_id in VIDEO_CALL:
        text = f"▶️ Rᴇsᴜᴍᴇᴅ !"
        await VIDEO_CALL[chat_id].set_video_pause(False)
    else:
        text = f"❌ Nᴏᴛʜɪɴɢ ɪs Pʟᴀʏɪɴɢ !"
    await Client.answer_callback_query(
        CallbackQuery.id, text, show_alert=True
    )


@Client.on_callback_query(filters.regex("end_callback"))
async def end_callbacc(client, CallbackQuery):
    chat_id = CallbackQuery.message.chat.id
    if chat_id in AUDIO_CALL:
        text = f"⏹️ 🆂🆃🅾️🅿️🅿️🅴🅳  !"
        await AUDIO_CALL[chat_id].stop()
        AUDIO_CALL.pop(chat_id)
    elif chat_id in VIDEO_CALL:
        text = f"⏹️ 🆂🆃🅾️🅿️🅿️🅴🅳  !"
        await VIDEO_CALL[chat_id].stop()
        VIDEO_CALL.pop(chat_id)
    else:
        text = f"❌ Nᴏᴛʜɪɴɢ ɪs Pʟᴀʏɪɴɢ !"
    await Client.answer_callback_query(
        CallbackQuery.id, text, show_alert=True
    )
    await Client.send_message(
        chat_id=CallbackQuery.message.chat.id,
        text=f"✅ **Sᴛʀᴇᴀᴍɪɴɢ Sᴛᴏᴘᴘᴇᴅ & Lᴇғᴛ Tʜᴇ Vɪᴅᴇᴏ Cʜᴀᴛ !**"
    )
    await CallbackQuery.message.delete()


@Client.on_message(filters.command(["stream", f"stream@{USERNAME}"]) & filters.group & ~filters.edited)
@authorized_users_only
async def stream(client, m: Message):
    msg = await m.reply_text("🔄 Pʀᴏᴄᴇssɪɴɢ ...`")
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
            await msg.edit("🔄 Sᴛᴀʀᴛɪɴɢ YᴏᴜTᴜʙᴇ Vɪᴅᴇᴏ Sᴛʀᴇᴀᴍ ...`")
            try:
                meta = ydl.extract_info(query, download=False)
                formats = meta.get('formats', [meta])
                for f in formats:
                    ytstreamlink = f['url']
                link = ytstreamlink
                search = VideosSearch(query, limit=1)
                opp = search.result()["result"]
                oppp = opp[0]
                thumbid = oppp["thumbnails"][0]["url"]
                split = thumbid.split("?")
                thumb = split[0].strip()
            except Exception as e:
                return await msg.edit(f"❌ YᴏᴜTᴜʙᴇ Dᴏᴡɴʟᴏᴀᴅ Eʀʀᴏʀ !** \n\n`{e}`")
                print(e)

        else:
            await msg.edit("🔄 Sᴛᴀʀᴛɪɴɢ YᴏᴜTᴜʙᴇ Vɪᴅᴇᴏ Sᴛʀᴇᴀᴍ ...`")
            link = query
            thumb = "https://telegra.ph/file/0df0a53d07608604edd07.jpg"

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
            await group_call.start_video(link, with_audio=True, repeat=False)
            VIDEO_CALL[chat_id] = group_call
            await msg.delete()
            await m.reply_photo(
               photo=thumb, 
               caption=f"▶️ **Started [Video Streaming]({query}) In {m.chat.title} !**",
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

    elif media.video or media.document:
        await msg.edit("🔄 'Dᴏᴡɴʟᴏᴀᴅɪɴɢ ...`")
        if media.video.thumbs:
            lol = media.video.thumbs[0]
            lel = await client.download_media(lol['file_id'])
            thumb = lel
        else:
            thumb = "https://telegra.ph/file/62e86d8aadde9a8cbf9c2.jpg"
        video = await client.download_media(media)

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
            await group_call.start_video(video, with_audio=True, repeat=False)
            VIDEO_CALL[chat_id] = group_call
            await msg.delete()
            await m.reply_photo(
               photo=thumb,
               caption=f"▶️ **Sᴛᴀʀᴛᴇᴅ [Vɪᴅᴇᴏ Sᴛʀᴇᴀᴍɪɴɢ](telegram.me/VAMPIRE_KING_NO_1) Iɴ {m.chat.title} !**",
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
            "💁🏻‍♂️ Dᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ sᴇᴀʀᴄʜ ғᴏʀ ᴀ YᴏᴜTᴜʙᴇ ᴠɪᴅᴇᴏ?",
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


@Client.on_message(filters.command(["pause", f"pause@{USERNAME}"]) & filters.group & ~filters.edited)
@authorized_users_only
async def pause(_, m: Message):
    chat_id = m.chat.id

    if chat_id in AUDIO_CALL:
        await AUDIO_CALL[chat_id].set_audio_pause(True)
        await m.reply_text("⏸ **Pᴀᴜsᴇᴅ Aᴜᴅɪᴏ Sᴛʀᴇᴀᴍɪɴɢ !**")

    elif chat_id in VIDEO_CALL:
        await VIDEO_CALL[chat_id].set_video_pause(True)
        await m.reply_text("⏸ **Pᴀᴜsᴇᴅ Vɪᴅᴇᴏ Sᴛʀᴇᴀᴍɪɴɢ !**")

    else:
        await m.reply_text("❌ **Nᴏᴛɪɴɢ Is Sᴛʀᴇᴀᴍɪɴɢ !**")


@Client.on_message(filters.command(["resume", f"resume@{USERNAME}"]) & filters.group & ~filters.edited)
@authorized_users_only
async def resume(_, m: Message):
    chat_id = m.chat.id

    if chat_id in AUDIO_CALL:
        await AUDIO_CALL[chat_id].set_audio_pause(False)
        await m.reply_text("▶️ **Rᴇsᴜᴍᴇᴅ Aᴜᴅɪᴏ Sᴛʀᴇᴀᴍɪɴɢ !**")

    elif chat_id in VIDEO_CALL:
        await VIDEO_CALL[chat_id].set_video_pause(False)
        await m.reply_text("▶️ **Rᴇsᴜᴍᴇᴅ  Vɪᴅᴇᴏ Sᴛʀᴇᴀᴍɪɴɢ !**")

    else:
        await m.reply_text("❌ **Nᴏᴛɪɴɢ Is Sᴛʀᴇᴀᴍɪɴɢ !**")


@Client.on_message(filters.command(["endstream", f"endstream@{USERNAME}"]) & filters.group & ~filters.edited)
@authorized_users_only
async def endstream(client, m: Message):
    msg = await m.reply_text("🔄 `Pʀᴏᴄᴇssɪɴɢ ...`")
    chat_id = m.chat.id

    if chat_id in AUDIO_CALL:
        await AUDIO_CALL[chat_id].stop()
        AUDIO_CALL.pop(chat_id)
        await msg.edit("⏹️ **Sᴛᴏᴘᴘᴇᴅ Aᴜᴅɪᴏ Sᴛʀᴇᴀᴍɪɴɢ !**")

    elif chat_id in VIDEO_CALL:
        await VIDEO_CALL[chat_id].stop()
        VIDEO_CALL.pop(chat_id)
        await msg.edit("⏹️ **Sᴛᴏᴘᴘᴇᴅ Vɪᴅᴇᴏ Sᴛʀᴇᴀᴍɪɴɢ !**")

    else:
        await msg.edit("🤖 **Pʟᴇᴀsᴇ Sᴛᴀʀᴛ Aɴ Sᴛʀᴇᴀᴍ Fɪʀsᴛ !**")


# pytgcalls handlers

@group_call.on_audio_playout_ended
async def audio_ended_handler(_, __):
    await sleep(3)
    await group_call.stop()
    print(f"[INFO] - AUDIO_CALL ENDED !")

@group_call.on_video_playout_ended
async def video_ended_handler(_, __):
    await sleep(3)
    await group_call.stop()
    print(f"[INFO] - VIDEO_CALL ENDED !")
