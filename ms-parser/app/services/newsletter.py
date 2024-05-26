import pyrogram
from pyrogram import Client
from pyrogram.errors import FloodWait
from app.database.mysql import MysqlManager
import logging
import smtplib
import asyncio
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
logging.basicConfig(level=logging.ERROR)


pyrogram_app = Client(name="newsletter", api_id=25161896, api_hash="51b2b63b2521ae5e58493cc31307fd64")

async def get_user_by_id(user_id: str):
    await MysqlManager.db.ping()
    query = await MysqlManager.cursor.execute(f"SELECT `_id`, `selected_company` FROM `users` WHERE `_id` = '{user_id}'")
    result = await MysqlManager.cursor.fetchall()
    return result[0]

async def delete_newsletters(user_id, newsletter_ids):
    await MysqlManager.db.ping()
    await MysqlManager.cursor.execute(f"DELETE FROM `newsletters` WHERE `user_id` = '{user_id}' AND `_id` IN ({newsletter_ids})")
    await MysqlManager.db.commit()

async def create_newsletter(user_id, name, to, text, letter_type):
    await MysqlManager.db.ping()
    user = await get_user_by_id(user_id)
    await MysqlManager.cursor.execute(f"INSERT INTO `newsletters` (`user_id`, `name`, `text`, `users_to`, `type`, `company`) VALUES ('{user_id}', '{name}', '{text}', '{to}', '{letter_type}', '{user['selected_company']}')")
    await MysqlManager.db.commit()
    query = await MysqlManager.cursor.execute(f"SELECT * FROM `newsletters` WHERE `_id` = '{MysqlManager.cursor.lastrowid}'")
    result = await MysqlManager.cursor.fetchall()
    return result

async def send_telegram(to, text):
    await pyrogram_app.start()
    for login in to.split(";"):
        try:
            chat = await pyrogram_app.get_chat(login)
            chat_id = chat.id
            await pyrogram_app.send_message(chat_id, text)
        except Exception as e:
            print(e)
            pass
    await pyrogram_app.stop()

async def send_email(to, text):
    smtpObj = smtplib.SMTP('sm8.hosting.reg.ru', 587)
    smtpObj.starttls()
    smtpObj.login('mailing@brendboost.ru','brendboostmailing.!')

    for email in to.split(";"):
        try:
            smtpObj.sendmail("mailing@brendboost.ru",email,text.encode('utf8'))
        except Exception as e:
            print(e)
            pass
    smtpObj.quit()

async def send_whatsapp(to, text):
    options = webdriver.ChromeOptions()
    options.add_argument('--allow-profiles-outside-user-dir')
    options.add_argument('--enable-profile-shortcut-manager')
    options.add_argument(r'user-data-dir=/root/DEV/ms-parser/app/services/profilechrome')
    options.add_argument('--profile-directory=Profile 1')
    options.add_argument('--profiling-flush=n')
    options.add_argument('--enable-aggressive-domstorage-flushing')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 30)
    for number in to.split(";"):
        url = f"https://web.whatsapp.com/send?phone={number}&text={text}"
        driver.get(url)
        wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[5]/div/footer/div[1]/div/span[2]/div/div[2]/div[2]/button')))
        driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[5]/div/footer/div[1]/div/span[2]/div/div[2]/div[2]/button').click()
        await asyncio.sleep(5)

async def get_history(user_id):
    await MysqlManager.db.ping()
    user = await get_user_by_id(user_id)
    query = await MysqlManager.cursor.execute(f"SELECT * FROM `newsletters` WHERE `user_id` = '{user_id}' AND `company` = '{user['selected_company']}'")
    result = await MysqlManager.cursor.fetchall()

    return result