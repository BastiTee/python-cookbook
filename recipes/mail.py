import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate


def send_mail(sender, receiver, subject, body, username, password, host,
              attachment=None, port=465):
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach(MIMEText(body))
    if attachment:
        with open(attachment, "rb") as fil:
            part = MIMEApplication(fil.read(), Name=basename(attachment))
        part['Content-Disposition'] = (
            'attachment; filename="%s"' % basename(attachment))
        msg.attach(part)

    server = smtplib.SMTP_SSL(host, port)
    server.ehlo()
    server.login(username, password)
    server.sendmail(sender, receiver, msg.as_string())
    server.close()


if __name__ == '__main__':
    from argparse import ArgumentParser
    from sys import exit
    prs = ArgumentParser(description='Python SMTP email client.')
    prs.add_argument('-f', metavar='FROM', help='Sender e-mail')
    prs.add_argument('-t', metavar='TO', help='Receiver e-mail')
    prs.add_argument('-s', metavar='SUBJECT', help='E-mail subject')
    prs.add_argument('-m', metavar='MSG', help='E-mail message')
    prs.add_argument('-a', metavar='FILEPATH', help='Attached file')
    prs.add_argument('-u', metavar='USER', help='Login username')
    prs.add_argument('-p', metavar='PASSWORD', help='Login password')
    prs.add_argument('-d', metavar='SMTPHOST', help='SMTP hostname')
    args = prs.parse_args()
    if (not args.f or not args.t or not args.s or not args.m
            or not args.u or not args.p or not args.d):
        prs.print_help()
        exit(1)
    send_mail(args.f, args.t, args.s, args.m, args.u, args.p, args.d, args.a)
