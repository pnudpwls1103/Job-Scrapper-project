import requests
from bs4 import BeautifulSoup


def extract_job(html):
    # job title
    try:
      title = html.find("a", {"class": "preventLink"})
      if title is None:
          return None
      else:
          title = title.get_text(strip=True)

      # job company
      company = html.find("span", {"class": "companyLink"}).get_text(strip=True)

      # link
      link = html.find("a", {"class": "preventLink"})['href']
      link = f'https://remoteok.com/{link}'
    except:
      return None

    return {'title': title, 'company': company, 'link': link}


def extract_jobs(url):
    jobs = []
    headers = {
        'User-Agent':
        ('Mozilla/5.0 (Windows NT 10.0;Win64; x64)\AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98\Safari/537.36'
         )
    }
    print(f'<<Scrapping page remoteok-jobs>>')
    result = requests.get(url, headers=headers)
    soup = BeautifulSoup(result.text, "html.parser")

    try:
      results = soup.find_all("tr", {"class": "job"})
      for result in results:
          td = result.find("td", {"class": "company_and_position"})
          job = extract_job(td)
          if job is None:
              continue
          jobs.append(job)
    except:
      pass
    return jobs


def get_jobs(word):
    url = f"https://remoteok.com/remote-{word}-jobs"
    jobs = extract_jobs(url)
    return jobs