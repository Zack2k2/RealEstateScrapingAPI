from flask import Flask, render_template                                                                    
from flask import jsonify, request, flash, url_for                                                          
from flask import Response 
import json
import ZameenScrapingAPI.scraper as scraper
from flask_cors import cross_origin

app = Flask(__name__)


@app.route("/",methods=['GET'])
def index():
    return render_template("index.html");

@app.route("/get_formated_ads_data",methods=['POST'])
@cross_origin()
def get_ad_format_info():
    
    return jsonify(["hello world"])
    ads_data = []
    req_data = request.get_json()
    try:
        urls_list = req_data['urls']
        urls_len = len(urls_list)
    except (TypeError):
        return jsonify("""
                {
            "reasons": [
                {
                    "you need to issue an urls list like this {"urls":[....]}"
                    "language": "en",
                    "message": "JSON Schema Validation filter failed"
                }
            ],
            "details": {
                "exception message": "JSON Schema Validation filter failed.",
            }
        }

                       """)
    
    for ad_link in urls_list:
        ads_data.append(json.loads(scraper.transform_data((scraper.getAdInfo(ad_link)))))
    return jsonify(ads_data)


@app.route("/getadinfo",methods=['POST'])
@cross_origin()
def get_ad_info():
    
    ads_data = []
    req_data = request.get_json()
    try:
        urls_list = req_data['urls']
        urls_len = len(urls_list)
    except (TypeError):
        return jsonify("""
                {
            "reasons": [
                {
                    "you need to issue an urls list like this {"urls":[....]}"
                    "language": "en",
                    "message": "JSON Schema Validation filter failed"
                }
            ],
            "details": {
                "exception message": "JSON Schema Validation filter failed.",
            }
        }

                       """)
    
    for ad_link in urls_list:
        ads_data.append(json.loads( scraper.getAdInfo(ad_link)))
    return jsonify(ads_data)


@app.route("/getlatestads", methods=['POST'])
@cross_origin()
def get_latest_ads():
    links_found = set()
    req_data = request.get_json()


    try:
        urls_list = req_data['urls']
        urls_len = len(urls_list)
    except (TypeError):
        return jsonify("""
                {
            "reasons": [
                {
                    "you need to issue an urls list like this {"urls":[....]}"
                    "language": "en",
                    "message": "JSON Schema Validation filter failed"
                }
            ],
            "details": {
                "exception message": "JSON Schema Validation filter failed.",
            }
        }

                       """)
    
    for link in urls_list:
        property_links = json.loads(scraper.getAdsUrlLists(link))
        for p_link in property_links:
            links_found.add(p_link)

    return jsonify(list(links_found))



@app.route('/geturban',methods=['POST'])
@cross_origin()
def get_urbanization():
    req_data = request.get_json()

    try:
        lat = req_data['latitude']
        long = req_data['longitude']
        rad = req_data['radius']
    except KeyError:
        return jsonify("""
                {
            "reasons": [
                {
                    "you need to issue an urls list like this {"urls":[....]}"
                    "language": "en",
                    "message": "JSON Schema Validation filter failed"
                }
            ],
            "details": {
                "exception message": "JSON Schema Validation filter failed.",
            }
        }

                       """)


    response = scraper.getUrbanization(lat,long,rad)

    return json.loads(response)["data"]

