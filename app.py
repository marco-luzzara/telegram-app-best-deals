from __future__ import annotations
from cProfile import run
from telethon import TelegramClient, events
import re
import os
import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

best_deals_pattern = re.compile(r'.*\berrore\b.*', re.I)

# set the environment variables below in a file called .env (for example)
#
#     API_ID=xxx
#     API_HASH=yyy
#     ACCEPTED_ENTITIES=username:channel_link:me
#     ENTITY_TO_FORWARD=channel_id
#
# and, before launching the application, run
#
#     source .env
api_id = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']
accepted_entities = os.environ['ACCEPTED_ENTITIES'].split(':')
entity_to_forward = os.environ['ENTITY_TO_FORWARD']

with TelegramClient('anon', api_id, api_hash) as client:
    client: TelegramClient
    @client.on(events.NewMessage(\
        incoming=True, forwards=False, pattern=best_deals_pattern, from_users=accepted_entities))
    async def incoming_best_deals(event):
        forwarding_entity = await client.get_input_entity(entity_to_forward)
        await event.forward_to(forwarding_entity)
    
    client.run_until_disconnected()