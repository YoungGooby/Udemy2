import httpx
from selectolax.parser import HTMLParser

url = "https://www.yellowpages.com/miami-fl/automobile-parts-supplies"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0"}

resp = httpx.get(url, headers = headers)
html = HTMLParser(resp.text)
repeat_businesses = set()
result_counter = 1
def extract_text(node):
    return node.text(strip=True) if node else "Error"

def parse_page(url):
    global result_counter
    rep = httpx.get(url, headers=headers)
    html = HTMLParser(rep.text)
    Business_name = html.css("a.business-name")
    Business_phone = html.css("div.phones")
    for Business_name, Business_phone in zip(Business_name, Business_phone):
        name = extract_text(Business_name)
        phone = extract_text(Business_phone)
        if (name, phone) not in repeat_businesses:
            item = {
                "number" : result_counter,
                "name" : extract_text(Business_name),
                "Phone" : extract_text(Business_phone)
            }
            print(item)
            repeat_businesses.add((name, phone))
            result_counter += 1
    next_page = html.css_first("a.next.ajax-page")
    if next_page:
        next_page_url = next_page.attrs.get("href")
        if next_page_url:
            return "https://www.yellowpages.com" + next_page_url
    return None

current_url = url
page_limit = 3
page_count = 0

while current_url and page_count < page_limit:
    current_url = parse_page(current_url)
    page_count += 1