import uvicorn
if __name__ == '__main__':
    uvicorn.run("app.main:app", port=8000, host='0.0.0.0', reload=True, ssl_keyfile="/etc/letsencrypt/live/dev.brendboost.ru/privkey.pem", ssl_certfile="/etc/letsencrypt/live/dev.brendboost.ru/fullchain.pem")