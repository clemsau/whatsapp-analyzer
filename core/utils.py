import os
import pandas as pd
import re
import emoji
import datetime

from .conf.settings import UPLOAD_FOLDER


def create_upload_folder():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)


def starts_with_date(s):
    pattern = r'^(\d{1,2}\/\d{1,2}\/\d{2,4})\s(\d(?:\d)?:\d{2})\s-\s([^:]*):(.*?)(?=\s*\d{2}\/|$)'
    result = re.match(pattern, s)
    if result:
        return True
    else:
        return False


def is_media_only(s):
    pattern = r'(.*?)(\<)(.*?)(\>)$'
    result = re.match(pattern, s)
    if result:
        return True
    else:
        return False


def starts_with_author(s):
    patterns = [
        '([\w]+):',  # First Name
        '([\w]+[\s]+[\w]+):',  # First Name + Last Name
        '([\w]+[\s]+[\w]+[\s]+[\w]+):',  # First Name + Middle Name + Last Name
        '([+]\d{2} \d{5} \d{5}):',  # Mobile Number (India)
        '([+]\d{2} \d{3} \d{3} \d{4}):',  # Mobile Number (US)
        '([+]\d{2} \d{4} \d{7})',  # Mobile Number (Europe)
        '([+]\d{1,2} \d{1,2} \d{1,2} \d{1,2} \d{1,2})'
    ]
    pattern = '^' + '|'.join(patterns)
    result = re.match(pattern, s)
    if result:
        return True
    return False


def get_data_point(line):
    # line = 18/06/17, 22:47 - Loki: Why do you have 2 numbers, Banner?

    splitLine = line.split(' - ')  # splitLine = ['18/06/17, 22:47', 'Loki: Why do you have 2 numbers, Banner?']

    dateTime = splitLine[0]  # dateTime = '18/06/17, 22:47'

    date, time = dateTime.split(' ')  # date = '18/06/17'; time = '22:47'

    message = ' '.join(splitLine[1:])  # message = 'Loki: Why do you have 2 numbers, Banner?'

    if starts_with_author(message):  # True
        splitMessage = message.split(': ')  # splitMessage = ['Loki', 'Why do you have 2 numbers, Banner?']
        author = splitMessage[0]  # author = 'Loki'
        message = ' '.join(splitMessage[1:])  # message = 'Why do you have 2 numbers, Banner?'
    else:
        author = None
    return date, time, author, message


def parse_file(file_path):
    """Return a dataframe with the parsed whatsapp conversation which columns are: Date, Time, Author, Message"""
    parsedData = []  # List to keep track of data so it can be used by a Pandas dataframe
    conversationPath = file_path
    with open(conversationPath, encoding="utf-8") as fp:
        fp.readline()  # Skipping first line of the file (usually contains information about end-to-end encryption)

        messageBuffer = []  # Buffer to capture intermediate output for multi-line messages
        date, time, author = None, None, None  # Intermediate variables to keep track of the current message being processed

        while True:
            line = fp.readline()
            if not line:  # Stop reading further if end of file has been reached
                break
            line = line.strip()  # Guarding against erroneous leading and trailing whitespaces
            if starts_with_date(line):  # If a line starts with a Date Time pattern, then this indicates the beginning of a new message
                if not is_media_only(line):
                    if len(messageBuffer) > 0:  # Check if the message buffer contains characters from previous iterations
                        parsedData.append([date, time, author,
                                           ' '.join(
                                               messageBuffer)])  # Save the tokens from the previous message in parsedData
                    messageBuffer.clear()  # Clear the message buffer so that it can be used for the next message
                    date, time, author, message = get_data_point(line)  # Identify and extract tokens from the line
                    messageBuffer.append(message)  # Append message to buffer
            else:
                messageBuffer.append(line)  # If a line doesn't start with a Date Time pattern,
                # then it is part of a multi-line message. So, just append to buffer
    return pd.DataFrame(parsedData[1:], columns=['Date', 'Time', 'Author', 'Message'])


def dataframe_insight(dataframe):
    return {'total_message_count': len(dataframe),
            'total_word_count': total_word_count(dataframe)}


def total_word_count(dataframe):
    return dataframe['Message'].str.lower().str.split().apply(lambda l: len(l)).sum()


def conversation_age(dataframe):
    df = dataframe['Date'].apply(lambda d: datetime.datetime())
    return
