# IUH_Chatbot
chat-bot-rasa
Run
rasa run --endpoints endpoints.yml --credentials credentials.yml & rasa run actions

rasa run -m models --enable-api --cors "*" & rasa run actions

Refresh localhost 5005
fuser -k 5005/tcp
