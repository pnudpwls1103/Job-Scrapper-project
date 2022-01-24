import csv

def save_to_file(jobs, word, site):
  print(f"[[Export {word}-{site}.csv]]")
  file = open(f"{word}-{site}.csv", mode="w")
  writer = csv.writer(file)
  writer.writerow(["title", "company", "link"])
  for job in jobs:
    writer.writerow(list(job.values()))