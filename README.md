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

## Usage

### Install required dependencies:

```bash
pip install beautifulsoup4 requests
````

### Run the main script:

```bash
python main.py
```

### Results will be saved to:

```
relevant_jobs.csv
```

## Customization

* To change search keywords, edit the `searches` list in `main.py`.
* To exclude specific job types or roles, modify the `bad_words` list.
* Change the location by updating the `location` parameter in `find_jobs()`.

## Example Search Terms

```python
searches = [
    'machine learning',
    'junior ml engineer',
    'computer vision engineer',
    'deep learning',
    ...
]
```

## Example Exclusion Terms

```python
bad_words = [
    'senior', 'manager', 'staff', 'qa', 'data analyst',
    'team lead', 'principal', 'blockchain', ...
]
```

## Output

The output CSV includes the following columns:

* Job URN
* Title
* Company
* Location
* Post Date
* Direct Link to Job


## Disclaimer ⚠️

This script relies on the LinkedIn guest job search API and may break if the site's structure or access policies change. Use responsibly and in compliance with LinkedIn’s terms of service.
