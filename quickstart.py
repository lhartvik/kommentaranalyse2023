from __future__ import print_function

import os.path
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from collections import defaultdict
import re

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

with open('spredsheetId.txt', 'r') as file:
    spreadsheetid = [line.strip() for line in file.readlines()]
# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = spreadsheetid[0]
SAMPLE_RANGE_NAME = 'Ark 1!C2:M2000'

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

        with open('synonymliste.txt', 'r') as file:
            synonymliste = [linje.strip() for linje in file.readlines()]

        allesynonymer = [linje.split(', ') for linje in synonymliste]

        with open('words.txt', 'r') as file:
            ignoredwords = [line.strip() for line in file.readlines()]

        with open('bydeler.txt', 'r') as file:
            bydeler = [line.strip().lower() for line in file.readlines()]

        flattened_array = [[row[0].lower(), row[j] if len(row) > j else ''] for row in values for j in range(3, 11)]
        filtered_array = [row for row in flattened_array if all(cell.strip() for cell in row) and row[0] in bydeler]
        # filtered_array = [row for row in flattened_array if all(cell.strip() for cell in row)]

        # print('Bydel, kommentar:')
        # for row in filtered_array:
        #     print('%30s \t %s' % (row[0], row[1]))


        # Stripper vekk alle tegn som ikke er bokstaver
        def bokstaver(input_string):
            return re.sub(r'[^a-zæøå]', '', input_string)

        def bokstaverogmellomrom(input_kommentar):
            return re.sub(r'[^a-zæøå\s]', '', re.sub(r'[()]', ' ', input_kommentar))

        def erstatt_med_første_ord(ord):
            for synonymer in allesynonymer:
                if ord in synonymer:
                    return synonymer[0]
            return ord

        # Tar inn en slik array [["bydel"], ["en setning om hva som bør prioriteres"]]
        # Returnerer en array [["en", 10], ["setning",3]...]
        def count_words(data):
            wordcount = defaultdict(int)
            for kommentar in data:
                words = kommentar[1].split()
                for word in words:
                    if bokstaver(word.lower()) not in ignoredwords:
                        wordcount[bokstaver(word.lower())] += 1
            return dict(sorted(wordcount.items(), key=lambda item: item[1], reverse=True))
            # return dict(sorted(wordcount.items(), key=lambda item: item[0], reverse=True))

        def tell_synonymer(data):
            synonymcount = defaultdict(int)
            for kommentar in data:
                words = re.split(r'[/\n, ]', kommentar[1])
                for word in words:
                    stripped_word = bokstaver(word.lower())
                    if stripped_word not in ignoredwords:
                        synonymcount[erstatt_med_første_ord(stripped_word)] += 1
            return dict(sorted(synonymcount.items(), key=lambda item: item[1], reverse=True))

        grouped_by_bydel = defaultdict(list)
        for kommentar in filtered_array:
            grouped_by_bydel[kommentar[0]].append(kommentar)

        bydel_wordcounts = defaultdict(lambda: defaultdict(int))
        for bydel, kommentarer in grouped_by_bydel.items():
            bydel_wordcounts[bydel] = tell_synonymer(kommentarer)

        sorted_bydel_wordcounts = {}
        for bydel, synonymcount in bydel_wordcounts.items():
            sorted_bydel_wordcounts[bydel] = synonymcount

        # Lag en ordbok for å lagre ord og synonymer
        ord_synonymer = {}
        for ord_gruppe in allesynonymer:
            hovedord = ord_gruppe[0]
            synonymer = ord_gruppe[1:]
            ord_synonymer[hovedord] = synonymer

        # Ordbok for å samle kommentarer etter bydel, ord og synonym
        resultat = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

        for bydel, ordliste in sorted_bydel_wordcounts.items():
            for ordet in ordliste:
                synonymer = ord_synonymer.get(ordet, [])
                synonymer.append(ordet)
                for kommentar_bydel, kommentar in flattened_array:
                    if kommentar_bydel == bydel:
                        kommentarlower = bokstaverogmellomrom(kommentar.lower())
                        for synonym in synonymer:
                            if f" {synonym} " in f" {kommentarlower} " or f" {ordet} " in f" {kommentarlower} ":
                                if kommentar not in resultat[bydel][ordet]["kommentarer"]:
                                    resultat[bydel][ordet]["kommentarer"].append(kommentar)

        for bydel, ordliste_data in resultat.items():
            bydel_array = []
            bydeler_sheet = create(creds, bydel)
            for ordet, kommentar_data in ordliste_data.items():
                kommentar_array = []

                for kommentar in kommentar_data["kommentarer"]:
                    kommentar_array.append([kommentar])

                if len(kommentar_array) > 0:
                    bydel_array.extend([[" "], [f"{ordet}"]])
                    bydel_array.extend(kommentar_array)
            append_values(creds, bydeler_sheet, f"A1:A1", "USER_ENTERED", bydel_array)

    except HttpError as err:
        print(err)


def create(creds, bydel):
    # pylint: disable=maybe-no-member
    try:
        service = build('sheets', 'v4', credentials=creds)
        spreadsheet = {
            'properties': {
                'title': f"bydel-{bydel}-{datetime.datetime.now()}"
            }
        }
        spreadsheet = service.spreadsheets().create(body=spreadsheet,
                                                    fields='spreadsheetId') \
            .execute()
        print(f"Spreadsheet ID: {(spreadsheet.get('spreadsheetId'))}")
        return spreadsheet.get('spreadsheetId')
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


def append_values(creds, spreadsheet_id, range_name, value_input_option,
                  _values):
    # pylint: disable=maybe-no-member
    try:
        service = build('sheets', 'v4', credentials=creds)

        values = _values
        body = {
            'values': _values
        }
        result = service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id, insertDataOption="INSERT_ROWS",
            range="A1:M1",
            valueInputOption=value_input_option, body=body).execute()
        print(f"{(result.get('updates').get('updatedCells'))} cells appended.")
        return result

    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


if __name__ == '__main__':
    main()
