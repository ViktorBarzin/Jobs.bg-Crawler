import sys
from bs4 import BeautifulSoup, SoupStrainer
from urllib import request
from urllib.parse import quote

# Benchmark decorator displays time for executing a method
from decorators import benchmark
from helpers import setup_parser, print_jobs, job_hours, job_level, job_types


home_page = 'https://www.jobs.bg'

def get_all_jobs_on_page(response):
    # Parse job urls
    job_urls = []
    for link in BeautifulSoup(response, 'html.parser', parse_only=SoupStrainer('a')):
        if link.has_attr('class') and link['class'][0] == 'joblink' and link.has_attr('href'):
            job_urls.append('{}/{}'.format(home_page, link['href']))
    return job_urls


def get_next_page_url(response):
    for link in BeautifulSoup(response,'html.parser', parse_only=SoupStrainer('a')):
        # The link to the next page is something as follows: '<a href=".." class="pathlink">>></a>'
        if link.has_attr('class') and link['class'][0] == 'pathlink' and link.text == '>>':
            return home_page + '/' + link['href']
    return ''


def tuple_to_url_param(inp):
    # Transforms a tuple with arguments to jobs.bg get params
    if inp and len(inp) >= 2:
        return '&{}={}'.format(inp[0], inp[1])
    return ''

def search_for_job(host='https://www.jobs.bg',params={}, all_pages=False):
    # Looking for jobs in IT sector

    # If you want to search in another categories, fiddle with the categories
    # parameter in the get_params string below

    # Prepare keywords to insert into query
    # does inner join on all passed keywords
    keywords = [quote(x) for x in params.pop('keywords')]
    keyword = '&keyword={}'.format('+'.join(keywords))

    for key, value in params.items():
        params[key] = tuple_to_url_param(value)

    get_params = 'front_job_search.php?first_search=1&distance=0&location_sid=&categories[]=14&categories[]=15&categories[]=16&all_position_level=1'
    get_params += ''.join(params.values())
    get_params += keyword

    final_query_url = 'https://www.jobs.bg/{}'.format(get_params)

    response = request.urlopen(final_query_url).read()

    if all_pages:
        # logic to check all pages
        jobs = []
        next_page_url = get_next_page_url(response)

        while next_page_url:
            jobs.extend(get_all_jobs_on_page(response))
            response = request.urlopen(next_page_url).read()
            next_page_url = get_next_page_url(response)
        # Fetching the jobs on the last page
        jobs.extend(get_all_jobs_on_page(response))
        return jobs
    else:
        return get_all_jobs_on_page(response)


# @benchmark
def main():
    parser = setup_parser()
    args = parser.parse_args()

    # expected input:" --keywords="kw1 kw2 kw3"
    keywords = args.keywords.split(' ') if args.keywords else ['']
    # Consider adding some default values to search with
    user_job_type = job_types.get(args.job_type, '')
    user_job_time = job_hours.get(args.job_time, '')
    user_job_position = job_level.get(args.position, '')

    params = {'keywords':keywords, 'job_type': user_job_type, 'job_time': user_job_time, 'job_position': user_job_position}

    jobs = search_for_job('https://www.jobs.bg', params=params, all_pages=args.all_pages)
    print_jobs(jobs, keywords, args.all_pages)

if __name__ == "__main__":
    main()

