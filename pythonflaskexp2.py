from flask import Flask, request
import requests

app = Flask(__name__)

# moj cennik, lebo v api ceny nie su
CENNIK = {
    "Margarita": 8.50,
    "Mojito": 7.90,
    "Old Fashioned": 9.50,
    "Pina Colada": 8.00,
    "Martini": 9.00,
    "Cosmopolitan": 8.20,
    "Bloody Mary": 7.50
}

# funkcia na tahanie dat z api
def stiahni_drinky():
    url = "https://boozeapi.com/api/v1/cocktails"
    odpoved = requests.get(url)
    return odpoved.json()['data']

# hlavna stranka (menu)
@app.route("/")
def ukaz_drinky():
    cocktails = stiahni_drinky()
    
    # check ci sa vraciam z detailu cez tlacidlo spat
    navrat = request.args.get("navrat")
    
    # ak hej, opona sa vobec neukaze nech to neotravuje
    trieda_opony = "otvorena" if navrat else ""
    styl_opony = "transition: none; display: none;" if navrat else ""
    
    html_hlavicka = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Luxusný Cocktail Bar</title>
        <style>
            body {{ background-color: #121212; color: #ffffff; font-family: Arial, sans-serif; text-align: center; margin: 0; padding: 0; overflow-x: hidden; }}
            h1 {{ color: #D4AF37; font-size: 40px; margin-top: 50px; }}
            .zoznam-drinkov {{ display: flex; flex-wrap: wrap; justify-content: center; gap: 30px; padding: 20px; }}
            .karticka {{ background-color: #1e1e1e; border: 1px solid #333; border-radius: 15px; padding: 20px; width: 250px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); transition: transform 0.3s; }}
            .karticka:hover {{ transform: scale(1.05); border-color: #D4AF37; cursor: pointer; }}
            img {{ width: 100%; border-radius: 10px; }}
            a {{ text-decoration: none; color: inherit; }}
            
            #opona {{
                position: fixed;
                top: 0; left: 0; width: 100%; height: 100vh;
                background: repeating-linear-gradient(to right, #4a0010, #800020 10%, #4a0010 20%);
                z-index: 1000; 
                display: flex; flex-direction: column; align-items: center; justify-content: center;
                transition: transform 1.5s cubic-bezier(0.77, 0, 0.175, 1);
                border-bottom: 15px solid #D4AF37;
                box-shadow: 0 10px 40px rgba(0,0,0,0.9);
            }}
            #opona.otvorena {{ transform: translateY(-100vh); }}
            
            #vstupne-tlacidlo {{
                margin-top: 40px; padding: 15px 50px; font-size: 24px; font-weight: bold;
                text-transform: uppercase; color: #121212;
                background: linear-gradient(to bottom, #FFDF73, #D4AF37);
                border: none; border-radius: 50px; cursor: pointer;
                box-shadow: 0 6px 20px rgba(0,0,0,0.7); transition: all 0.3s ease;
            }}
            #vstupne-tlacidlo:hover {{ transform: scale(1.1); box-shadow: 0 8px 25px rgba(212, 175, 55, 0.5); background: linear-gradient(to bottom, #FFF8DC, #FFDF73); }}
        </style>
    </head>
    <body>
        <div id="opona" class="{trieda_opony}" style="{styl_opony}">
            <h1 style="color: white; font-size: 60px; text-shadow: 2px 2px 10px rgba(0,0,0,0.8);">Matúšov Bar</h1>
            <button id="vstupne-tlacidlo">Vstúpiť</button>
        </div>

        <h1>Naše Špeciálne Menu</h1>
        <div class="zoznam-drinkov">
    """

    # vygenerovanie html pre kazdy drink
    html_drinky = ""
    for drink in cocktails:
        nazov = drink['name']
        obrazok = drink['image']
        html_drinky += f"""
            <a href="/drink/{nazov}">
                <div class="karticka">
                    <img src="{obrazok}" alt="{nazov}">
                    <h3 style="color: #D4AF37;">{nazov}</h3>
                    <p style="color: #aaa; font-size: 14px;">Klikni pre detaily a cenu</p>
                </div>
            </a>
        """

    # js script na otvorenie opony
    html_paticka = """
        </div>
        
        <script>
            let tlacidlo = document.getElementById('vstupne-tlacidlo');
            let opona = document.getElementById('opona');

            if (tlacidlo) {
                tlacidlo.addEventListener('click', function() {
                    opona.classList.add('otvorena');
                });
            }
        </script>
    </body>
    </html>
    """
    
    return html_hlavicka + html_drinky + html_paticka


# detail drinku
@app.route("/drink/<nazov_drinku>")
def detail_drinku(nazov_drinku):
    cocktails = stiahni_drinky()
    vybrany_drink = None
    
    # najdem kliknuty drink v zozname
    for drink in cocktails:
        if drink['name'] == nazov_drinku:
            vybrany_drink = drink
            break
            
    if vybrany_drink is None:
        return "<h1>Oops! Tento drink sme nenašli.</h1>"

    obrazok = vybrany_drink['image']
    
    # vypis ingrediencii
    html_ingrediencie = ""
    for polozka in vybrany_drink['ingredients']:
        html_ingrediencie += f"<li>{polozka['name']}</li>"
        
    # nacitam cenu z cennika, default je 7.50
    cena = CENNIK.get(nazov_drinku, 7.50)
    formatovana_cena = "{:.2f}".format(cena)
    
    html_detail = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{nazov_drinku}</title>
        <style>
            body {{ background-color: #121212; color: #ffffff; font-family: Arial, sans-serif; padding: 50px; display: flex; justify-content: center; }}
            .detail-okno {{ display: flex; background-color: #1e1e1e; border: 1px solid #D4AF37; border-radius: 15px; padding: 40px; max-width: 800px; gap: 40px; box-shadow: 0 4px 15px rgba(212, 175, 55, 0.2); }}
            .lavy-panel img {{ width: 300px; border-radius: 10px; border: 2px solid #333; }}
            .pravy-panel {{ display: flex; flex-direction: column; justify-content: center; }}
            h1 {{ color: #D4AF37; margin-top: 0; font-size: 36px; }}
            .cena {{ font-size: 28px; color: #4CAF50; font-weight: bold; margin: 20px 0; background-color: #2a2a2a; padding: 10px; border-radius: 8px; width: fit-content; border: 1px solid #4CAF50; }}
            ul {{ color: #aaa; font-size: 18px; line-height: 1.6; }}
            .spat-tlacidlo {{ margin-top: 30px; display: inline-block; padding: 10px 20px; background-color: #D4AF37; color: #121212; text-decoration: none; border-radius: 5px; font-weight: bold; text-align: center; width: 150px; transition: background-color 0.3s; }}
            .spat-tlacidlo:hover {{ background-color: #FFF8DC; }}
        </style>
    </head>
    <body>
        <div class="detail-okno">
            <div class="lavy-panel">
                <img src="{obrazok}" alt="{nazov_drinku}">
            </div>
            <div class="pravy-panel">
                <h1>{nazov_drinku}</h1>
                <div class="cena">Cena: {formatovana_cena} €</div>
                <h3>Potrebné ingrediencie:</h3>
                <ul>
                    {html_ingrediencie}
                </ul>
                <a href="/?navrat=1" class="spat-tlacidlo">Späť na menu</a>
            </div>
        </div>
    </body>
    </html>
    """
    return html_detail

if __name__ == "__main__":
    app.run(debug=True)