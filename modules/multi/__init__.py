import re
from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Group
from graia.ariadne.message.parser.base import StartsWith
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema


import modules.multi.fileio as mulio
from random import choice
from typing import Annotated
channel = Channel.current()

@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def add_sentence(app:Ariadne, group:Group, message: Annotated[MessageChain, StartsWith(["加语录"])]):
    rawmsg = message.display
    res = re.fullmatch(r"(.+?)[:|：][ ]?(.+)", rawmsg)
    if res is None:
        return await app.send_message(
            group,
            "empty string not allowed!!!1"
        )
    name, saying = res.group(1,2)
    if mulio.write(saying,name) == 1:
        return await app.send_group_message(
            group,
            MessageChain(f"{name} 说的 {saying} 已经有了！！！1")
        )
    await app.send_message(
        group,
        MessageChain(f"{saying} 现已加入 {name} 语录套餐")
    )


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def get_sentence(app:Ariadne, group:Group, message: Annotated[MessageChain, StartsWith(["语录"])]):
    rawmsg = message.display
    slist = mulio.getsp(rawmsg)
    if(slist == []):
        await app.send_message(
            group,
            f"{rawmsg} 说过什么吗"
        )
    await app.send_message(
        group,
        MessageChain(choice(slist))
    )
