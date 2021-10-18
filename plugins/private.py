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

import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import MessageNotModified
from helpers.bot_utils import BOT_NAME, USERNAME
from config import SUPPORT_GROUP, UPDATES_CHANNEL
from translations import START_TEXT, HELP_TEXT, ABOUT_TEXT
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

@Client.on_message(filters.command(["start", f"start@{USERNAME}"]))
async def start(client, message):
   buttons = [
            [
                InlineKeyboardButton("𝙃𝙚𝙡𝙥 🥺", callback_data="help"),
            ],
            [
                InlineKeyboardButton("𝙈𝙮 𝘿𝙚𝙫 🔥", url=f"telegram.me/VAMPIRE_KING_NO_1"),
                InlineKeyboardButton("𝗦𝗲𝗮𝗿𝗰𝗵 𝗬𝗼𝘂𝘁𝘂𝗯𝗲 𝗩𝗲𝗱𝗶𝗼🔎", switch_inline_query_current_chat=''),
            ],
            [
                InlineKeyboardButton("𝘼𝙗𝙤𝙪𝙩 😎", callback_data="about"),
                InlineKeyboardButton("𝙲𝙻𝙾𝚂𝙴 🔒", callback_data="close"),
            ],
            [
               InlineKeyboardButton("➕ 𝐀𝐝𝐝 𝐌𝐞 𝐓𝐨 𝐘𝐨𝐮𝐫 𝐆𝐫𝐨𝐮𝐩 ➕", url=f"https://t.me/{USERNAME}?startgroup=true"),
            ]
            ]
   reply_markup = InlineKeyboardMarkup(buttons)
   if message.chat.type == 'private':
       await message.reply_text(
          START_TEXT,
          reply_markup=reply_markup
       )
   else:
      await message.reply_text(f"**{BOT_NAME} is Alive !** ✨")

@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.data=="help":
        buttons = [
            [
                InlineKeyboardButton("🔙 ᗷᗩᑕK", callback_data="start"),
                InlineKeyboardButton ("🆁🅴🅿️🅾️", url=f"https://t.me/NOKIERUNNOIPPKITTUM"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            await query.edit_message_text(
                HELP_TEXT,
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

    elif query.data=="about":
        buttons = [
            [
                InlineKeyboardButton("🔙 ᗷᗩᑕK", callback_data="start"),
                InlineKeyboardButton ("𝙃𝙚𝙡𝙥 🥺", callback_data="help"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            await query.edit_message_text(
                ABOUT_TEXT,
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

    elif query.data=="start":
        buttons = [
            [
                InlineKeyboardButton("𝙃𝙚𝙡𝙥 🥺", callback_data="help"),
            ],
            [
                InlineKeyboardButton("𝙈𝙮 𝘿𝙚𝙫 🔥", url=f"telegram.me/VAMPIRE_KING_NO_1"),
                InlineKeyboardButton("𝗦𝗲𝗮𝗿𝗰𝗵 𝗬𝗼𝘂𝘁𝘂𝗯𝗲 𝗩𝗲𝗱𝗶𝗼🔎", switch_inline_query_current_chat=''),
            ],
            [
                InlineKeyboardButton("𝘼𝙗𝙤𝙪𝙩 😎", callback_data="about"),
                InlineKeyboardButton("𝙲𝙻𝙾𝚂𝙴 🔒", callback_data="close"),
            ],
            [
               InlineKeyboardButton("➕ 𝐀𝐝𝐝 𝐌𝐞 𝐓𝐨 𝐘𝐨𝐮𝐫 𝐆𝐫𝐨𝐮𝐩 ➕", url=f"https://t.me/{USERNAME}?startgroup=true"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            await query.edit_message_text(
                START_TEXT,
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

    elif query.data=="close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
        except:
            pass

