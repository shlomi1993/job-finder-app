# Job Finder App

This repository contains a script for programmatically searching and filtering relevant job postings from LinkedIn based on custom search terms and exclusion keywords.

The goal of this app is to automate the job search process for specific roles (e.g., "junior machine learning engineer") in a given location (e.g., "Tel Aviv"), while filtering out irrelevant or undesirable results (e.g., senior positions, team leads, etc.).

## Features

- Automatically search LinkedIn job postings using multiple keyword combinations.
- Filter out jobs by undesirable terms (e.g., "senior", "manager", "analyst", etc.).
- Collect job metadata (title, company, location, post date, link).
- Export results to a CSV file sorted by post date.

## Repository Structure

- **`main.py`**  
  The main script to run the job finder with pre-defined search terms and filters.

- **`src/job_finder.py`**
  Core module that performs scraping, parsing, filtering, and exporting.

- **`src/utils.py`**
  Utility functions like custom logging (not shown here).


## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/shlomi1993/job-finder-app.git
cd job-finder-app
```

### 2. Install required dependencies

```bash
pip install -r requirements.txt
```

## Usage

Run the main script using command-line arguments:

```bash
python main.py --search "backend engineer, machine learning engineer" --filter "senior, manager"
```

Or use YAML files for configuration:

```bash
python main.py --search-yaml searches.yaml --filter-yaml filters.yaml
```

You can also specify location and output file:

```bash
python main.py --location "Tel Aviv" --output results.csv
```

Additional options:

```bash
python main.py --search "backend engineer" --max-results 50 --max-days-old 14
```

All available options:
- `--search`: Comma-separated job search keywords
- `--search-yaml`: YAML file with job search keywords
- `--filter`: Comma-separated exclusion keywords
- `--filter-yaml`: YAML file with exclusion keywords
- `--location`: Job location (default: Tel Aviv)
- `--output`: Output CSV file path (default: relevant_jobs.csv)
- `--max-results`: Maximum number of jobs to find (no limit by default)
- `--max-days-old`: Maximum age of job postings in days (default: 30)

If no arguments are provided, the app will require you to specify either `--search` or `--search-yaml`.

### Results will be saved to:

```
relevant_jobs.csv
```

## Customization

- To change search keywords, edit the `searches.yaml` file.
- To exclude specific job types or roles, modify the `filters.yaml` file.
- Change the location by using the `--location` argument.
- Change the output file name with the `--output` argument.

## Example YAML Files

**searches.yaml**
```yaml
searches:
  - machine learning
  - backend engineer
  - computer vision engineer
```

**filters.yaml**
```yaml
filters:
  - senior
  - manager
  - staff
```

## Output

The output CSV includes the following columns:

- Job URN
- Title
- Company
- Location
- Post Date
- Direct Link to Job

## Disclaimer ⚠️

This script relies on the LinkedIn guest job search API and may break if the site's structure or access policies change. Use responsibly and in compliance with LinkedIn’s terms of service.
