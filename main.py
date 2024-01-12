from src.job_finder import find_jobs, export_to_csv


def main():
    searches = [
        'software developer',
        # Add your search keywords here
    ]

    bad_words = [
        'senior',
        'sr',
        'quality assurance',
        # Add words that you do not want to have in the title
    ]

    jobs = find_jobs(searches, location='Tel Aviv', max_results=50, bad_words=bad_words)
    export_to_csv(jobs)


if __name__ == '__main__':
    main()
