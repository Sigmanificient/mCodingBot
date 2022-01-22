from __future__ import annotations

import re
from typing import TYPE_CHECKING

from pincer import Client

if TYPE_CHECKING:
    from pincer.objects import UserMessage

    from mcoding_bot.bot import Bot


class AutoMod:
    def __init__(self, client: Bot):
        self.client = client

        self.bad_strings = (
            (
                re.compile(r"sudo\s+rm"),
                (
                    "`sudo rm` can be dangerous, as it will remove "
                    "any file and is irreversible. Use with care."
                ),
            ),
            (
                re.compile(r".+\(?.*\)?.*{.+\|.+&.*}.*;.*"),
                (
                    "This is a dangerous function and can cause your "
                    "computer to freeze. Please don't run it."
                ),
            ),
        )

    @Client.event
    async def on_message(self, message: UserMessage):
        if message.author.id == self.client.bot.id:
            return

        content = message.content.replace("\n", " ")

        for bad_reg, resp in self.bad_strings:
            if bad_reg.findall(content):
                await (await self.client.get_channel(message.channel_id)).send(resp)


setup = AutoMod
