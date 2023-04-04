import requests
from bs4 import BeautifulSoup

url = 'https://markets.businessinsider.com/index/components/s&p_500'
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

# Extract table of stock data
table = soup.find('table', {'class': 'table'})

# Extract rows of stock data
rows = table.find_all('tr')

# Skip the first row because it contains the header
for row in rows[1:]:
    # Extract the ticker symbol, latest price, and previous close from the row
    ticker = row.find('a', {'class': 'link'})
    latest_price = row.find('span', {'class': 'price'})
    previous_close = row.find_all('td')[-3]

    # Print the data for each stock

    print(latest_price)
    #print(ticker.strip(), latest_price.strip(), previous_close.strip())