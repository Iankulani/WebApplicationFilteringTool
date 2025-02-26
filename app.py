from flask import Flask, request
import requests
import re

app = Flask(__name__)

@app.route('/check_website', methods=['GET'])
def check_website():
    url = request.args.get('url')
    result = filter_website(url)
    return result

def is_https(url):
    return url.startswith("https://")

def is_valid_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://' 
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]*[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]*[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

def has_suspicious_keywords(url):
    suspicious_keywords = ["malware", "phishing", "login", "free", "promo", "update", "gift", "offers"]
    for word in suspicious_keywords:
        if word in url.lower():
            return True
    return False

def check_url_reputation(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def filter_website(url):
    if not is_valid_url(url):
        return "Invalid URL format!"

    if not is_https(url):
        return "Warning: The URL does not use HTTPS! This may not be secure."

    if has_suspicious_keywords(url):
        return "Suspicious: The URL contains suspicious keywords."

    if not check_url_reputation(url):
        return "Suspicious: The website might be down or unavailable."

    return "The website seems safe!"

if __name__ == '__main__':
    app.run(debug=True)
