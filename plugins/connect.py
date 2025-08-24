from info import *
from utils import *
from client import User 
from pyrogram import Client, filters

@Client.on_message(filters.group & filters.command("connect"))
async def connect(bot, message):
    m = await message.reply("<b>ᴄᴏɴɴᴇᴄᴛɪɴɢ...</b>")
    user = await User.get_me()
    try:
        group = await get_group(message.chat.id)
        user_id = group["user_id"] 
        user_name = group["user_name"]
        verified = group["verified"]
        channels = group["channels"].copy()
    except:
        return await bot.leave_chat(message.chat.id)  
    if message.from_user.id != user_id:
        return await m.edit(f"Only {user_name} can use this command 😁")
    if not verified:
        return await m.edit("ᴛʜɪꜱ ᴄʜᴀᴛ ɪꜱ ɴᴏᴛ ᴠᴇʀɪꜰɪᴇᴅ 🚫\nᴜꜱᴇ /verify")    
    try:
        channel = int(message.command[-1])
        if channel in channels:
            return await m.edit("ᴛʜɪꜱ ᴄʜᴀɴɴᴇʟ ɪꜱ ᴀʟʀᴇᴀᴅʏ ᴄᴏɴɴᴇᴄᴛᴇᴅ")
    except:
        return await m.edit("ɪɴᴄᴏʀʀᴇᴄᴛ ꜰᴏʀᴍᴀᴛ 🚫\nᴜꜱᴇ `/connect <channel_id>`")    
    try:
        chat = await bot.get_chat(channel)
        group = await bot.get_chat(message.chat.id)
        c_link = chat.invite_link or f"https://t.me/{chat.username}" if chat.username else f"Private Channel ({chat.id})"
        g_link = group.invite_link or f"Private Group ({group.id})"
        # Check if bot is already a member of the channel
        member = await User.get_chat_member(channel, user.id)
        if member.status not in ["member", "administrator", "creator"]:
            return await m.edit(
                f"🚫 Bot must be added as an admin to [{chat.title}]({c_link}) first!\n"
                "Please add @search_postbbot manually and try again."
            )
        channels.append(channel)
        await update_group(message.chat.id, {"channels": channels})
        await m.edit(f"ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴛᴏ\n[{chat.title}]({c_link})", disable_web_page_preview=True)
        text = f"#NewConnection\n\nUser: {message.from_user.mention}\nGroup: [{group.title}]({g_link})\nChannel: [{chat.title}]({c_link})"
        await bot.send_message(chat_id=LOG_CHANNEL, text=text)
    except Exception as e:
        text = f"🚫 ᴇʀʀᴏʀ - `{str(e)}`\nᴍᴀᴋᴇ ꜱᴜʀᴇ @search_postbbot is an admin in the channel and group with all permissions and not banned."
        return await m.edit(text)

@Client.on_message(filters.group & filters.command("disconnect"))
async def disconnect(bot, message):
    m = await message.reply("<b>ᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ...</b>")   
    try:
        group = await get_group(message.chat.id)
        user_id = group["user_id"] 
        user_name = group["user_name"]
        verified = group["verified"]
        channels = group["channels"].copy()
    except:
        return await bot.leave_chat(message.chat.id)  
    if message.from_user.id != user_id:
        return await m.edit(f"Only {user_name} can use this command 😁")
    if not verified:
        return await m.edit("ᴛʜɪꜱ ᴄʜᴀᴛ ɪꜱ ɴᴏᴛ ᴠᴇʀɪꜰɪᴇᴅ 🚫\nᴜꜱᴇ /verify")    
    try:
        channel = int(message.command[-1])
        if channel not in channels:
            return await m.edit("ʏᴏᴜ ᴅɪᴅ ɴᴏᴛ ᴀᴅᴅᴇᴅ ᴛʜɪꜱ ᴄʜᴀɴɴᴇʟ ʏᴇᴛ")
        channels.remove(channel)
    except:
        return await m.edit("ɪɴᴄᴏʀʀᴇᴄᴛ ꜰᴏʀᴍᴀᴛ 🚫\nᴜꜱᴇ `/disconnect <channel_id>`")
    try:
        chat = await bot.get_chat(channel)
        group = await bot.get_chat(message.chat.id)
        c_link = chat.invite_link or f"https://t.me/{chat.username}" if chat.username else f"Private Channel ({chat.id})"
        g_link = group.invite_link or f"Private Group ({group.id})"
        # Optional: Bot leaves channel (uncomment if desired)
        # await User.leave_chat(channel)
        await update_group(message.chat.id, {"channels": channels})
        await m.edit(f"ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴅɪꜱᴄᴏɴɴᴇᴄᴛᴇᴅ ꜰʀᴏᴍ [{chat.title}]({c_link})", disable_web_page_preview=True)
        text = f"#DisConnection\n\nUser: {message.from_user.mention}\nGroup: [{group.title}]({g_link})\nChannel: [{chat.title}]({c_link})"
        await bot.send_message(chat_id=LOG_CHANNEL, text=text)
    except Exception as e:
        text = f"🚫 ᴇʀʀᴏʀ - `{str(e)}`\nᴍᴀᴋᴇ ꜱᴜʀᴇ @search_postbbot is an admin in the channel and group with all permissions and not banned."
        return await m.edit(text)

@Client.on_message(filters.group & filters.command("connections"))
async def connections(bot, message):
    try:
        group = await get_group(message.chat.id)    
        user_id = group["user_id"]
        user_name = group["user_name"]
        channels = group["channels"]
        f_sub = group["f_sub"]
    except:
        return await bot.leave_chat(message.chat.id)
    if message.from_user.id != user_id:
        return await message.reply(f"Only {user_name} can use this command 😁")
    if not channels:
        return await message.reply("ᴛʜɪꜱ ɢʀᴏᴜᴘ ɪꜱ ᴄᴜʀʀᴇɴᴛʟʏ ɴᴏᴛ ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴛᴏ ᴀɴʏ ᴄʜᴀɴɴᴇʟꜱ.\nᴄᴏɴɴᴇᴄᴛ ᴏɴᴇ ᴜꜱɪɴɢ /connect")
    text = "ᴛʜɪꜱ ɢʀᴏᴜᴘ ɪꜱ ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴡɪᴛʜ - \n\n"
    for channel in channels:
        try:
            chat = await bot.get_chat(channel)
            name = chat.title
            link = chat.invite_link or f"https://t.me/{chat.username}" if chat.username else f"Private Channel ({chat.id})"
            text += f"[{name}]({link})\n"
        except Exception as e:
            text += f"🚫 Error in `{channel}`: `{e}`\n"
    if f_sub:
        try:
            f_chat = await bot.get_chat(f_sub)
            f_title = f_chat.title
            f_link = f_chat.invite_link or f"https://t.me/{f_chat.username}" if f_chat.username else f"Private Channel ({f_chat.id})"
            text += f"\nFSub: [{f_title}]({f_link})"
        except Exception as e:
            text += f"❌ ᴇʀʀᴏʀ ɪɴ ꜰꜱᴜʙ (`{f_sub}`): `{e}`\n"
    await message.reply(text=text, disable_web_page_preview=True)
