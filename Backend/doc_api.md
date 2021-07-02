# Account

    - create user: post
        + username, email, password, avartar, full_name
        + account/create-user/
    - log in: post
        + username, password
        + account/login/
    - check login: get
        + sent access token
        + account/check-login/
    - get all user: get
        + sent access token of admin
        + account/get-all/

# Chatbot

    - get response of bot: post
        + text
        + get-response/
    - get all chat content: get
        + No args in funtion
        + get-chat/
