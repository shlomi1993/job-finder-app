
import argparse
import sys
import yaml

from src.job_finder import find_jobs, export_to_csv


def load_yaml_list(file_path, key):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict) or key not in data:
        sys.exit(f'Error: {file_path} must contain a "{key}:" list')
    return [str(item).strip() for item in data[key] or [] if str(item).strip()]


def main():
    parser = argparse.ArgumentParser(description='Job Finder App')

    search_group = parser.add_mutually_exclusive_group(required=True)
    search_group.add_argument('--search', type=str, help='Comma-separated job search keywords')
    search_group.add_argument('--search-yaml', type=str, help='YAML file with job search keywords')

    filter_group = parser.add_mutually_exclusive_group()
    filter_group.add_argument('--filter', type=str, help='Comma-separated exclusion keywords')
    filter_group.add_argument('--filter-yaml', type=str, help='YAML file with exclusion keywords')

    parser.add_argument('--location', type=str, default='Tel Aviv', help='Job location (default: Tel Aviv)')
    parser.add_argument('--cities', type=str, help='Comma-separated cities to keep, e.g. "Tel Aviv, Ramat Gan" (default: all)')
    parser.add_argument('--output', type=str, default='relevant_jobs.csv', help='Output CSV file path')
    parser.add_argument('--max-results', type=int, help='Maximum number of jobs to find (default: no limit)')
    parser.add_argument('--max-days-old', type=int, default=30, help='Maximum age of job postings in days (default: 30)')
    parser.add_argument('--open', action='store_true', help='Open the CSV file after creation')
    args = parser.parse_args()

    # Load searches
    if args.search_yaml:
        searches = load_yaml_list(args.search_yaml, 'searches')
    else:  # Assume args.search is provided
        searches = [s.strip() for s in args.search.split(',') if s.strip()]

    if not searches:
        sys.exit('Error: no search keywords given')

    # Load filters
    if args.filter_yaml:
        bad_words = load_yaml_list(args.filter_yaml, 'filters')
    elif args.filter:
        bad_words = [f.strip() for f in args.filter.split(',') if f.strip()]
    else:  # Assume no filters
        bad_words = []

    cities = [c.strip() for c in args.cities.split(',') if c.strip()] if args.cities else None

    jobs = find_jobs(searches, location=args.location, max_results=args.max_results, max_days_old=args.max_days_old,
                     bad_words=bad_words, cities=cities)
    export_to_csv(jobs, output_file_path=args.output, open_file=args.open)


if __name__ == '__main__':
    main()
