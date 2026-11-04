# Job Finder App

[![Python](https://img.shields.io/badge/python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux-lightgrey)](#)
[![Last commit](https://img.shields.io/github/last-commit/shlomi1993/job-finder-app)](https://github.com/shlomi1993/job-finder-app/commits)
[![Repo size](https://img.shields.io/github/repo-size/shlomi1993/job-finder-app)](https://github.com/shlomi1993/job-finder-app)

A command-line tool that automates the repetitive part of a job search. Give it the job titles you are looking for and the words you want to avoid (such as `senior` or `intern`), and it runs every search on LinkedIn's public job listings, removes duplicates and irrelevant roles, and skips stale postings.

The results are saved to a single CSV file, newest first, with a direct link to each posting, ready to open in Excel, Numbers or Google Sheets.

## Features

1. Search many keyword combinations in one run
2. Exclude jobs whose titles contain unwanted words (e.g. `senior`, `intern`)
3. Skip postings older than a given number of days
4. Automatic retries on timeouts and rate limiting
5. CSV output: title, company, location, post date and link

## Quick Start

```bash
git clone https://github.com/shlomi1993/job-finder-app.git
cd job-finder-app
./install.sh
source job-finder-venv/bin/activate
```

Quick test (5 results):

```bash
python main.py --search "project manager" --filter "senior, intern" --max-results 5
```

## Usage

```bash
# Keywords from the command line
python main.py --search "graphic designer, ux designer" --filter "senior, director" --location "London"

# Keywords from YAML files
python main.py --search-yaml searches.yaml --filter-yaml filters.yaml --max-days-old 14 --open

# Search the Tel Aviv area but keep only some of its cities
python main.py --search "accountant" --cities "Tel Aviv, Ramat Gan, Herzliya"
```

| Option | Description | Default |
|---|---|---|
| `--search` / `--search-yaml` | Search keywords (comma-separated or YAML) — **required** | — |
| `--filter` / `--filter-yaml` | Words to exclude from job titles | none |
| `--location` | Job location | `Tel Aviv` |
| `--cities` | Keep only jobs in these cities (comma-separated) | all |
| `--output` | Output CSV path | `relevant_jobs.csv` |
| `--max-results` | Stop after N jobs | no limit |
| `--max-days-old` | Max posting age in days | `30` |
| `--open` | Open the CSV when done (macOS) | off |

Keywords and filters are case-insensitive: `Senior`, `senior` and `SENIOR` are treated the same.

YAML format:

`searches.yaml`

```yaml
searches:
  - accountant
  - sales representative
```

`filters.yaml`

```yaml
filters:
  - senior
  - intern
```

## Disclaimer

This tool uses LinkedIn's public guest job search API and may break if LinkedIn changes it. Use responsibly and in line with LinkedIn's terms of service.
