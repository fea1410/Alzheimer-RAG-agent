import requests
import pandas as pd
from tqdm import tqdm
from lxml import etree
import time
import json




MAX_PAPERS = 50
SAVE_XML = False

QUERY = '''
("Alzheimer" OR "Alzheimer's disease")
AND
("therapeutic target" OR "drug target" OR "targeting")
AND
OPEN_ACCESS:y
AND
HAS_FT:y
AND
SRC:PMC
'''




def search_papers(max_papers=50):

    url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"

    papers = []
    page = 1

    while len(papers) < max_papers:

        params = {
            "query": QUERY,
            "format": "json",
            "pageSize": 100,
            "page": page
        }

        r = requests.get(url, params=params)
        r.raise_for_status()
        data = r.json()

        results = data["resultList"]["result"]

        if not results:
            break

        papers.extend(results)
        page += 1

    return papers[:max_papers]



def download_xml(pmcid):

    url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML"

    r = requests.get(url)

    if r.status_code != 200:
        return None

    return r.text



def extract_text_from_xml(xml_string):

    try:
        root = etree.fromstring(xml_string.encode())
        paragraphs = root.xpath("//p//text()")
        return " ".join(paragraphs)
    except:
        return ""




papers = search_papers(MAX_PAPERS)

records = []

for p in tqdm(papers):

    pmcid = p.get("pmcid")

    if not pmcid:
        continue

    xml = download_xml(pmcid)

    if xml is None:
        continue

    full_text = extract_text_from_xml(xml)

    record = {
        "title": p.get("title"),
        "doi": p.get("doi"),
        "pmcid": pmcid,
        "abstract": p.get("abstractText"),
        "full_text": full_text,
        "journal": p.get("journalTitle"),
        "year": p.get("pubYear"),
    }

    records.append(record)

    if SAVE_XML:
        with open(f"{pmcid}.xml", "w", encoding="utf-8") as f:
            f.write(xml)

    time.sleep(0.2)   # чтобы не спамить API



df = pd.DataFrame(records)

df.to_csv("alzheimer_targets.csv", index=False)

with open("alzheimer_targets.json", "w", encoding="utf-8") as f:
    json.dump(records, f, indent=2, ensure_ascii=False)


print("Saved:", len(records), "papers")