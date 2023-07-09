


from telethon import TelegramClient, events, utils, types, sync
import openai
import Creds
client = TelegramClient('session_name', Creds.tg_api_id, Creds.tg_hash, proxy=None)
# ----------------------------------------------------------------------------------------------------------------------

async def send_text(chat_id, caption, link, channel_name):
    await client.send_message(chat_id, f'<b>{caption}</b>\n \nTransmits <a href="{link}">{channel_name}</a>', parse_mode="HTML")

async def send_document(media, chat_id, caption, link, channel_name):
    if isinstance(media, types.Document):
        file_path = await client.download_media(media)
        await client.send_file(chat_id, file_path, caption=f'<b>{caption}</b>\n \nTransmits <a href="{link}">{channel_name}</a>', parse_mode="HTML")
    elif isinstance(media, types.WebPage):
        await client.send_message(chat_id, f'<b>{caption}</b>\n \nTransmits <a href="{link}">{channel_name}</a>', link_preview=True, parse_mode="HTML")
    else:
        await send_text(chat_id, caption, link, channel_name)
# ----------------------------------------------------------------------------------------------------------------------

@client.on(events.NewMessage(chats=["rybar", "tpolit", "box_of_pandora", "ASupersharij", "strelkovii", "SBelkovskiy", "helper0372"]))
async def handle_new_message(event):
# event = oefhliughas;doihgba;owuirg - 1234565432345
    message = event.message  # full info
    media = message.media  # media info
    caption = message.message  # text
    chat_id = "ainewsusa"  # to
    message_id = event.message.id  # message id
    channel_id = event.chat_id  # id from ...
    channel_entity = await client.get_entity(channel_id)  # channel info
    channel_username = channel_entity.username  # channel username
    channel_name = utils.get_display_name(channel_entity)  # channel name
    link = f"https://t.me/{channel_username}/{message_id}"
# ----------------------------------------------------------------------------------------------------------------------

    if caption == "":
        pass

    else:
        openai.api_key = Creds.key_il
        completion = openai.ChatCompletion.create(
            temperature=0.5,
            model="gpt-3.5-turbo",  # this is "ChatGPT" $0.002 per 1k tokens
            messages=[
                {"role": "user", "content": f"translate this into English - {message.message}"},
                {"role": "system", "content": "You only translate text and return only the translation"}])
        caption = completion.choices[0].message.content
    if media == None:
        await send_text(chat_id, caption, link, channel_name)

    else:
        await send_document(media, chat_id, caption, link, channel_name)
# ----------------------------------------------------------------------------------------------------------------------

with client:
    client.run_until_disconnected()

