import requests
import csv
import os

# ----------
# CONFIG
# ----------

coins = [
    "bitcoin",
    "ethereum",
    "solana",
    "cardano",
    "dogecoin"
]

alert_rules = {
    "bitcoin": {"below": 40000, "above": 100000},
    "ethereum": {"below": 2000, "above": 5000}
}

data_dir = "data"
output_dir = "output"

os.makedirs(data_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

csv_file = os.path.join(output_dir, "crypto_prices.csv")
report_file = os.path.join(output_dir, "summary.txt")

# ----------
# FETCH DATA
# ----------

def fetch_prices(coins):
    url = "https://api.coingecko.com/api/v3/simple/price"
    
    params = {
        "ids": ",".join(coins),
        "vs_currencies": "usd",
        "include_24hr_change": "true"
}
    
    response = requests.get(url, params=params)
    data = response.json()
    
    results = []
    
    for coin in coins:
        if coin in data:
            results.append({
                "coin": coin,
                "price_usd": data[coin].get("usd", 0),
                "change_24hr": data[coin].get("usd_24hr_change", 0)
            })
    
    return results    

# ----------
# SAVE TO CSV
# ----------

def save_csv(rows, filename):
    if not rows:
        return
    
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
        
# ----------
# CHECK ALERTS
# ----------

def check_alerts(rows, alert_rules):
    triggered = []
    
    for row in rows:
        coin = row["coin"]
        price = row["price_usd"]
        
        if coin in alert_rules:
            rules = alert_rules[coin]
            
            if "below" in rules and price < rules["below"]:
                triggered.append(f"{coin.upper()} fell below ${rules['below']}")
                
            if "above" in rules and price > rules["above"]:
                triggered.append(f"{coin.upper()} rose above ${rules['above']}")
                
    return triggered

# ----------
# WRITE SUMMARY
# ----------

def write_summary(rows, alerts_triggered, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("CRYPTO PRICE SUMMARY\n")
        f.write("====================\n\n")
        
        for row in rows:
            f.write(
                f"{row['coin'].upper()} | "
                f"${row['price_usd']:,.2f} | "
                f"{row['change_24hr']:,.2f}%\n"
            )
            
        if alerts_triggered:
            f.write("\nALERTS\n")
            f.write("------\n")
            for alert in alerts_triggered:
                f.write(alert + "\n")
                
# ----------
# MAIN
# ----------
        
def main():
    prices = fetch_prices(coins)
    save_csv(prices, csv_file)

    alerts_triggered = check_alerts(prices, alert_rules)
    write_summary(prices, alerts_triggered, report_file)

    print("Done.")
    print(f"Saved: {csv_file}")
    print(f"Saved: {report_file}")
    
    if alerts_triggered:
        print(f"\n {len(alerts_triggered)} alert(s) triggered:")
        for alert in alerts_triggered:
            print(f" {alert}")
    else:
        print("\n No alerts triggered")
if __name__ == "__main__":
    main()
               