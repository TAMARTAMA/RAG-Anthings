import pandas as pd
import json
import os

# Path to the chats.json file
CHATS_PATH = os.path.join(
    os.path.dirname(__file__),
    '..', 'project', 'chats.json'
)

# Load chat history from JSON
with open(CHATS_PATH, 'r', encoding='utf-8') as f:
    chats = json.load(f)

# Flatten messages for DataFrame
rows = []
for chat in chats:
    user_id = chat.get('userId', '')
    for msg in chat.get('messages', []):
        rows.append({
            'userId': user_id,
            'msgId': msg.get('id'),
            'role': msg.get('role'),
            'content': msg.get('content'),
            'timestamp': msg.get('timestamp'),
            'replyTo': msg.get('replyTo', None)
        })

# Create DataFrame
if rows:
    df = pd.DataFrame(rows)
    print(df)
else:
    print('No chat history found.')
