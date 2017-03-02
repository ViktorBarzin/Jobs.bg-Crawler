import sys
from bs4 import BeautifulSoup, SoupStrainer
from urllib import request
from urllib.parse import quote
import argparse

# Benchmark decorator displays time for executing a method
from decorators import benchmark


home_page = 'https://www.jobs.bg'
job_types = {
        'all types': ('all_type', 0),
        'full time': ('job_type[]', 1),
        'part time': ('job_type[]', 2),
        'internship': ('job_type[]', 4)
}

job_hours = {
        'full time': ('job_hours[]', 1),
        'not full time': ('job_hours[]',2)
}

suitable_for_students = {
        'for students': ('is_student', 1)
}


def get_all_jobs_on_page(response):
    # Parse job urls
    job_urls = []
    # soup = BeautifulSoup(response, 'html.parser')
    # for link in soup.find_all('a'):
    for link in BeautifulSoup(response, 'html.parser', parse_only=SoupStrainer('a')):
        if link.has_attr('class') and link['class'][0] == 'joblink' and link.has_attr('href'):
            job_urls.append('{}/{}'.format(home_page, link['href']))
    return job_urls


def get_next_page_url(response):
    # links = []
    for link in BeautifulSoup(response,'html.parser', parse_only=SoupStrainer('a')):
        # The link to the next page is something as follows: '<a href=".." class="pathlink">>></a>'
        if link.has_attr('class') and link['class'][0] == 'pathlink' and link.text == '>>':
            return home_page + '/' + link['href']
    return ''


def search_for_job(host='https://www.jobs.bg',keywords='',job_type=[], all_pages=False):
    # Jobs.bg specific get params
    # Looking for jobs in IT sector
    import ipdb; ipdb.set_trace()# BREAKPOINT)

    # Prepare job_type to insert into query
    if job_type:
        job_type_url = '&{}={}'.format(job_type[0], job_type[1])
    else:
        job_type_url = ''
    get_params = 'front_job_search.php?first_search=1&distance=0&location_sid=&categories[]=14&categories[]=15&categories[]=16{}&all_position_level=1'.format(job_type_url)
    # Prepare keywords to insert into query
    keyword = quote(keywords.replace(' ', '+'))
    final_query_url = 'https://www.jobs.bg/{}&keyword={}'.format(get_params, keyword)

    response = request.urlopen(final_query_url).read()

    if all_pages:
        # logic to check all pages
        jobs = []
        next_page_url = get_next_page_url(response)

        while next_page_url:
            # print('getting all jobs')
            jobs.extend(get_all_jobs_on_page(response))
            # print('getting next page')
            response = request.urlopen(next_page_url).read()
            # print('getting next page url')
            next_page_url = get_next_page_url(response)
        # Fetching the jobs on the last page
        jobs.extend(get_all_jobs_on_page(response))
        return jobs
    else:
        return get_all_jobs_on_page(response)


# @benchmark
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--keywords', nargs='+', required = True, help='filter jobs by keywords, separated with space (" ")')
    parser.add_argument('--job-type', choices = list(job_types.keys()), help='filter job by type')

    # Get if should look on all pages or only first
    parser.add_argument('--all-pages', dest='all_pages', action='store_true', help='sets a flag wheter to scan all pages or just first')
    # parser.add_argument('--first-page', dest='all_pages', action='store_false')
    parser.set_defaults(all_pages=False)


    args = parser.parse_args()
    keywords = args.keywords if args.keywords else ['']
    user_job_type = job_types.get(args.job_type, 'all jobs')

    for keyword in keywords:
        jobs = search_for_job('https://www.jobs.bg', keyword,job_type=user_job_type, all_pages=args.all_pages)
        # This weird string makes the console output color light green
        # '\033[1;32mGreen like Grass\033[1;m'
        print('\033[1;32m[+] Found {} job results for keyword "{}"\033[1;m'.format(len(jobs), keyword))
        print()
        print('\033[1;32m[+] Diplaying first 10 results\033[1;m')
        print('\n'.join(jobs[:10]))
        print()


if __name__ == "__main__":
    main()
