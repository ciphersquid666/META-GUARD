import requests
from bs4 import BeautifulSoup, Comment
from tabulate import tabulate
import json
from termcolor import colored
from urllib.parse import urlparse
import time
import ssl
import re

print(colored("=====================================", 'cyan'))
print(colored("[×] NETA-GUARD Tool by 𝘾𝙞𝙥𝙝𝙚𝙧 𝙎𝙦𝙪𝙞𝙙", 'red'))
print(colored("[×] Use responsibly!", 'yellow'))
print(colored("=====================================", 'cyan'))

def extract_metadata(urls, verbose=False):
    try:
        for url in urls:
            print(colored(f"\nRetrieving data from {url}...", "cyan"))
            start_time = time.time()
            response = requests.get(url, timeout=10, allow_redirects=True)

            if response.status_code != 200:
                print(colored(f"Error: Status code {response.status_code} for the URL: {url}", "red"))
                continue

            page_load_time = round(time.time() - start_time, 2)
            soup = BeautifulSoup(response.text, 'html.parser')

            metadata = {}
            metadata['title'] = soup.title.string if soup.title else colored('No title found', 'yellow')
            description_tag = soup.find('meta', attrs={'name': 'description'})
            metadata['description'] = description_tag['content'] if description_tag else colored('No description found', 'yellow')

            og_title = soup.find('meta', attrs={'property': 'og:title'})
            og_description = soup.find('meta', attrs={'property': 'og:description'})
            og_image = soup.find('meta', attrs={'property': 'og:image'})
            metadata['og:title'] = og_title['content'] if og_title else colored('No og:title found', 'yellow')
            metadata['og:description'] = og_description['content'] if og_description else colored('No og:description found', 'yellow')
            metadata['og:image'] = og_image['content'] if og_image else colored('No og:image found', 'yellow')

            twitter_title = soup.find('meta', attrs={'name': 'twitter:title'})
            twitter_description = soup.find('meta', attrs={'name': 'twitter:description'})
            twitter_image = soup.find('meta', attrs={'name': 'twitter:image'})
            metadata['twitter:title'] = twitter_title['content'] if twitter_title else colored('No twitter:title found', 'yellow')
            metadata['twitter:description'] = twitter_description['content'] if twitter_description else colored('No twitter:description found', 'yellow')
            metadata['twitter:image'] = twitter_image['content'] if twitter_image else colored('No twitter:image found', 'yellow')

            charset_tag = soup.find('meta', attrs={'charset': True})
            viewport_tag = soup.find('meta', attrs={'name': 'viewport'})
            robots_tag = soup.find('meta', attrs={'name': 'robots'})
            metadata['charset'] = charset_tag['charset'] if charset_tag else colored('No charset found', 'yellow')
            metadata['viewport'] = viewport_tag['content'] if viewport_tag else colored('No viewport found', 'yellow')
            metadata['robots'] = robots_tag['content'] if robots_tag else colored('No robots found', 'yellow')

            og_site_name = soup.find('meta', attrs={'property': 'og:site_name'})
            twitter_site = soup.find('meta', attrs={'name': 'twitter:site'})
            metadata['og:site_name'] = og_site_name['content'] if og_site_name else colored('No og:site_name found', 'yellow')
            metadata['twitter:site'] = twitter_site['content'] if twitter_site else colored('No twitter:site found', 'yellow')

            al_ios_app_store_id = soup.find('meta', attrs={'property': 'al:ios:app_store_id'})
            al_android_url = soup.find('meta', attrs={'property': 'al:android:url'})
            metadata['al:ios:app_store_id'] = al_ios_app_store_id['content'] if al_ios_app_store_id else colored('No al:ios:app_store_id found', 'yellow')
            metadata['al:android:url'] = al_android_url['content'] if al_android_url else colored('No al:android:url found', 'yellow')

            headings = {f'h{n}': [heading.text.strip() for heading in soup.find_all(f'h{n}')] for n in range(1, 7)}
            links = [a['href'] for a in soup.find_all('a', href=True)]
            images = [img['src'] for img in soup.find_all('img', src=True)]

            structured_data = soup.find('script', type='application/ld+json')
            metadata['structured_data'] = structured_data.string if structured_data else colored('No structured data found', 'yellow')

            canonical_url = soup.find('link', rel='canonical')
            metadata['canonical_url'] = canonical_url['href'] if canonical_url else colored('No canonical URL found', 'yellow')

            favicon = soup.find('link', rel='icon')
            metadata['favicon'] = favicon['href'] if favicon else colored('No favicon found', 'yellow')

            metadata['language'] = soup.find('html').get('lang', colored('No language attribute found', 'yellow'))
            metadata['final_url'] = response.url
            metadata['page_load_time'] = page_load_time
            metadata['http_headers'] = dict(response.headers)
            metadata['headings'] = headings
            metadata['links'] = links
            metadata['images'] = images

            metadata['ssl_certificate'] = 'HTTPS' if response.url.startswith('https') else 'HTTP'
            metadata['security_headers'] = {
                'Content-Security-Policy': response.headers.get('Content-Security-Policy', 'Not Set'),
                'Strict-Transport-Security': response.headers.get('Strict-Transport-Security', 'Not Set'),
                'X-Content-Type-Options': response.headers.get('X-Content-Type-Options', 'Not Set'),
                'X-XSS-Protection': response.headers.get('X-XSS-Protection', 'Not Set'),
                'X-Frame-Options': response.headers.get('X-Frame-Options', 'Not Set')
            }

            sensitive_data = scan_for_sensitive_data(soup, links, response.headers)
            metadata['sensitive_data'] = sensitive_data

            with open('metadata.json', 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=4)

            print(colored("\nSummary Metadata:", "green"))
            summary = [(k, v if isinstance(v, str) else str(v)[:300] + '...') for k, v in metadata.items() if k not in ['headings', 'links', 'images', 'http_headers']]
            print(tabulate(summary, headers=["Metadata Field", "Value"], tablefmt="grid"))

            if verbose:
                print(colored("\nDetailed Metadata", "cyan"))
                print(colored("\nHeadings:", "blue"))
                print(json.dumps(headings, indent=2))
                print(colored("\nLinks:", "blue"))
                print(json.dumps(links[:20], indent=2))
                print(colored("\nImages:", "blue"))
                print(json.dumps(images[:20], indent=2))
                print(colored("\nHTTP Headers:", "blue"))
                print(json.dumps(metadata['http_headers'], indent=2))
                print(colored("\nSensitive Data Found:", "red"))
                print(json.dumps(sensitive_data, indent=2))
                print(colored("\nFull metadata saved to metadata.json", "green"))

    except requests.exceptions.RequestException as e:
        print(colored(f"HTTP request error: {e}", "red"))
    except Exception as e:
        print(colored(f"Metadata extraction error: {e}", "red"))

def scan_for_sensitive_data(soup, links, headers):
    sensitive_data = {}
    sensitive_patterns = [
        r"([a-zA-Z0-9]{32})",
        r"([A-Za-z0-9]{40})",
        r"(?:\b(?:password|secret|key|token|api|client_secret|auth)\s*[:=]\s*[\"']?([a-zA-Z0-9]{32,})[\"']?)",
        r"(?i)aws|s3|cloudfront"
    ]
    page_text = soup.get_text()

    for pattern in sensitive_patterns:
        matches = re.findall(pattern, page_text)
        if matches:
            sensitive_data[pattern] = matches

    for link in links:
        if 'api' in link.lower() or 'token' in link.lower() or re.search(r'^[a-zA-Z0-9]{32}$', link):
            sensitive_data['link_with_possible_sensitive_data'] = link

    return sensitive_data

def get_robots_txt(url):
    try:
        robots_url = urlparse(url)._replace(path='/robots.txt').geturl()
        response = requests.get(robots_url, timeout=10)
        return response.text if response.status_code == 200 else "Not found"
    except Exception:
        return "Not found"

def find_sitemap_xml(url):
    try:
        sitemap_url = urlparse(url)._replace(path='/sitemap.xml').geturl()
        response = requests.get(sitemap_url, timeout=10)
        return response.text if response.status_code == 200 else "Not found"
    except Exception:
        return "Not found"

if __name__ == "__main__":
    urls_input = input("Enter the URLs of the web pages (comma separated): ")
    verbose_input = input("Enable verbose mode? (yes/no): ").strip().lower() == 'yes'
    urls = [url.strip() for url in urls_input.split(',')]
    extract_metadata(urls, verbose=verbose_input)
