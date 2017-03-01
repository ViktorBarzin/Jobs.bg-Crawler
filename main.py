import sys
from urllib.parse import quote
from urllib import request
from bs4 import BeautifulSoup, SoupStrainer


home_page = 'https://www.jobs.bg'

def get_all_jobs_on_page(response):
    # Parse job urls
    job_urls = []
    soup = BeautifulSoup(response, 'html.parser')
    for link in soup.find_all('a'):
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


def search_for_job(host='https://www.jobs.bg',keywords='', all_pages=False):
    # Jobs.bg specific get params
    get_params = 'front_job_search.php?first_search=1&distance=0&location_sid=&all_categories=0&all_type=0&all_position_level=1'
    # Prepare keywords to insert into query
    keyword = quote(keywords.replace(' ', '+'))
    final_query_url = 'https://www.jobs.bg/{}&keyword={}'.format(get_params, keyword)

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


def main():
    if len(sys.argv) != 2:
        print('Usage: python main.py keywords,separated,by,comma')
        return
    keywords = sys.argv[1].split(',')

    for keyword in keywords:
        jobs = search_for_job('https://www.jobs.bg', keyword, all_pages=True)
        # This weird string makes the console output color light green
        # '\033[1;32mGreen like Grass\033[1;m'
        print('\033[1;32m[+] Found {} job results for keyword "{}"\033[1;m'.format(len(jobs), keyword))
        print()
        print('\033[1;32m[+] Diplaying first 10 results\033[1;m')
        print('\n'.join(jobs[:10]))
        print()


if __name__ == "__main__":
    main()
