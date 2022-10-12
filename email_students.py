from email.policy import default
import smtplib, ssl
import os
import re
import pandas as pd
import numpy as np
import click
from dotenv import load_dotenv
load_dotenv()

SHEET_URL: str = os.getenv('GOOGLE_SHEET_URL')
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PW = os.getenv('SENDER_PW')
SERVER_NAME = os.getenv('SMTP_SERVER_NAME')
SERVER_PORT: int = os.getenv('SMTP_SERVER_PORT')

def export_url(sharing_url: str) -> str:
    '''
    Convert url from Google sheets sharing mode to readable csv format
    '''
    
    return re.sub(r'/edit.*', '/export?format=csv', sharing_url)

message = """Subject: Your {assignment} grade

Hi, 

Your grade for {assignment} is {grade}.

Contact us if you have any questions.

Best,

CS339H Team
cs339h-aut2223-staff@lists.stanford.edu
"""

@click.command()
@click.option(
    "--assignment",
    "-a",
    required=True,
    type=str,
    help="Name of the assignment, e.g. `Assignment 1`, to be included in the email body and subject line."
)
@click.option(
    "--grade_column",
    "-g",
    required=True,
    type=str,
    help="The column name that corresponds to the assignment column grade, e.g. `A1 grade`"
)
@click.option(
    "--email_column",
    "-e",
    required=False,
    default="Email",
    type=str,
    help="The column name that corresponds to the assignment column grade, e.g. `Email`",
)
@click.option(
    "--notify",
    "-n",
    is_flag=True,
    help="By default, the script will not send emails unless this is passed.",
)

def main(assignment, grade_column, email_column, notify):
    csv_export_url = export_url(SHEET_URL)
    print(csv_export_url)
    df = pd.read_csv(csv_export_url)
    df = df.loc[:, [email_column, grade_column]] 

    if not (
        notify
        and click.confirm(f"Are you sure you want to email students?")
    ):
        click.echo("Aborting.")
        return

    context = ssl.create_default_context()
    with smtplib.SMTP(SERVER_NAME, SERVER_PORT) as server:
        server.ehlo() # identify to smtp client
        server.starttls(context=context) # secure email with tls encryption & context
        server.ehlo() # re-identify as an encrypted connection
        server.login(SENDER_EMAIL, SENDER_PW)

        for _, row in df.iterrows():
            student_email = row[email_column]
            student_grade = row[grade_column]
            if not np.isnan(student_grade):
                click.echo(f"Sending email to student {student_email}...")
                server.sendmail(
                    SENDER_EMAIL, # from address
                    student_email, # to address
                    message.format(grade=student_grade, assignment=assignment),
                )
                click.echo("... sent!")

        click.echo(f"Done sending emails.")

if __name__ == "__main__":
    main()