"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs

Good luck!
"""

from flask import Flask, render_template, request, redirect, send_file
from so import get_jobs as get_so_jobs
from wwr import get_jobs as get_work_jobs
from remoteok import get_jobs as get_remoteok_jobs
from exporter import save_to_file
import time

# from exporter import save_to_file
app = Flask("JobScrapper")

db = {}
scrapper = {
    'WWR': 'get_work_jobs(word)',
    'Stackoverflow': 'get_so_jobs(word)',
    'Remoteok': 'get_remoteok_jobs(word)'
}

def scrapping(word):
  jobs = {}
  for site, func in scrapper.items(): 
    result = eval(func)
    jobs[site] = result
  return jobs

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/report")
def report():
    word = request.args.get('word')
    if word:
        word = word.lower()
        existingJobs = db.get(word)
        if existingJobs:
            jobs = existingJobs
        else:
            start_time = time.time()
            db[word] = scrapping(word)
            jobs = db[word]
            end_time = time.time()
            print(end_time - start_time)
        number = len(jobs['WWR']) + len(jobs['Stackoverflow']) + len(jobs['Remoteok'])
    else:
        return redirect("/")
    
    return render_template("report.html",
                           searchingBy=word,
                           resultsNumber=number,
                           jobs=jobs)


@app.route("/export")
def export():
    jobs = []
    try:
        word = request.args.get('word')
        site = request.args.get('site')
        if not word:
            raise Exception()
        if not site:
            raise Exception()

        word = word.lower()
        wordJobs = db[word]
        if site == 'all':
            jobs += wordJobs['WWR']
            jobs += wordJobs['Stackoverflow']
            jobs += wordJobs['Remoteok']
        else:
            jobs = wordJobs[site]

        if not jobs:
            raise Exception()

        save_to_file(jobs, word, site)
        return send_file(f"{word}-{site}.csv",
                         mimetype='text/csv',
                         as_attachment=True,
                         attachment_filename=f'{word}-{site}.csv')
    except:
        return redirect(f'/report?word={word}')


app.run(host="0.0.0.0")
