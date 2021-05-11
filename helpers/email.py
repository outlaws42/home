from smtplib import SMTP

class Mail():

  def mail(
    body: str, 
    subject: str,
    send_to: list,
    login: list
    ):
    """
    body = Body of the message, subject = The subject,
    send_to = Who you want to send the message to,
    login = The login information for email.
    Requires from smtplib import SMTP
    """
    us, psw = login
    message = f'Subject: {subject}\n\n{body}'
    print(message)
    try:
      mail = SMTP('smtp.gmail.com', 587)
      mail.ehlo()
      mail.starttls()
      mail.ehlo()
      mail.login(us, psw)
      mail.sendmail(us,send_to, message)
      mail.close()
      print('Successfully sent email')
    except Exception as e:
      print('Could not send email because')
      print(e)