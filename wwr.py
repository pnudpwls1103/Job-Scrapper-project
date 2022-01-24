import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool, Manager

def extract_job(html):
    # job title
    try:
      title = html.find("span", {"class": "title"})
      if title is None:
        return None
      else:
        title = title.get_text(strip=True)
      # job company
      company = html.find("span", {"class": "company"}).get_text(strip=True)

      # link
      link = f'https://weworkremotely.com/{html["href"]}'
    except:
      return None

    return {
        'title': title,
        'company': company,
        'link': link
    }


def extract_jobs(url):
    jobs = []
    print(f'<<Scrapping page WWR>>')
    try:
      result = requests.get(url)
      soup = BeautifulSoup(result.text, "html.parser")
      results = soup.find_all("section", {"class":"jobs"})
      for result in results:
          a_tags = result.select("article li a")
          for a_tag in a_tags:
            job = extract_job(a_tag)
            if job is None:
              continue
            jobs.append(job)
    except Exception as e:
      print(e)
    return jobs


def get_jobs(word):
    manager = Manager()

    url = f"https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term={word}"
    jobs = extract_jobs(url)
    return jobs
