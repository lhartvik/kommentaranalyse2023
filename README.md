# Prosjektnavn

Velkommen til Kommentaranalyse 2023! Dette programmet bruker Google Sheets API for å lese et regneark fra 
docs.google.com og deler dette inn i bydeler. Følg trinnene nedenfor for å komme i gang.

## Installasjon og kjøring

Følg disse trinnene for å sette opp og kjøre programmet:

1. **Klon repoet:**

Åpne terminalen og naviger til ønsket mappe. Deretter kjør følgende kommando for å klone dette Git-repoet:

```sh
   git clone https://github.com/lhartvik/kommentaranalyse2023.git
   cd kommentaranalyse2023
```

2. **Installer avhengigheter**
   
Sørg for at du har Python 3.x installert. Deretter kan du installere avhengigheter ved hjelp av pip:
```sh
   pip install -r requirements.txt
```

3. **Opprett credentials.json**

https://developers.google.com/sheets/api/quickstart/python

4. **Finn IDen til regnearket**

Eksempel: https://docs.google.com/spreadsheets/d/1oNjnO19NpeHRMcYra53DQN55uRnjIOz4-2U8KK5miwI/edit#gid=0
Da er IDen det som er imellom /d/ og /edit, i eksempelet '1oNjnO19NpeHRMcYra53DQN55uRnjIOz4-2U8KK5miwI'

Denne skal inn i quickstart.py på linje 16 SAMPLE_SPREADSHEET_ID = 'regneark-id'

6. **Kjør programmet**

Nå skal alt være klart for å kjøre programmet:
  ```sh
  python3 quickstart.py
```
## Kontakt
Hvis du har spørsmål, forslag eller innspill kan du sende epost til lhartvik@gmail.com eller opprette en Issue på https://github.com/lhartvik/kommentaranalyse2023/issues
