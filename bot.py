import amino
import json
import re

with open('params.json', 'r') as f:
    d = f.read()
    json_file = json.loads(d)
    STAFF_CHAT_ID = json_file['staff_chat']
    CLIENT_EMAIL = json_file['email']
    CLIENT_PASSWORD = json_file['password']
    AMINO_LINK = 'http://aminoapps.com/c/' + json_file['amino_name']

client = amino.Client()
client.login(email=CLIENT_EMAIL, password=CLIENT_PASSWORD)
AMINO_ID = client.get_from_code(AMINO_LINK).json
AMINO_ID = AMINO_ID['path'].split('/')[0]
AMINO_ID = re.sub('[A-Za-z]', '', AMINO_ID)
subclient = amino.SubClient(comId=AMINO_ID, profile=client.profile)

print('[SUCCESS] Bot connected!')

def getChats():
    chats = subclient.get_chat_threads()
    for name, id in zip(chats.title, chats.chatId):
        print(name, id)

@client.callbacks.event("on_text_message")
def on_text_message(data):
      msg = data.message.content.split()
      cmd = msg[0]
      if (cmd == '!question')and(len(msg) > 1):
        author = data.message.author.nickname
        linkto = client.get_from_id(objectId=data.message.author.userId, objectType=0, comId=AMINO_ID).fullUrl
        cnt = '-'
        cnt += " ".join(msg[ 1: ])
        res = f'{data.message.author.userId}\n[B]{author} asked a question: \n{cnt}\n \nLink to user: {linkto}'
        subclient.send_message(chatId=STAFF_CHAT_ID, message=res)
        subclient.send_message(chatId=data.message.chatId, message="Thank you for submitting your question! The staff will get to you ASAP!")
        print(f'[LOG] New question has been sent from {author}')
      else:
        subclient.send_message(chatId=data.message.chatId,
                               message='Incorrect usage of !question command!\n \nCorrect usage: !question <your question>')
      if cmd == '!listchats':

          """
          with this command you will be able to find the if of the chat you need
          just dm a bot command !listchats and look at the console in your IDE!
          """

          getChats()