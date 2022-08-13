import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import configparser
from datetime import datetime

def get_config_vals():
    config = configparser.ConfigParser()
    config.read("settings.env")

    sender_email = config["SenderAccountInfo"]["EMAIL"]
    sender_name = config["SenderAccountInfo"]["NAME"]
    cc = config["SenderAccountInfo"]["CC"]
    app_password = config["SenderAccountInfo"]["APP_PASSWORD"]

    receiver_first_name = config["ReceiverAccountInfo"]["FIRST_NAME"]
    receiver_last_name = config["ReceiverAccountInfo"]["LAST_NAME"]
    receiver_email = config["ReceiverAccountInfo"]["EMAIL"]

    return {
        "sender_email": sender_email,
        "sender_name": sender_name,
        "cc": cc,
        "app_password": app_password,
        "receiver_first_name": receiver_first_name,
        "receiver_last_name": receiver_last_name,
        "receiver_email": receiver_email,
    }


CONFIG_VALS = get_config_vals()


def get_mail_subject():
    return "Testing Automated Emails"


def get_mail_body(receiver_first_name: str, sender_name: str):
    msg_body = f"Dear {receiver_first_name}, \nThis email was automatically sent using Python. \n" \
               f"Hope you like it. \n Cheers, \n {sender_name}  "
    return msg_body


def get_email_attachment(file_name: str = "test_image.png"):
    file_path = "../assets/"
    attachment_file = file_path + file_name
    return attachment_file


def prepare_email(receiver_first_name: str, receiver_email: str, sender_name: str, sender_email: str, cc: str = ""):
    email = MIMEMultipart()
    email["From"] = sender_email
    email["To"] = receiver_email
    email["Subject"] = get_mail_subject()
    email["Cc"] = cc
    email_body = get_mail_body(receiver_first_name, sender_name)

    # Add body and attachment to email
    email.attach(MIMEText(email_body, "html"))

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    attachment_file_name = "test_image.png"
    attachment = open(get_email_attachment(), "rb")

    # To change the payload into encoded form
    p.set_payload(attachment.read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % attachment_file_name)

    # attach the instance 'p' to instance 'msg'
    email.attach(p)

    return email.as_string()


def send_email(first_name: str = CONFIG_VALS["receiver_first_name"], last_name: str = CONFIG_VALS["receiver_last_name"],
               receiver_email: str = CONFIG_VALS["receiver_email"]):
    # Create SMTP session for sending the mail
    # use gmail with port
    session = smtplib.SMTP('smtp.gmail.com', 587)
    # enable security
    session.starttls()
    # login with mail_id and password

    session.login(CONFIG_VALS["sender_email"], CONFIG_VALS["app_password"])
    text = prepare_email(first_name, receiver_email, CONFIG_VALS["sender_name"], CONFIG_VALS["sender_email"],
                         CONFIG_VALS["cc"])
    session.sendmail(CONFIG_VALS["sender_email"], receiver_email, text)
    session.quit()
    print(f"Mail Sent to {first_name} {last_name} at {receiver_email} at {datetime.now()}")


if __name__ == "__main__":
    send_email(CONFIG_VALS["receiver_first_name"], CONFIG_VALS["receiver_last_name"], CONFIG_VALS["receiver_email"])
