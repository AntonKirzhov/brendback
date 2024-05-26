import smtplib

print(0)
smtpObj = smtplib.SMTP('mail.hosting.reg.ru', 587)
print(1)
smtpObj.starttls()
print(2)
smtpObj.login('mailing@brendboost.ru','mailingboost.')
print(3)
try:
    smtpObj.sendmail("mailing@brendboost.ru","tosha.nesterenko206@yandex.com","Test hello!")
    print(5)
except Exception as e:
    print(e)
    pass