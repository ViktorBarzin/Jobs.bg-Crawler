import argparse


job_types = {
        'all jobs': ('all_type', 0),
        'full time': ('job_type[]', 1),
        'part time': ('job_type[]', 2),
        'internship': ('job_type[]', 4)
}

job_hours = {
        'full time': ('job_hours[]', 1),
        'hourly': ('job_hours[]',2)
}

# not used yet because seems useless
suitable_for_students = {
        'for students': ('is_student', 1)
}


# jobs.bg job level defaults to 1 -> management (weird?)
job_level = {
        'management': ('position_level[]', 1),
        'team lead': ('position_level[]', 3),
        'expert': ('position_level[]', 4),
        'workers': ('position_level[]', 5)
}


def setup_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('--keywords', required = True, help='filter jobs by keywords, separated with space (" ")')
    parser.add_argument('--job-type', choices = list(job_types.keys()), help='filter job by type')
    parser.add_argument('--job-time', choices = list(job_hours.keys()), help = 'full 8 hour work day or hourly jobs')
    parser.add_argument('--position', choices = list(job_level.keys()), help = 'job position')
    # Get if should look on all pages or only first
    parser.add_argument('--all-pages', dest='all_pages', action='store_true', help='sets a flag whether to scan all pages(default scans only first)')
    parser.set_defaults(all_pages=False)

    return parser


def print_jobs(jobs, search_keywords, all_pages):
    # This weird string makes the console output color light green
    # '\033[1;32mGreen like Grass\033[1;m'

    # RIP DRY, but w/e another time
    if not all_pages:
        print('\033[1;32m[+] Showing job results for keywords "{}" from first page only!\nTo scan all pages use "--all-pages" argument\033[1;m'.format(' '.join(search_keywords)))
        print()
        print('\n'.join(jobs))
        print()
        return
    else:
        print('\033[1;32m[+] Found {} job results for keywords "{}"\033[1;m'.format(len(jobs), ' '.join(search_keywords)))
    print()
    print('\033[1;32m[+] Diplaying first 10 results\033[1;m')
    print('\n'.join(jobs[:10]))
    print()


