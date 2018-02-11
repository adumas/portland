from gmail_message import Gmail
from gmail_message import Message

G = Gmail()
test = G.search_messages('subject: "Re: Portland"')
raw_message = G.get_raw_message(test[2]['id'])
msg = Message(raw_message)
print msg


messageList = []
for msg in test[:10]:
    print msg['id']
    messageList.append(G.get_message(msg['id']))
