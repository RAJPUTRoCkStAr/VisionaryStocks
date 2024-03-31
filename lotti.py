import json
import requests
from streamlit_lottie import st_lottie
def load_lottiefile(filepath:str):
    with open (filepath, 'r') as f:
        return json.load(f)
def load_lottieurl(url:str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
lottie_buyshare = load_lottiefile("lotti/buyshare.json")
lottie_company = load_lottiefile("lotti/company.json")
lottie_exploredata = load_lottiefile("lotti/exploredata.json")
lottie_hello = load_lottiefile("lotti/hello.json")
lottie_map = load_lottiefile("lotti/map.json")
lottie_predaccu = load_lottiefile("lotti/predaccu.json")
lottie_report = load_lottiefile("lotti/report.json")

