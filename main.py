from src.job_finder import find_jobs, export_to_csv


def main():
    searches = [
        # 'software developer',
        # 'software engineer',
        # 'backend developer',
        # 'backend engineer',
        # 'full stack developer',
        # 'full stack engineer',
        # 'frontend developer',
        # 'frontend engineer',
        'python developer',
        'python engineer',
        'c++ developer',
        'c++ engineer',
        # 'c developer',
        # 'c engineer',
        'artificial intelligence'
        'ai engineer',
        'junior machine learning',
        'junior machine learning engineer',
        'junior ml engineer',
        'machine learning',
        'machine learning engineer',
        'ml engineer',
        'deep learning',
        'deep learning engineer',
        'computer vision',
        'computer vision engineer'
    ]

    bad_words = [
        'senior',
        'sr.',
        'sr',
        'experienced',
        'staff',
        'manual',
        'team lead',
        'leader',
        'cobol',
        'specialist',
        'manager',
        'soc',
        'technical support',
        'help desk',
        'student',
        'director',
        'system architect',
        'system administrator',
        'expert',
        'system security architect',
        'business analyst',
        'director of',
        'head of',
        'data analyst',
        'office administrator',
        'executive assistant',
        'data scientist',
        'business intelligence',
        'security engineer',
        'systems engineer',
        'tech support',
        'bi developer',
        'automation',
        'validation',
        'verification',
        'qa ',
        'quality assurance',
        'board design',
        'blockchain',
        'principal',
        'chief',
        'vlsi',
        'fpga',
        'lead',
        'tester'
    ]

    jobs = find_jobs(searches, location='Tel Aviv', bad_words=bad_words)
    export_to_csv(jobs)


if __name__ == '__main__':
    main()
