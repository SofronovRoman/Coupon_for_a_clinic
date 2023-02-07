# -*- coding: utf-8 -*-
"""
Created on Sat May 21 18:11:29 2022

@author: User
"""

import asyncio
from pyrogram import Client


api_id = int(input('Enter api_id: '))
api_hash = input('Enter api_hash: ')
phone_number = input('Enter phone number: ')


async def main():
    async with Client(phone_number, api_id, api_hash) as app:
        await app.send_message("me", "Telegram-сесиия создана.")


asyncio.run(main())