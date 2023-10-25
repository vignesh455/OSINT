
from urllib.parse import quote_plus
from json import dumps, decoder
import instaloader
import logging
import pandas as pd
import phonenumbers
import time
import requests
import truecallerpy
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

API = '' #Your Telegrma Bot API
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API)
BOT = instaloader.Instaloader()
dp = Dispatcher(bot)

b1 = KeyboardButton('Admin ☠')
b2 = KeyboardButton('IG OSINT ☠')
b3 = KeyboardButton('Actress Admirers❤')
b4 = KeyboardButton('PhoneInfo📞')

r = ReplyKeyboardMarkup(resize_keyboard=True).add(b1, b2).add(b3,b4)


@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    await msg.answer(f"Hello, Welcome {msg.chat.first_name} ", reply_markup=r)


@dp.message_handler(text='Admin ☠')
async def admin(msg: types.Message):
    await msg.answer("Admin --> @placements_VR")


@dp.message_handler(text='Actress Admirers❤')
async def actress(msg: types.Message):
    await msg.answer('--> @Actress_Admirerss')


@dp.message_handler(text="IG OSINT ☠")
async def insta(msg: types.Message):
    await msg.answer("Send me Instagram Username: ")

@dp.message_handler(text='PhoneInfo📞')
async def insta(msg: types.Message):
    await msg.answer("Send me a MobileNum with Country Code: \nExample +91830xxxxxxx ")

@dp.message_handler()
async def user(msg: types.Message):
    username = msg.text
    if username[1:].isdigit():
        num = phonenumbers.parse(username)
        print(username)
        await msg.answer("______Processing______")
        time.sleep(2)
        await msg.answer("___Getting Information___")
        time.sleep(2)
        c = truecallerpy.search_phonenumber(username, "IN",
                                            "a1i0q--gY7qq2-c-IbuuAC96o2kttqyeNvZC9MTB-tx-5fyOQk5wu1-cs6sL4s4N")
        await msg.answer(f"Name  :  {str(c['data'][0]['name'])}")
        if 'gender' in c['data'][0].keys():
            await msg.answer(f"Gender  :  {str(c['data'][0]['gender'])}")
        await msg.answer(f"Access  :  {str(c['data'][0]['access'])}")
        await msg.answer(f"Enhanced  :  {str(c['data'][0]['enhanced'])}")
        await msg.answer(f"Number Type  :  {str(c['data'][0]['phones'][0]['numberType'])}")
        await msg.answer(f"Carrier  :  {str(c['data'][0]['phones'][0]['carrier'])}")
        await msg.answer(f"E164format  :  {str(c['data'][0]['phones'][0]['e164Format'])}")
        await msg.answer(f"Dialing Code  :  {str(c['data'][0]['phones'][0]['dialingCode'])}")
        await msg.answer(f"Country Code  :  {str(c['data'][0]['phones'][0]['countryCode'])}")
        await msg.answer(f"City  :  {str(c['data'][0]['addresses'][0]['city'])}")
        await msg.answer(f"Time Zone  :  {str(c['data'][0]['addresses'][0]['timeZone'])}")
        await msg.answer(f"Frequency  :  {str(c['data'][0]['surveys'][0]['frequency'])}")
        await msg.answer(f"Provider  :  {str(c['provider'])}")
        if len(c['data'][0]['internetAddresses']):
            await msg.answer(f"Email  :  {str(c['data'][0]['internetAddresses'][0]['id'])}")
        else:
            await msg.answer("Email  :  No Email Found")
        if 'image' in c['data'][0].keys():
            await msg.answer(f"Photo  :  {str(c['data'][0]['image'])}")
        else:
            await msg.answer("No Image file Found")

    else:
        try:
            profile = instaloader.Profile.from_username(BOT.context, username)
            result = advanced_lookup(username)
            result = result['user']
            if result['status'] == 'fail':
                await msg.answer("No username found or it's a verified account")
            else:
                print(result)
                print()
                A = [result['status'],result['user']['username'],result['user_id'],result['multiple_users_found'],result['user']['full_name'],result['user']['fbid_v2'],
                     profile.mediacount,profile.followers,profile.followees,profile.biography,profile.external_url,result['user']['is_private'],
                     result['user']['is_verified'],result['can_email_reset'],result['can_sms_reset'],result['fb_login_option']]
                B = ["Status : ","USername : ","User Id : ","MultipleUsersFound : ","FullName : ","FbId_V2 : ","Media Count : ","Followers : ","Following : ",
                     "Bio : ","External URL : ","Private Acc : ","Verified Acc : ","Email Reset : ","SMS Reset : ","FB Login : ","Obfuscated Phone : ","Obfuscated Email : "]
                if 'obfuscated_phone' in result.keys():
                    A.append(result['obfuscated_phone'])
                else:
                    A.append("None")
                if 'obfuscated_email' in result.keys():
                    A.append(result['obfuscated_email'])
                else:
                    A.append("None")
                await msg.answer("______Processing______")

                time.sleep(3)
                await msg.answer(str(pd.Series(A,index=B)))
        except Exception as e:
            await msg.answer(str(e))


def advanced_lookup(username):
    data = "signed_body=SIGNATURE." + quote_plus(dumps(
        {"q": username, "skip_recovery": "1"},
        separators=(",", ":")
    ))
    api = requests.post(
        'https://i.instagram.com/api/v1/users/lookup/',
        headers={
            "Accept-Language": "en-US",
            "User-Agent": "Instagram 101.0.0.15.120",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-IG-App-ID": "124024574287414",
            "Accept-Encoding": "gzip, deflate",
            "Host": "i.instagram.com",
            # "X-FB-HTTP-Engine": "Liger",
            "Connection": "keep-alive",
            "Content-Length": str(len(data))
        },
        data=data
    )
    try:
        return ({"user": api.json(), "error": None})
    except decoder.JSONDecodeError:
        return ({"user": None, "error": "rate limit"})


executor.start_polling(dp)
