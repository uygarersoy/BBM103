def mail_checker(mail):
    if "@" in mail and mail.count(".") >= 1:
        return True
    else:
        return False

mail = input("Enter your e-mail address: ")
print(f"This e-mail address is {mail_checker(mail)}")