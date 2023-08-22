from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from collections import defaultdict
import re

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

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
                words = re.split(r'[\/\n, ]', kommentar[1])
                for word in words:
                    stripped_word = bokstaver(word.lower())
                    if stripped_word not in ignoredwords:
                        synonymcount[erstatt_med_første_ord(stripped_word)] += 1
            return dict(sorted(synonymcount.items(), key=lambda item: item[0], reverse=True))




        grouped_by_bydel = defaultdict(list)
        for kommentar in filtered_array:
            grouped_by_bydel[kommentar[0]].append(kommentar)

        sorted_grouped_and_counted = count_words(filtered_array)
        synonymer_opptellt = tell_synonymer(filtered_array)

        bydel_wordcounts = defaultdict(lambda: defaultdict(int))
        for bydel, kommentarer in grouped_by_bydel.items():
            bydel_wordcounts[bydel] = tell_synonymer(kommentarer)

        sorted_bydel_wordcounts = {}
        for bydel, synonymcount in bydel_wordcounts.items():
            sorted_bydel_wordcounts[bydel] = synonymcount

        # print(dict(grouped_by_bydel))
        antall_elementer = len(synonymer_opptellt)
        slutt_indeks = antall_elementer
        antall_hopp = 0

        for ord in reversed(list(synonymer_opptellt.keys())):
            if antall_hopp > slutt_indeks:
                antall_hopp += 1
                continue
            antall = synonymer_opptellt[ord]
            if antall > 5:
                print(f"Ord: {ord}, Antall: {antall}")

        # for bydel, wordcount in sorted_bydel_wordcounts.items():
        #     print(f"Ordtelling for {bydel}:")
        #     for word, count in wordcount.items():
        #         if count > 1:
        #             print(f"{word}: {count}")
        #     print("\n")

    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()
