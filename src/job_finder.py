import csv
import os
import requests
import re
import subprocess

from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep
from urllib.parse import urlencode


JOB_SEARCH_API_URL = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search'
JOB_VIEW_BASE_URL = 'https://www.linkedin.com/jobs/view/{}'

API_MAX_JOB_POSTS = 1000
REQUEST_TIMEOUT_SEC = 15
MAX_RETRIES = 4


def get_job_list(keywords: str, location: str, start: int, max_days_old: int = None) -> list[BeautifulSoup]:
    params = {'keywords': keywords, 'location': location, 'start': start}
    if max_days_old:
        # Ask LinkedIn for recent posts only, otherwise its limited result set is mostly old posts that get filtered out
        params['f_TPR'] = f'r{max_days_old * 24 * 60 * 60}'
    url = JOB_SEARCH_API_URL + '?' + urlencode(params)
    # print(' * Fetch: ' + url)
    for attempt in range(1, MAX_RETRIES + 1):
        sleep(1)  # To avoid hitting the API too fast
        try:
            res = requests.get(url, timeout=REQUEST_TIMEOUT_SEC)
        except requests.RequestException as e:
            reason = type(e).__name__
        else:
            if res.ok:
                return BeautifulSoup(res.text, 'html.parser').find_all('li')
            if res.status_code not in (429, 500, 502, 503, 504):
                print(f'Could not fetch {res.url} - response status code: {res.status_code}')
                return []
            reason = f'status code {res.status_code}'
        backoff = 5 * attempt
        print(f'Request failed ({reason}), retry {attempt}/{MAX_RETRIES} in {backoff}s...')
        sleep(backoff)
    print(f'Giving up on {url}')
    return []


def parse_detail(soup: BeautifulSoup, tag: str, class_value: str) -> str:
    attrs = {'class': class_value}
    element = soup.find(tag, attrs)
    if not element:
        print(f'The tag "{tag}" with attributes {attrs} was not found')
        return None
    return element.text.strip()


def normalize_place(name: str) -> str:
    # "Tel Aviv-Yafo" -> "tel aviv yafo", "Giv'atayim" -> "givatayim"
    return name.lower().replace('-', ' ').replace("'", '').strip()


def contains_bad_word(title: str, bad_words: list[str]) -> bool:
    # Match whole words only, so "intern" excludes "Intern" but not "Internal" or "International"
    return any(re.search(rf'(?<!\w){re.escape(bw)}(?!\w)', title, re.IGNORECASE) for bw in bad_words)


def process_job(job_li: BeautifulSoup, jobs: dict, bad_words: list[str], max_days_old: int, cities: list[str] = None) -> None:

    # Get unique job ID
    match = re.search(r'jobPosting:(\d+)', str(job_li))
    if match:
        job_id = match.group(1)
    else:
        print('Could not find job URN!')
        return
    if job_id in jobs.keys():
        return

    # Parse title and filter titles with bad words
    job_title = parse_detail(job_li, tag='h3', class_value='base-search-card__title')
    if not job_title:
        return
    if bad_words and contains_bad_word(job_title, bad_words):
        return

    # Parse date and filter old job posts
    time_tag = job_li.find('time')
    if not time_tag or 'datetime' not in time_tag.attrs:
        return
    date_posted = datetime.strptime(time_tag.attrs['datetime'], '%Y-%m-%d')
    date_delta = datetime.now() - date_posted
    if date_delta.days > max_days_old:
        return

    # Parse company name and job location
    company_name = parse_detail(job_li, tag='h4', class_value='base-search-card__subtitle') or ''
    job_location = parse_detail(job_li, tag='span', class_value='job-search-card__location') or ''
    if cities:
        city = normalize_place(job_location.split(',')[0])  # e.g. "Or Yehuda" out of "Or Yehuda, Tel Aviv District, Israel"
        if not any(normalize_place(c) in city for c in cities):
            return

    # Skip reposts of the same role (same title and company under a new job ID), keeping the newest post
    for other_id, other in list(jobs.items()):
        if other['title'].lower() == job_title.lower() and other['company'].lower() == company_name.lower():
            if other['posted'] >= date_posted:
                return
            del jobs[other_id]

    # Map job ID to a new job dict
    jobs[job_id] = {
        'title': job_title,
        'company': company_name,
        'location': job_location,
        'posted': date_posted,
        'link': JOB_VIEW_BASE_URL.format(job_id)
    }
    print(f' - Found \033[96m{job_title}\033[0m at {company_name} in {jobs[job_id]["location"]}')


def find_jobs(searches: list[str], location: str, max_results: int = None, max_days_old: int = 30, bad_words: list[str] = None,
              cities: list[str] = None) -> dict:
    print('Job search started...')
    jobs = dict()
    prev_n_found_jobs = 0
    for i, keywords in enumerate(searches, start=1):
        print(f'\033[94mSearching keywords ({i}/{len(searches)}): "{keywords}"\033[0m')
        start = 0
        while start < API_MAX_JOB_POSTS:
            jobs_on_page = get_job_list(keywords, location, start, max_days_old)
            if len(jobs_on_page) == 0:
                break
            for job_html_li in jobs_on_page:
                process_job(job_html_li, jobs, bad_words, max_days_old, cities)
                if len(jobs) == max_results:
                    return jobs
            start += len(jobs_on_page)  # The API page size varies (currently 10), so advance by what was returned
        print(f'\033[93m*** Found {len(jobs) - prev_n_found_jobs} new positions in the last search, {len(jobs)} in total ***\033[0m\n')
        prev_n_found_jobs = len(jobs)
    return jobs


def export_to_csv(job_dict: dict, output_file_path: str = 'relevant_jobs.csv', open_file: bool = False) -> None:
    print('Writing CSV file...')
    job_dict = dict(sorted(job_dict.items(), key=lambda item: item[1]['posted'], reverse=True))
    headers = ['URN', 'Title', 'Company', 'Location', 'Post date', 'Link']
    with open(output_file_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for job_id, job in job_dict.items():
            data = [job_id, job['title'], job['company'], job['location'], job['posted'].strftime('%d.%m.%Y'), job['link']]
            print(f'Writing job ID {job_id}: {job["title"]} at {job["company"]}, in {job["location"]}')
            writer.writerow(data)
    print(f'\n\033[92mCSV file created: {os.path.abspath(output_file_path)}\033[0m')
    if open_file:
        subprocess.run(['open', output_file_path], check=True)
