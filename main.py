import mail
import PythonTelegramWraper.bot as BotWrapper
import time
import os
import config

sender = mail.Sender()


def start(update, context):
    chatID = BotWrapper.chatID(update)
    BotWrapper.sendMessage(chatID, "Your ChatID is: "+str(chatID))


BotWrapper.addBotCommand("start", start)
BotWrapper.startBot()

while True:

    out = sender.check()
    if out is not None:
        
        for mail in out:
            out_string = "*Neuer Druckauftrag*\n\n"
            for key in mail:
                if key == "Email":
                    continue
                out_string += "_"+key+"_"
                out_string += "\n   "
                out_string += mail[key]
                out_string += "\n"
            BotWrapper.sendMessage(config.chatID, out_string)
            if "file" in mail:
                BotWrapper.botBackend.dispatcher.bot.send_document(
                    chat_id=config.chatID, document=open(mail['file'], 'rb'))
                os.remove(mail['file'])

    time.sleep(10)
