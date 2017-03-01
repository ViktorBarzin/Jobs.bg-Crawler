class Job(object):
    title = ''
    description = ''
    requirements = ''
    benefits = ''

    def __init__(self, url):
        self.url = url
