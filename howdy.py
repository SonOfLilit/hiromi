from hiromi.commands import command


@command("howdy <weather>")
def schedule(command, weather):
    command.room.send(f"Hello to you too, isn't it a nice {weather}y day outside?")
