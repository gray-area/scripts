import requests
from bs4 import BeautifulSoup
from requests.exceptions import SSLError

def read_urls_from_file(file_path: str):
    with open(file_path, 'r') as file:
        urls = file.read().splitlines()
    return urls

def test_html_injection(url: str, payload: str):
    resp = requests.get(url, params={'input': payload})
    soup = BeautifulSoup(resp.text, 'html.parser')
    alert_element = soup.find('script', string='alert("HTML Injection!")')

    php_payload = "<?php echo 'PHP Injection!'; ?>"
    php_resp = requests.get(url, params={'input': php_payload})

    if alert_element:
        return True, "HTML Injection vulnerability found!"
    elif php_payload in php_resp.text:
        return True, "PHP Injection vulnerability found!"
    else:
        return False, "No HTML or PHP Injection vulnerability found."

def main():
    file_path = 'urls.txt'  # Replace with the path to your text file
    payload = '<script>alert("HTML Injection!")</script>'
    output_file_path = 'results.txt'

    urls = read_urls_from_file(file_path)
    with open(output_file_path, 'w') as output_file:
        for url in urls:
            try:
                result, message = test_html_injection(url, payload)

                if result:
                    print(message)
                    output_file.write(f"{url}: {message}\n")
                else:
                    print(f"No HTML or PHP Injection vulnerability found at {url}.")
                    output_file.write(f"{url}: No HTML or PHP Injection vulnerability found.\n")

            except SSLError:
                print(f"SSL verification error for URL: {url}")
                output_file.write(f"{url}: SSL verification error\n")
                continue

if __name__ == '__main__':
    main()
