import requests

url = 'http://23.20.49.160:8080/'

try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    content = response.text
except requests.exceptions.RequestException as e:
    content = str(e)

content[:1000]  # Return the first 1000 characters of the content for inspection