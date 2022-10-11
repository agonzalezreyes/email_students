# Script to send grades to students 

* Requirements: At least Python 3.7
* Tested with Python 3.9

### Setup
    pip install -r requirements.txt
    cp .env.template .env

Fill the `.env` variables which are the following:

    GOOGLE_SHEET_URL= # the url to the google sheet
    SENDER_EMAIL= # sender email
    SENDER_PW= # sender password 
    SMTP_SERVER_NAME= # smtp-mail.outlook.com for stanford.edu email 
    SMTP_SERVER_PORT= # 587 

### Usage 

Arguments required:

    --assignment      Name of the assignment, e.g. `Assignment 1`, to be included in the email body and subject line.
    --grade_column    The column name that corresponds to the assignment column grade, e.g. `A1 grade`

To send emails, pass the `--notify` flag:

    python email_students.py --assignment="Assignment 1" --grade_column="A1 grade" --notify

### Notes
* By default, it will only send email if grade value is not `NaN`.

For more information run: `python email_students.py --help`