import requests
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
from urllib.parse import urljoin, urlparse, urldefrag
from collections import deque
import warnings

# Optional: suppress XMLParsedAsHTMLWarning
# warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

def crawl_site(base_url, max_pages=1):
    visited = set()
    to_visit = deque([base_url])  # Use queue for BFS
    pages = {}

    while to_visit and len(visited) < max_pages:
        url = to_visit.popleft()  # BFS: pop from front
        url = url.rstrip('/')
        if url in visited or not url.startswith(base_url):
            continue
        try:
            res = requests.get(url, timeout=5)
            content_type = res.headers.get('Content-Type', '')
            is_xml = content_type.startswith('application/xml') or res.text.strip().startswith('<?xml')

            # Use XML parser if XML, otherwise HTML parser
            parser = 'xml' if is_xml else 'html.parser'
            soup = BeautifulSoup(res.text, parser)

            text = extract_text(soup)
            pages[url] = text
            print(url)  # Show progress
            visited.add(url)

            for link in soup.find_all('a', href=True):
                full_url = urljoin(url, link['href'])
                full_url, _ = urldefrag(full_url)  # remove fragments like #section
                full_url = full_url.rstrip('/')
                if same_domain(base_url, full_url) and full_url not in visited and full_url not in to_visit:
                    to_visit.append(full_url)  # enqueue for BFS

        except Exception:
            continue

    return pages

def same_domain(base, target):
    return urlparse(base).netloc == urlparse(target).netloc

def extract_text(soup):
    for tag in soup(['script', 'style']):
        tag.decompose()
    return soup.get_text(separator=' ', strip=True)
