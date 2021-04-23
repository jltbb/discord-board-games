import os
import discord
import checkers
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("discord_token")
GUILD_ID = os.getenv("guild_id")

players = {}

def discord_bot_loop():
    client = discord.Client()

    @client.event
    async def on_ready():
        for guild in client.guilds:
            if guild.name == GUILD_ID:
                break

        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )

    @client.event
    async def on_message(message):
        if str(message.author) == 'buyerbeware#0728':
            pass

        if message.content == '-play checkers':
            checkers.create_board()

            text = checkers.draw_board()
            await message.channel.send(text)

        if message.content.startswith('-move'):
            if checkers.game.current_player not in players:
                players[checkers.game.current_player] = str(message.author)
                await message.channel.send(f'<@{str(message.author.id)}> is now {checkers.game.current_player.name}')
            else:
                if not str(message.author) == players[checkers.game.current_player]:
                    return

            start, end = message.content.split(' ')[1:]
            checkers.move_piece(start, end)

            if checkers.msg_buffer != None:
                await message.channel.send(checkers.msg_buffer)

                if "has won" in checkers.msg_buffer:
                    text = checkers.draw_board()
                    await message.channel.send(text)

                    checkers.create_board()
            else:
                text = checkers.draw_board()
                await message.channel.send(text)

    client.run(TOKEN)

if __name__ == '__main__':
    discord_bot_loop()
