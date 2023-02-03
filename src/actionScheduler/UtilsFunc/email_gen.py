import email
import os
import smtplib
import random
import sys
import time

# Path to directory where attachments will be stored:
#PATH = os.getcwd() # "C:/Users/gt/Documents/email_generator/"
PATH = dirpath = os.path.dirname(__file__)

def caption(origin):
    """Extracts: To, From, Subject and Date from email.Message() or mailbox.Message()
    origin -- Message() object
    Returns tuple(From, To, Subject, Date)
    If message doesn't contain one/more of them, the empty strings will be returned.
    """
    send_date = ""
    if origin.__contains__("date"):
        send_date = origin["date"].strip()
    sender = ""
    if origin.__contains__("from"):
        sender = origin["from"].strip()
    recipient = ""
    if origin.__contains__("to"):
        recipient = origin["to"].strip()
    subject = ""
    if origin.__contains__("subject"):
        subject = origin["subject"].strip()
    return sender, recipient, subject, send_date


def extract(chosen_file):
    """Extracts all data from e-mail, including From, To, etc., and returns it.
    chosen_file -- A file-like readable object
    """
    m = email.message_from_binary_file(chosen_file)
    sender, recipient, subject, send_date = caption(m)
    return sender


def rand_server():
    """
    Select random email server to send emails to
    """
    file_name = os.path.join(PATH, "server_list.txt")
    with open(file_name) as file:
        server = file.read().splitlines()
        return random.choice(server)


def rand_user(email_server):
    """
    Select random email address to send emails to
    """
    file_name = os.path.join(PATH, email_server)
    with open(file_name) as file:
        user = file.read().splitlines()
        return random.choice(user)


def send_mail(email_server):
    """
    Send email out to specified IP address
    """
    port = 25

    recipient = rand_user(email_server)
    email_destination = "192.168.56.10"  # email_server[0:-4]
    email_bank = os.path.join( PATH, 'email_bank')
    #PATH + "./email_bank/"
    selected_file = os.path.join(email_bank, random.choice(os.listdir(email_bank)))
    #email_bank + random.choice(os.listdir(email_bank))  # select random eml file to send

    with open(selected_file, "rb") as file:
        message = file.read()
        sender = extract(file)

    # smtp = None <-- used ONLY is finally line below is used
    try:
        smtp = smtplib.SMTP(email_destination, port)
        smtp.sendmail(sender, recipient, message)
    except Exception as e:
        print('Failed to send mail.')
        #print(str(e))
        pass
    else:
        print('Succeeded to send mail.')
        pass
    # finally:
    #     if smtp is not None:
    #         smtp.close()


def rand_intensity(intensity_level):
    """
    random generate intensity of email send
    """
    intensity = 0
    if intensity_level == "1":
        # random between 1 packet to 20 packets
        intensity = random.randint(1, 20)
    if intensity_level == "2":
        # random between 20 packets to 70 packets
        intensity = random.randint(20, 70)
    if intensity_level == "3":
        # random between 50 packets to 100 packets
        intensity = random.randint(70, 150)
    if intensity_level == "9":
        # random between 1 packet to 200 packets
        intensity = random.randint(1, 200)

    return intensity


def rand_sleep(sleep_level):
    """
    randomly generate sleep time between email send
    """
    sleep_time = 0
    if sleep_level == "1":
        # random between 120s to 180s
        sleep_time = random.randint(120, 180)
    if sleep_level == "2":
        # random between 60s (1 minutes) to 120s (2 minutes)
        sleep_time = random.randint(60, 120)
    if sleep_level == "3":
        # random between 1s to 60s (1 minute)
        sleep_time = random.randint(1, 60)
    if sleep_level == "9":
        # random between 1s to 300s (5 minutes)
        sleep_time = random.randint(1, 180)

    return sleep_time


def test():
    #intensity_level = sys.argv[1]
    #sleep_level = sys.argv[2]

    while True:
        #intensity = rand_intensity(intensity_level)
        #sleep_time = rand_sleep(sleep_level)
        intensity = 1
        sleep_time = 0  # do not sleep
        print(f"intensity: {intensity}")

        for counter in range(intensity):

            email_server = "mail.poople.com.txt"
            send_mail(email_server)
        print(f"sleep: {sleep_time}")

        time.sleep(sleep_time)


def main():
    #intensity_level = sys.argv[1]
    #sleep_level = sys.argv[2]

 #   while True:
        #intensity = rand_intensity(intensity_level)
        #sleep_time = rand_sleep(sleep_level)
        intensity = 3000 # send 3000 times
        sleep_time = 0  # do not sleep
        for counter in range(intensity):
            email_server = "mail.gt.org.txt" # rand_server()
            send_mail(email_server)

        time.sleep(sleep_time)


if __name__ == '__main__':
    main()
