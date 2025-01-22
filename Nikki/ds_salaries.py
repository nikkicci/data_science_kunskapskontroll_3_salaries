import requests
import pandas as pd
import sqlite3 as db
import logging
import sys
import json

API_KEY = "929ce405b668474ea251cb0f2cb4764b"  

def bail(message):
    logger.error(message)
    sys.exit(1)

def fetch_exchange_rate():
    url = f"https://api.currencyfreaks.com/v2.0/rates/latest?apikey={API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch currencies: {response.text}")
    except Exception as e:
        raise Exception(f"Failed to fetch currencies: {str(e)}")
    
    payload = json.loads(response.text)
    try:
        sek_rate = float(payload["rates"]["SEK"])  # Hämta SEK-växelkursen
    except KeyError:
        raise Exception("SEK rate not found in API response")
    
    return sek_rate

def convert_salaries_to_sek(salaries_df, sek_rate):
    try:
        # Lägg till en ny kolumn med omvandlade löner
        salaries_df["salary_in_sek"] = round(salaries_df["salary_in_usd"] * sek_rate)
    except Exception as e:
        raise Exception(f"Failed to convert salaries: {str(e)}")
    return salaries_df

def export_to_database(df):
    try:
        con = db.connect("ds_salaries.db")
        df.to_sql("salaries", con, if_exists="replace", index=False)
        con.close()
    except Exception as e:
        raise Exception(f"Failed to export to database: {str(e)}")

if __name__ == "__main__":
    logging.basicConfig(filename="salaries.log", level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
    logger = logging.getLogger()
    
    try:
        # Steg 1: Hämta SEK-växelkursen
        sek_rate = fetch_exchange_rate()
        logger.info(f"Fetched SEK exchange rate: {sek_rate}")
        
        # Steg 2: Läs in löner från CSV
        salaries_df = pd.read_csv("ds_salaries.csv")
        if "salary_in_usd" not in salaries_df.columns:
            raise Exception("CSV file must contain 'salary_in_usd' column")
        
        # Steg 3: Omvandla löner till SEK
        salaries_df = convert_salaries_to_sek(salaries_df, sek_rate)
        
        # Steg 4: Exportera data till SQLite-databas
        export_to_database(salaries_df)
        
        logger.info("Salaries converted and exported successfully")
    except Exception as e:
        bail(str(e))

