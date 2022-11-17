import asyncio
from main_twitch import TwitchBot
from main_discord import DiscordBot
from discord import Intents, Status

# override methods to have names from proper functions even if they collide between libs

class MainBot():
    def __init__(self) -> None:
        self.discord = DiscordBot(bridge=self,
            command_prefix="=", 
            owner_id = 347524158181212161, 
            intents = Intents.all(), 
            case_insensitive=True, 
            status=Status.online
            )
        self.twitch = TwitchBot(bridge=self)

    async def start(self) -> None:
        print("Starting bots...")
        await asyncio.gather(self.discord.go(), 
                            self.twitch.go(), 
                            return_exceptions=True)



if __name__ == "__main__":
    main = MainBot()

    asyncio.run(main.start())