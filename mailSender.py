import smtplib
from email.mime.text import MIMEText
from email.utils import parseaddr


class InvalidEmailAddress(Exception):
    """Raise when email address could not be parsed
    """


def sendMail(text, address,
             mailFrom="arXivUpdate@nut.physik.uni-mainz.de",
             mailgateAddress="mailgate.zdv.uni-mainz.de:25"):
    msg = MIMEText(text)
    msg["Subject"] = "arXive update"
    msg["From"] = mailFrom
    if type(address) is list:
        for email in address:
            if parseaddr(email)[1] == "":
                raise InvalidEmailAddress
        msg["To"] = ",".join(address)
        to = address
    else:
        if parseaddr(address) == "":
            raise InvalidEmailAddress
        msg["To"] = address
        to = [address]
    s = smtplib.SMTP(mailgateAddress)
    s.sendmail(msg["From"], to, msg.as_string())
    s.quit()
