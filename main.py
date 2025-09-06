
import argparse
import yaml

from src.job_finder import find_jobs, export_to_csv


def load_yaml_list(file_path, key):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
        return data.get(key, [])


def main():
    parser = argparse.ArgumentParser(description='Job Finder App')

    search_group = parser.add_mutually_exclusive_group(required=True)
    search_group.add_argument('--search', type=str, help='Comma-separated job search keywords')
    search_group.add_argument('--search-yaml', type=str, help='YAML file with job search keywords')

    filter_group = parser.add_mutually_exclusive_group()
    filter_group.add_argument('--filter', type=str, help='Comma-separated exclusion keywords')
    filter_group.add_argument('--filter-yaml', type=str, help='YAML file with exclusion keywords')

    parser.add_argument('--location', type=str, default='Tel Aviv', help='Job location (default: Tel Aviv)')
    parser.add_argument('--output', type=str, default='relevant_jobs.csv', help='Output CSV file path')
    parser.add_argument('--max-results', type=int, help='Maximum number of jobs to find (default: no limit)')
    parser.add_argument('--max-days-old', type=int, default=30, help='Maximum age of job postings in days (default: 30)')
    args = parser.parse_args()

    # Load searches
    if args.search_yaml:
        searches = load_yaml_list(args.search_yaml, 'searches')
    else:  # Assume args.search is provided
        searches = [s.strip() for s in args.search.split(',') if s.strip()]

    # Load filters
    if args.filter_yaml:
        bad_words = load_yaml_list(args.filter_yaml, 'filters')
    elif args.filter:
        bad_words = [f.strip() for f in args.filter.split(',') if f.strip()]
    else:  # Assume no filters
        bad_words = []

    jobs = find_jobs(searches, location=args.location, max_results=args.max_results,  max_days_old=args.max_days_old, bad_words=bad_words)
    export_to_csv(jobs, output_file_path=args.output)


if __name__ == '__main__':
    main()
