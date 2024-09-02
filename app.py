from flask import Flask, jsonify, Response, make_response, request
import requests
from bs4 import BeautifulSoup
import html
import uuid
import base64

# from asgiref.wsgi import WsgiToAsgi

app = Flask(__name__)
# asgi_app = WsgiToAsgi(app)


@app.route("/api/v1/getBanks", methods=["GET"])
def getBanks():
    try:
        url = "https://www.policybazaar.com/ifsc/"
        session = requests.Session()

        session.headers = {
            "authority": "www.policybazaar.com",
            "method": "GET",
            "path": "/ifsc/",
            "scheme": "https",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9,hi-IN;q=0.8,hi;q=0.7",
            "Cache-Control": "max-age=0",
            "Priority": "u=0, i",
            "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        }

        response = session.get(url)

        htmlString = response.text
        cleaned_html_string = htmlString.replace('\n', '').replace('\r', '').replace('\t', '').replace('\\', '')
        cleaned_html_string = html.unescape(cleaned_html_string)

        soup = BeautifulSoup(cleaned_html_string, 'html.parser')

        bankOptions = soup.find('select', id="bank")
        options = bankOptions.find_all('option')

        bankValues = []
        for i in range(1,len(options)):
            bank = options[i].get('value')
            bankValues.append(bank)

        jsonResponse = {
            "banks": bankValues,
            "status": "Success"
        }

        return jsonify(jsonResponse)
    
    except Exception as e:
        print(e)
        return jsonify({"error": "Error in fetching Bank Names"})
    
@app.route("/api/v1/getStates", methods=["POST"])
def getStates():
    try:
        post_url = "https://www.policybazaar.com/templates/policybazaar/getifscval.php"
        bank = request.json.get("bank")
        session = requests.Session()

        session.headers = {
            "authority": "www.policybazaar.com",
            "method": "GET",
            "path": "/ifsc/",
            "scheme": "https",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9,hi-IN;q=0.8,hi;q=0.7",
            "Cache-Control": "max-age=0",
            "Priority": "u=0, i",
            "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Sec-Fetch-User": "?1",
            "Referer": "https://www.policybazaar.com/ifsc/",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        }
         
        postData = {
            "task": "getstate",
            "bankname": bank
        }

        response = session.post(post_url, data=postData)

        return jsonify(response.json())

    except Exception as e:
        print(e)
        return jsonify({"error": "Error in fetching State Names which has this Bank"})
    
@app.route("/api/v1/getDistricts", methods=["POST"])
def getDistricts():
    try:
        post_url = "https://www.policybazaar.com/templates/policybazaar/getifscval.php"
        bank = request.json.get("bank")
        state = request.json.get("state")
        session = requests.Session()

        session.headers = {
            "authority": "www.policybazaar.com",
            "method": "GET",
            "path": "/ifsc/",
            "scheme": "https",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9,hi-IN;q=0.8,hi;q=0.7",
            "Cache-Control": "max-age=0",
            "Priority": "u=0, i",
            "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Sec-Fetch-User": "?1",
            "Referer": "https://www.policybazaar.com/ifsc/",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        }
         
        postData = {
            "task": "getdistrict",
            "bankname": bank,
            "statename": state
        }

        response = session.post(post_url, data=postData)

        return jsonify(response.json())

    except Exception as e:
        print(e)
        return jsonify({"error": "Error in fetching districts of state chosen"})
    
@app.route("/api/v1/getBranches", methods=["POST"])
def getBranches():
    try:
        post_url = "https://www.policybazaar.com/templates/policybazaar/getifscval.php"
        bank = request.json.get("bank")
        state = request.json.get("state")
        district = request.json.get("district")
        session = requests.Session()

        session.headers = {
            "authority": "www.policybazaar.com",
            "method": "GET",
            "path": "/ifsc/",
            "scheme": "https",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9,hi-IN;q=0.8,hi;q=0.7",
            "Cache-Control": "max-age=0",
            "Priority": "u=0, i",
            "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Sec-Fetch-User": "?1",
            "Referer": "https://www.policybazaar.com/ifsc/",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        }
         
        postData = {
            "task": "getbranch",
            "bankname": bank,
            "statename": state,
            "districtname": district
        }

        response = session.post(post_url, data=postData)

        return jsonify(response.json())

    except Exception as e:
        print(e)
        return jsonify({"error": "Error in fetching branches in the branches"})

@app.route("/api/v1/get_ifsc_code", methods=["POST"])
def get_ifsc_code():
    try:
        post_url = "https://www.policybazaar.com/templates/policybazaar/getifscval.php"
        bank = request.json.get("bank")
        state = request.json.get("state")
        district = request.json.get("district")
        branch = request.json.get('branch')
        session = requests.Session()

        session.headers = {
            "authority": "www.policybazaar.com",
            "method": "GET",
            "path": "/ifsc/",
            "scheme": "https",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9,hi-IN;q=0.8,hi;q=0.7",
            "Cache-Control": "max-age=0",
            "Priority": "u=0, i",
            "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Sec-Fetch-User": "?1",
            "Referer": "https://www.policybazaar.com/ifsc/",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        }
         
        postData = {
            "task": "getdetail",
            "bankname": bank,
            "statename": state,
            "districtname": district,
            "branchname": branch
        }

        response = session.post(post_url, data=postData)

        return jsonify(response.json())

    except Exception as e:
        print(e)
        return jsonify({"error": "Error in fetching IFSC Code. Please Retry Again"})
