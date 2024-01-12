import requests
import re
import csv

from bs4 import BeautifulSoup
from typing import List
from datetime import datetime

from src.utils import get_logger


JOB_SEARCH_API_URL = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search'
JOB_POST_BASE_URL = 'https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{}'
JOB_VIEW_BASE_URL = 'https://www.linkedin.com/jobs/view/{}'

N_JOBS_PER_PAGE = 25

LOGGER = get_logger('Job-Finder')


def get_job_list(keywords: str, location: str, start: int) -> List[BeautifulSoup]:
    res = requests.get(JOB_SEARCH_API_URL, params={'keywords': keywords, 'location': location, 'start': start})
    if not res.ok:
        LOGGER.warning(f'Could not fetch {res.url} - response status code: {res.status_code}')
        return []
    return BeautifulSoup(res.text, 'html.parser').find_all('li')


def parse_detail(soup: BeautifulSoup, tag: str, class_value: str) -> str:
    attrs = {'class': class_value}
    element = soup.find(tag, attrs)
    if not element:
        LOGGER.warning(f'The tag "{tag}" with attributes {attrs} was not found')
        return None
    return element.text.strip()


def contains_bad_word(title: str, bad_words: List[str]) -> bool:
    title = title.lower()
    return any(bw.lower() in title for bw in bad_words)


def process_job(job_li: BeautifulSoup, jobs: dict, bad_words: List[str], max_days_old: int) -> None:

    # Get unique job ID
    match = re.search(r'jobPosting:(\d+)', str(job_li))
    if match:
        job_id = match.group(1)
    else:
        LOGGER.warning('Could not find job URN!')
        return
    if job_id in jobs.keys():
        return

    # Parse title and filter titles with bad words
    job_title = parse_detail(job_li, tag='h3', class_value='base-search-card__title')
    if bad_words and contains_bad_word(job_title, bad_words):
        return

    # Parse date and filter old job posts
    date_posted = datetime.strptime(job_li.find('time').attrs['datetime'], '%Y-%m-%d')
    date_delta = datetime.now() - date_posted
    if date_delta.days > max_days_old:
        return

    # Parse comapny name and job location
    company_name = parse_detail(job_li, tag='h4', class_value='base-search-card__subtitle')
    job_location = parse_detail(job_li, tag='span', class_value='job-search-card__location')

    # Map job ID to a new job dict
    jobs[job_id] = {
        'title': job_title,
        'company': company_name,
        'location': job_location,
        'posted': date_posted.strftime('%d.%m.%Y'),
        'link': JOB_VIEW_BASE_URL.format(job_id)
    }
    LOGGER.info(f' - Found {job_title} at {company_name} in {jobs[job_id]["location"]}')


def find_jobs(searches: List[str], location: str, max_results: int = None, max_days_old: int = 7,
              bad_words: List[str] = None) -> dict:
    LOGGER.info('Job search started...')
    jobs = dict()
    for keywords in searches:
        LOGGER.info(f'Searching keywords: "{keywords}"')
        start = 0
        while True:
            jobs_on_page = get_job_list(keywords, location, start)
            for job_html_li in jobs_on_page:
                process_job(job_html_li, jobs, bad_words, max_days_old)
                if len(jobs) == max_results:
                    break
            if len(jobs) == max_results:
                break
            start += N_JOBS_PER_PAGE
        LOGGER.info('-------------------- Search End --------------------')
    return jobs


def export_to_csv(job_dict: dict, output_file_path: str = 'relevant_jobs.csv') -> None:
    LOGGER.info('Writing CSV file...')
    headers = ['URN', 'Title', 'Comapny', 'Location', 'Post date', 'Link']
    with open(output_file_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for job_id, job in job_dict.items():
            data = [job_id, job['title'], job['company'], job['location'], job['posted'], job['link']]
            LOGGER.info(f'Writing job ID #{job_id}: {job["title"]} at {job["company"]}, in {job["location"]}')
            writer.writerow(data)
        LOGGER.info('CSV file created.')
