import requests
from bs4 import BeautifulSoup

def read_urls_from_file(file_path: str):
    with open(file_path, 'r') as file:
        urls = file.read().splitlines()
    return urls

def test_html_injection(url: str, payload: str):
    resp = requests.get(url, params={'input': payload})
    soup = BeautifulSoup(resp.text, 'html.parser')
    alert_element = soup.find('script', text='alert("HTML Injection!")')
    if alert_element:
        return True
    else:
        return False

def main():
    file_path = 'urls.txt'  # Replace with the path to your text file

    urls = read_urls_from_file(file_path)
    for url in urls:
        result = test_html_injection(url, payload)
        if result:
            print(f"HTML Injection vulnerability found at {url}!")
        else:
            print(f"No HTML Injection vulnerability found at {url}.")

if __name__ == '__main__':
    main()
