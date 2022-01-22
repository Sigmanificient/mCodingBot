from __future__ import annotations

import inspect
from os import getenv, listdir
from platform import python_version
from typing import TYPE_CHECKING, Dict

import dotenv
import pincer
from pincer.commands import command

if TYPE_CHECKING:
    from pincer.objects import Embed

    from mcoding_bot.bot import Bot


dotenv.load_dotenv()
MCODING = getenv("MCODING_SERVER")


class Information:
    def __init__(self, client: Bot) -> None:
        self.client = client

        self.files: Dict[str, str] = {}
        folders = (".", "cogs")

        for path in folders:
            files = (
                file for file in listdir(f"mcoding_bot/{path}") if file.endswith(".py")
            )

            for file in files:
                with open(f"mcoding_bot/{path}/{file}", encoding="utf-8") as f:
                    self.files[file] = f.read()

        self.files["Total"] = "\n".join(self.files.values())

    @command(name="links", description="Useful links", guild=MCODING)
    async def links(self):
        return self.client.embed(
            title="Useful links",
            description=inspect.cleandoc(
                """
                **[mCoding Youtube](https://www.youtube.com/channel/UCaiL2GDNpLYH6Wokkk1VNcg)**
                **[mCoding repo](https://github.com/mCodingLLC/VideosSampleCode)**
                **[mCoding-Bot repo](https://github.com/Sigmanificient/mCodingBot)**
                """
            ),
        )

    @command(name="code", description="Provide the code info", guild=MCODING)
    async def get_code(self) -> Embed:
        return self.client.embed(
            title="Code structure",
            description=f"The whole code structure of {self.client.bot}!",
        ).add_fields(
            self.files,
            map_title=lambda name: f"> {name}",
            map_values=lambda f: inspect.cleandoc(
                f"""
                - `{len(f):,}` characters
                - `{len(f.splitlines()):,}` lines
                """
            ),
        )

    @command(name="bot", description="Display the bot information", guild=MCODING)
    async def bot_info(self):
        embed = self.client.embed(
            title=f"{self.client.bot} Bot Information",
            description="This bot was created by mCoding discord community.",
        )

        info = {
            "Python": python_version(),
            "Pincer": str(pincer.__version__),
            "Commands": len(self.client.chat_commands),
            "Extensions": len(self.client.get_cogs()),
        }

        embed.add_fields(
            info.items(),
            map_title=lambda name: f"> {name}",
            map_values=lambda value: f"`{value}`",
        )

        return embed


setup = Information
