# IUH_Chatbot

chat-bot-rasa
Run
rasa run --endpoints endpoints.yml --credentials credentials.yml & rasa run actions

rasa run -m models --enable-api --cors "\*" & rasa run actions

Refresh localhost 5005
fuser -k 5005/tcp

# Run server

## download models

-   pip3 install gdown
-   gdown --id 1JwXcUJeLzQQFNg_k_PkV-7Aln_0Hfvxj
-   unzip models.zip
-   move models to Backend/API/
