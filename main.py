import httplib2
import sys
from urllib import quote
from BeautifulSoup import BeautifulSoup, SoupStrainer


home_page = 'https://www.jobs.bg'

def get_all_jobs_on_page(response):
    # Assert this is the last page
    global last_page
    last_page = False

    # Parse job urls
    job_urls = []
    for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
        if link.has_key('class') and link['class'].decode('utf-8') == 'joblink' and link.has_key('href'):
            job_urls.append('{}/{}'.format(home_page, link['href']))

        # Check if last page so no need to iterate to response in another
        # function
        if link.has_key('class') and link['class'] == 'pathlink':
            set_last_page_flag(True)
    # import ipdb; ipdb.set_trace()# BREAKPOINT)

    return job_urls


def get_next_page_url(response):
    for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
        # The link to the next page is something as follows: '<a href=".." class="pathlink">>></a>'
        if link.has_key('class') and link['class'] == 'pathlink' and link.text == '&gt;&gt;':
            return home_page + '/' + link['href']
    return ''


def search_for_job(host='https://www.jobs.bg',keywords='', all_pages=False):
    global last_page
    get_params = 'front_job_search.php?first_search=1&distance=0&location_sid=&all_categories=0&all_type=0&all_position_level=1'
    keyword = quote(keywords.replace(' ', '+'))
    http = httplib2.Http()
    final_query_url = 'https://www.jobs.bg/{}&keyword={}'.format(get_params, keyword)
    status, response = http.request(final_query_url)

    if all_pages:
        # make logic to list all pages
        jobs = []
        next_page_url =get_next_page_url(response)

        while next_page_url:
            jobs.extend(get_all_jobs_on_page(response))
            status, response = http.request(next_page_url)
            next_page_url = get_next_page_url(response)
        # Fetching the jobs on thelast page
        jobs.extend(get_all_jobs_on_page(response))
        return jobs
    else:
        return get_all_jobs_on_page(response)


def set_last_page_flag(bool_value):
    global last_page
    last_page = bool_value



def main():
    # keywords = ['python', 'linux', 'C#' ]
    if len(sys.argv) != 2:
        print('Usage: python main.py keywords,separated,by,comma')
        return
    keywords = sys.argv[1].split(',')

    for keyword in keywords:
        jobs = search_for_job('https://www.jobs.bg', keyword, all_pages=True)
            # for jobs in jobs:
# '\033[1;32mGreen like Grass\033[1;m'
        print('\033[1;32m[+] Found {} job results for keyword "{}"\033[1;m'.format(len(jobs), keyword))
        print
        print('\033[1;32m[+] Diplaying first 10 results\033[1;m')
        print('\n'.join(jobs[:10]))
        print
    # jobs_links = search_for_job(keywords='python', all_pages=True)




if __name__ == "__main__":
    main()
