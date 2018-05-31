import requests
import time
from lxml import html
from Bio import Entrez


def entrez_timer_gen():
    while True:
        yield
        yield
        yield
        time.sleep(1)


entrez_timer = entrez_timer_gen()


def entrez_fetch(db, **kwargs):
    """
    Interface to Entrez.efetch that reads email from `ENTREZ_EMAIL` environment variable and automatically rate limits
    to three requests per second
    (per https://www.ncbi.nlm.nih.gov/books/NBK25497/#chapter2.Usage_Guidelines_and_Requiremen).
    """
    next(entrez_timer)
    return Entrez.efetch(db, **kwargs)


sesh = requests.session()


def login(rosalind_user, rosalind_password):
    """
    Logs into http://rosalind.info/, reading credentials from `ROSALIND_USER` and `ROSALIND_PASSWORD` environment
    variables.
    """
    response = sesh.get('http://rosalind.info/accounts/login/')
    payload = {
        'username': rosalind_user,
        'password': rosalind_password,
        'next': '',
        'csrfmiddlewaretoken': response.cookies['csrftoken']
    }
    sesh.post('http://rosalind.info/accounts/login/', data=payload)


SOLVERS = {}


def solves(problem_url):
    def decorator(fn):
        def decorated(rosalind_user, rosalind_password, *args, entrez_email=None, **kwargs):
            login(rosalind_user, rosalind_password)
            dataset = sesh.get(problem_url + 'dataset').text.strip()
            Entrez.email = entrez_email
            answer = fn(dataset=dataset)
            response = sesh.post(problem_url, data={
                'output_text': answer,
                'csrfmiddlewaretoken': sesh.get(problem_url).cookies['csrftoken']
            })
            doc = html.fromstring(response.content)
            result = doc.xpath(".//div[@class='problem-solved ']")[0].text_content().strip().split('\n')[0]
            print("%s:\t%s" % (problem_url, result))
            return answer
        SOLVERS[problem_url] = decorated
        return decorated
    return decorator
