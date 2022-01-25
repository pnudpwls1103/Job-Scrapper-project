import requests
from bs4 import BeautifulSoup
import concurrent.futures
import asyncio
from functools import partial

jobs = []

def get_last_page(url):
  try:
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')

    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
    last_page = pages[-2].get_text(strip=True)
  except:
    last_page = 0
  return int(last_page)


def extract_job(html):
    # job title
    title = html.find("a", {"class": "s-link"})['title']

    # job company, location
    company, _ = html.find("h3", {
        "class": "fc-black-700"
    }).find_all("span", recursive=False)
    company = company.get_text(strip=True)

    # id
    job_id = html["data-result-id"]

    return {
        'title': title,
        'company': company,
        'link': f"https://stackoverflow.com/jobs/{job_id}/"
    }


async def extract_jobs(page, url):
    global jobs
    
    try:
      print(f'<<Scrapping page Stackoverflow-{page}>>')
      result = requests.get(f'{url}&pg={page+1}')
      soup = BeautifulSoup(result.text, "html.parser")
      results = soup.find_all("div", {"class": "js-result"})
      for result in results:
          job = extract_job(result)
          jobs.append(job)
    except:
      pass
    # return jobs

async def main(last_page, url):
    await asyncio.wait([extract_jobs(page, url) for page in range(last_page)])

def get_jobs(word):
    global jobs
    jobs = []
    url = f"https://stackoverflow.com/jobs?q={word}"
    last_page = get_last_page(url)
    
    asyncio.run(main(last_page, url))

    # with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
    #   results = [executor.submit(extract_jobs, page, url) for page in range(1, last_page + 1)]

    # for result in results:
    #   jobs += result.result()
    return jobs
