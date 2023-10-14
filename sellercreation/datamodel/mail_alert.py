import smtplib

def welcome_mail(username, email):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("shantanushuklacse2017@gmail.com", "ixxuzmefsujnemdd")
    msg_header = 'From: Sender Name <sender@server>\n' \
                 'To: Receiver Name <receiver@server>\n' \
                 'Cc: Receiver2 Name <receiver2@server>\n' \
                 'MIME-Version: 1.0\n' \
                 'Content-type: text/html\n' \
                 'Subject: Any subject\n'

    Subject = 'Welcome'
    msg_content = """<h2>Hi {}, Welcome To QBITZ</h2>""".format(username)
    msg_full = (''.join([msg_header, msg_content])).encode()
    server.sendmail(email, "shuklakrshantanu@gmail.com", msg_full)
