import asyncio
from info import *
from utils import *
from time import time 
from client import User
from pyrogram import Client, filters 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 

@Client.on_message(filters.text & filters.group & filters.incoming & ~filters.command(["verify", "connect", "id"]))
async def search(bot, message):
    # Check if user is subscribed to required channels
    f_sub = await force_sub(bot, message)
    if f_sub == False:
        return     
    channels = (await get_group(message.chat.id))["channels"]
    if not channels:
        return     
    if message.text.startswith("/"):
        return    

    query = message.text.strip()
    # Skip casual or vague messages (e.g., questions, greetings, or short phrases)
    if not await is_relevant_query(query):
        return

    head = "<b>⇩  ʜᴇʀᴇ ɪꜱ ʏᴏᴜʀ ʀᴇꜱᴜʟᴛꜱ  ⇩</b>\n\n"
    results = ""
    try:
        for channel in channels:
            async for msg in User.search_messages(chat_id=channel, query=query):
                name = (msg.text or msg.caption).split("\n")[0].lower()
                if name in results.lower():
                    continue 
                results += f"<b>🎬 {name}\n {msg.link} </b>\n\n"                                                      
        if not results:
            # If no results found in channels, suggest IMDb matches
            movies = await search_imdb(query)
            buttons = []
            for movie in movies: 
                buttons.append([InlineKeyboardButton(movie['title'], callback_data=f"recheck_{movie['id']}")])
            msg = await message.reply(
                "𝗜 𝗰𝗼𝘂𝗹𝗱𝗻'𝘁 𝗳𝗶𝗻𝗱 𝗮𝗻𝘆𝘁𝗵𝗶𝗻𝗴 𝗿𝗲𝗹𝗮𝘁𝗲𝗱 𝘁𝗼 𝘁𝗵𝗮𝘁.\n𝗗𝗶𝗱 𝘆𝗼𝘂 𝗺𝗲𝗮𝗻 𝗮𝗻𝘆 𝗼𝗻𝗲 𝗼𝗳 𝘁𝗵𝗲𝘀𝗲 ??", 
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        else:
            msg = await message.reply_text(text=head + results, disable_web_page_preview=True)
        _time = int(time()) + (15 * 60)
        await save_dlt_message(msg, _time)
    except Exception as e:
        print(f"Error in search: {e}")
        pass

async def is_relevant_query(query):
    """
    Check if the query is likely a specific anime/movie title rather than casual chat.
    You can customize this to fit your needs.
    """
    query = query.lower().strip()
    # Skip short queries, questions, or common conversational phrases
    if len(query.split()) <= 2:  # Adjust threshold as needed
        return False
    if any(word in query for word in ["what", "how", "why", "who", "which", "?", "kya", "kaise", "konsi"]):
        return False
    # Optionally, add more logic to validate against a list of known anime/movie titles
    # For example, check if query matches a pattern or exists in a predefined list
    return True

@Client.on_callback_query(filters.regex(r"^recheck"))
async def recheck(bot, update):
    clicked = update.from_user.id
    try:      
        typed = update.message.reply_to_message.from_user.id
    except:
        return await update.message.delete(2)       
    if clicked != typed:
        return await update.answer("ᴛʜɪꜱ ɪꜱ ɴᴏᴛ ꜰᴏʀ ʏᴏᴜ", show_alert=True)

    m = await update.message.edit("<b>ꜱᴇᴀʀᴄʜɪɴɢ ᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ ♻️</b>")
    id = update.data.split("_")[-1]
    query = await search_imdb(id)
    channels = (await get_group(update.message.chat.id))["channels"]
    head = "<b>ɪ ʜᴀᴠᴇ ꜱᴇᴀʀᴄʜᴇᴅ ᴍᴏᴠɪᴇ ᴡɪᴛʜ ʏᴏᴜʀ ᴡʀᴏɴɢ ꜱᴘᴇʟʟɪɴɢ...\nʙᴜᴛ ᴛᴀᴋᴇ ᴄᴀʀᴇ ɴᴇxᴛ ᴛɪᴍᴇ 😋</b>\n\n"
    results = ""
    try:
        for channel in channels:
            async for msg in User.search_messages(chat_id=channel, query=query):
                name = (msg.text or msg.caption).split("\n")[0].lower()
                if name in results.lower():
                    continue 
                results += f"<b>🎬 {name}\n {msg.link} </b>\n\n"
        if not results:          
            return await update.message.edit(
                "<b>⚠️ ɴᴏ ʀᴇꜱᴜʟᴛꜱ ꜰᴏᴜɴᴅ !!\nᴘʟᴇᴀꜱᴇ ʀᴇǫᴜᴇꜱᴛ ᴛᴏ ɢʀᴏᴜᴘ ᴀᴅᴍɪɴ 👇🏻</b>",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🧑‍✈️  ʀᴇǫᴜᴇꜱᴛ ᴛᴏ ᴀᴅᴍɪɴ  🧑‍✈️", callback_data=f"request_{id}")]
                ])
            )
        await update.message.edit(text=head + results, disable_web_page_preview=True)
    except Exception as e:
        await update.message.edit(f"ᴇʀʀᴏʀ - `{e}`")

@Client.on_callback_query(filters.regex(r"^request"))
async def request(bot, update):
    clicked = update.from_user.id
    try:      
        typed = update.message.reply_to_message.from_user.id
    except:
        return await update.message.delete()       
    if clicked != typed:
        return await update.answer("ᴛʜɪꜱ ɪꜱ ɴᴏᴛ ꜰᴏʀ ʏᴏᴜ", show_alert=True)

    admin = (await get_group(update.message.chat.id))["user_id"]
    id = update.data.split("_")[1]
    name = await search_imdb(id)
    url = f"https://www.imdb.com/title/tt{id}"
    text = f"#Request\n\nɴᴀᴍᴇ - {name}\nɪᴍᴅʙ - {url}"
    await bot.send_message(chat_id=admin, text=text, disable_web_page_preview=True)
    await update.answer("ʀᴇǫᴜᴇꜱᴛ ꜱᴇɴᴅ ᴛᴏ ᴀᴅᴍɪɴ  ✅", show_alert=True)
    await update.message.delete(60)
