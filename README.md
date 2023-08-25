# Kommentaranalyse 2023

Velkommen til Kommentaranalyse 2023! Dette programmet bruker Google Sheets API for å lese et regneark fra 
[docs.google.com](https://docs.google.com/spreadsheets/).  Stedsnavn skal ligge i kolonne C og kommentarer skal ligge i F,G,H,I,J,K,L,M. Alle kommentarer blir lest inn, 
og alle ord telles for hver bydel. Deretter opprettes et regneark for hver bydel, hvor de ordene eller synonymbegrepene som er nevnt oftest listes opp først. 
Begreper eller ord som bare forekommer 1 gang blir ikke skrevet inn i regnearket til bydelene.
Følg trinnene nedenfor for å komme i gang.

## Installasjon og kjøring

Følg disse trinnene for å sette opp og kjøre programmet:

1. **Klon repoet:**

Åpne terminalen og naviger til ønsket mappe. Kjør deretter følgende kommando for å klone dette Git-repoet:

```sh
   git clone https://github.com/lhartvik/kommentaranalyse2023.git
   cd kommentaranalyse2023
```

2. **Installer avhengigheter**
   
Sørg for at du har Python 3.x installert. https://www.python.org/downloads/

Deretter må avhengigheter installeres ved hjelp av pip:
```sh
   pip3 install -r requirements.txt
```

3. **Opprett credentials.json**

Denne fila kan du følge guiden og opprette selv eller få fra en annen som har opprettet den og som du stoler på. Her er guiden for å opprette den:
https://developers.google.com/sheets/api/quickstart/python
OBS: Viktig at man legger inn brukernavnet på den som har tilgang til dokumentet også, i OAuth consent screen, test users!
credentials.json skal ligge i samme katalog som quickstart.py

4. **Finn IDen til regnearket**

Eksempel: https://docs.google.com/spreadsheets/d/1oNjnO19NpeHRMcYra53DQN55uRnjIOz4-2U8KK5miwI/edit#gid=0
Da er IDen det som er imellom /d/ og /edit, i eksempelet '1oNjnO19NpeHRMcYra53DQN55uRnjIOz4-2U8KK5miwI'

Denne skal inn som første linje i spreadsheetId.txt

5. **Slett token.json**

Hvis du har en token.json som er eldre enn en viss tid(jeg tror 1 uke) så vil den gi feilmelding om at den er for gammel. 
Den bør da slettes, slik at man logger inn i google docs på nytt og får en ny token.

6. **Rediger filene for synonymer og ignorerte ord**

synonymliste.txt inneholder lister med synonymer. Ordene på hver linje telles sammen, når man vil finne hvilke politiske begreper som det er mye interesse for i hver bydel. 
words.txt er en liste med ord som ikke skal telles. Oppdager du ord som ikke er politiske temaer/begreper kan de legges inn her.
bydeler.txt kan evt. redigeres for å legge til eller fjerne bydeler/steder/byer som skal leses. Jeg har lagt inn 15 bydeler i Oslo.

7. **Kjør programmet**

Nå skal alt være klart for å kjøre programmet:
  ```sh
  python3 quickstart.py
```
## Kontakt
Hvis du har spørsmål, forslag eller innspill kan du sende epost til lhartvik@gmail.com eller opprette en Issue på https://github.com/lhartvik/kommentaranalyse2023/issues
