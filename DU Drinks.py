import requests

# 1. stiahnem data z netu
url = "https://boozeapi.com/api/v1/cocktails"
response = requests.get(url)
data = response.json()

# 2. ziskam zoznam drinkov
cocktails = data['data']

# 3. pripravim si drinky co hladam
pocet_vodka = 0
pocet_gin = 0
pocet_rum = 0

# 4. Prejdem vsetky drinky
for drink in cocktails:
    obsahuje_vodku = False
    obsahuje_gin = False
    obsahuje_rum = False

    # prejdem ingrediencie
    for ingredient in drink['ingredients']:
        # Zmenim nazov na male pismena, aby som nasiel "Vodka" aj "vodka"
        nazov_ingrediencie = ingredient['name'].lower()
        
        # Ak najdem v nazve vodku, zapamatam si to
        if "vodka" in nazov_ingrediencie:
            obsahuje_vodku = True
        
        # To iste pre gin
        if "gin" in nazov_ingrediencie:
            obsahuje_gin = True
            
        # A to iste pre rum
        if "rum" in nazov_ingrediencie:
            obsahuje_rum = True

    # 5. Ak som nasialkohol, pripocitam ho k celkovemu poctu
    # (Robim to az tu, aby som jeden drink nepocital dvakrat)el 
    if obsahuje_vodku:
        pocet_vodka = pocet_vodka + 1
    if obsahuje_gin:
        pocet_gin = pocet_gin + 1
    if obsahuje_rum:
        pocet_rum = pocet_rum + 1

# 6. Vypisem vysledky na obrazovku
print(f"Počet drinkov s vodkou: {pocet_vodka}")
print(f"Počet drinkov s ginom: {pocet_gin}")
print(f"Počet drinkov s rumom: {pocet_rum}")

# Toto tu je len aby sa mi hned nezavrelo okno
input("\nStlač Enter pre ukončenie...")