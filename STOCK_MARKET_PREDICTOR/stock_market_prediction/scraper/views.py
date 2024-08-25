from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_and_return_data(request):
    url = "https://www.sharesansar.com/today-share-price"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find('table', {'id': 'headFixed'})
    rows = table.find_all('tr')
    stock_data = []
    
    for row in rows[1:]:
        columns = row.find_all('td')
        symbol = columns[1].text.strip()
        open_price = columns[3].text.strip()
        high = columns[4].text.strip()
        low = columns[5].text.strip()
        close = columns[6].text.strip()
        perChange = columns[14].text.strip()
        volume = columns[8].text.strip()
        turnover = columns[10].text.strip()
        
        stock_data.append({
            'Symbol': symbol,
            'Open': open_price,
            'High': high,
            'Low': low,
            'Close': close,
            '% Change': perChange,
            'Volume': volume,
            'Turnover': turnover
        })
    
    # Convert to DataFrame and then to JSON
    df = pd.DataFrame(stock_data)
    return JsonResponse(df.to_dict(orient="records"), safe=False)
