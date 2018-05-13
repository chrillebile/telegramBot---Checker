from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

bot = ChatBot(
    'Sven',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch'
        },
        {
            'import_path': 'chatterbot.logic.MathematicalEvaluation'
        },
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': 0.65,
            'default_response': 'I am sorry, but I do not understand.'
        }
    ],
    database='./database.sqlite3'
)

def getResponse(message, chat_id):
    # ToDo: Add so the response is base on chat_id, with "generate_response"
    respone = bot.get_response(message)
    return str(respone)

def trainBot():
    bot.set_trainer(ChatterBotCorpusTrainer)
    bot.train(
        "chatterbot.corpus.english",
        'chatterbot.corpus.swedish'
    )
    return "Training done!\n"