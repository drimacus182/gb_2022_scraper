from bs4 import BeautifulSoup
from datetime import datetime
import pytz


tz = pytz.timezone('Europe/Kiev')


def parse_datetime(val):
    t = tz.localize(
        datetime.strptime(val, "%d.%m.%Y о %H:%M")
    )

    return t.isoformat()


def _read_stub():
    """
    For testing purposes only
    """
    with open('stubs/project_page.html') as f:
        return f.read()


def get_votes_table(soup):
    voted_table = soup.select_one('.voted_table')

    rows = voted_table.select('tr.voted_row')

    """ Якщо голосів немає, то там таблиця із одним рядком, у якому один єдиний td"""
    if len(rows) == 1:
        td_count = len(rows[0].select('td'))
        if td_count == 1:
            return []

    return [{'name': r.select('td')[0].text, 'datetime': parse_datetime(r.select('td')[1].text)} for r in rows]


def get_votes_count(soup):
    return soup.select_one('.votes-count > strong:nth-child(2)').text


def parse_project_page(html):
    soup = BeautifulSoup(html, 'html5lib')
    votes = get_votes_table(soup)

    if len(votes) == 0:
        votes_count = 0
    else:
        votes_count = get_votes_count(soup)

    return {
        'votes_count': votes_count,
        'votes_table': votes
    }


def get_csrf_token(html):
    soup = BeautifulSoup(html, 'html5lib')

    return soup.find('meta', {'name': "csrf-token"})['content']


if __name__ == '__main__':
    content = _read_stub()
    print(parse_project_page(content))
