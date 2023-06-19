# send_email.py
# 2023-06-18 | CR

# https://realpython.com/python-send-email/

from os import environ
from os.path import basename
import smtplib
import ssl
import argparse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import COMMASPACE, formatdate


def send_email(sender_email, receiver_email, subject, text,
               html, files=[], debug=None):
    smtp_server = environ.get('SMTP_SERVER')
    smtp_port = environ.get('SMTP_PORT')  # For starttls
    smtp_user = environ.get('SMTP_USER')
    smtp_password = environ.get('SMTP_PASSWORD')
    if sender_email is None or sender_email.strip() == '':
        sender_email = environ.get('SMTP_DEFAULT_SENDER')

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message['To'] = COMMASPACE.join(receiver_email)
    message['Date'] = formatdate(localtime=True)

    # Turn these into plain/html MIMEText objects
    body_plain_text = MIMEText(text, "plain")
    if html:
        body_html = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(body_plain_text)
    if html:
        message.attach(body_html)

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        message.attach(part)

    if debug:
        print(f'smtp_server: {smtp_server}')
        print(f'smtp_port: {smtp_port}')
        print(f'smtp_user: {smtp_user}')
        print(f'smtp_password: {"*" * len(smtp_password)}')
        # print(f'smtp_password: {smtp_password}')
        print(f'sender_email: {sender_email}')
        print(f'receiver_email: {receiver_email}')
        print(f'subject: {subject}')
        print(f'text: {text}')
        print(f'html: {html}')
        print(f'file_path: {files}')

    # Create a secure SSL context
    context = ssl.create_default_context()
    # Try to log in to smtp server and send email
    try:
        smtp = smtplib.SMTP(smtp_server, smtp_port)
        # smtp.ehlo()  # Can be omitted
        smtp.starttls(context=context)  # Secure the connection
        # smtp.ehlo()  # Can be omitted
        smtp.login(smtp_user, smtp_password)
    except Exception as e:
        # Print any error messages to stdout
        print(f'Send_Email ERROR (preparing phase): {e}')
        return False
    try:
        smtp.sendmail(sender_email, receiver_email, message.as_string())
    except Exception as e:
        # Print any error messages to stdout
        print(f'Send_Email ERROR (sending phase): {e}')
    finally:
        smtp.close()
    return True


def init_parser():
    parser = argparse.ArgumentParser(
        description='Send an email'
    )
    parser.add_argument(
        "-D", "--debug",
        action="store_true",
        required=False,
        help="Show debug information",
    )
    parser.add_argument(
        "-f", "--sender",
        default='',
        required=False,
        help="Sender email",
    )
    parser.add_argument(
        "-t", "--to",
        nargs='+',
        default=[],
        required=True,
        help="Destination emails (separated by blanks)",
    )
    parser.add_argument(
        "-s", "--subject",
        nargs='+',
        default=[],
        required=True,
        help="Email subject",
    )
    parser.add_argument(
        "-m", "--message",
        nargs='+',
        default=[],
        required=False,
        help="Message (plain text)",
    )
    parser.add_argument(
        "-a", "--attachments",
        nargs='+',
        default=[],
        required=False,
        help="Attachments (filespecs separated by blanks)",
    )
    return parser


def main():
    parser = init_parser()
    args = parser.parse_args()

    send_email(
        args.sender,
        args.to,
        ' '.join(args.subject),
        ' '.join(args.message),
        None,
        args.attachments,
        args.debug
    )
    return


if __name__ == "__main__":
    main()
