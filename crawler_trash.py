#!/usr/bin/env python3
import codecs
import datetime
import logging
import re
import sys
from io import StringIO
from time import sleep

import requests
from ics import Calendar
from lxml import etree

from dto.dto import ParseResponse, Event

logging.basicConfig(level=logging.DEBUG)


def crawl_page(page: int = 0) -> str:
    url = f'https://www.zistersdorf.gv.at/system/web/kalender.aspx?page={page}'
    res = requests.get(url=url)
    if res.status_code != 200:
        logging.error(f'Failed to crawl page {page}: status code is not 200 (OK)')
        sys.exit(4)
    logging.debug(f'successfully crawled page {page}')
    return res.content.decode("utf-8")


# parse page and return max number of pages
def parse_page(html: str, pages: int | None) -> ParseResponse:
    tree = etree.parse(StringIO(html), parser=etree.HTMLParser())
    size = tree.xpath('//a[@title="Letzte Seite"]')
    response = ParseResponse()
    if pages is None:
        if not size:
            logging.error(f'Failed to find last element!')
            sys.exit(1)
        match = re.search('page=([0-9]+)', size[0].get('href', ''))
        if not match.group(1):
            logging.error(f'Failed to find last page number from: {match}')
            sys.exit(2)
        response.pages = int(match.group(1))
        logging.info(f'Found {response.pages} pages to crawl')
    else:
        response.pages = pages
    response.events = []
    dates: list[datetime] = [parse_date(date.text) for date in tree.xpath('//tr//td[position()=1]')]
    titles: list[str] = [title.text for title in tree.xpath('//tr//td[position()=2]//a')]
    calendar_types: list[str] = [calendar_type.text for calendar_type in tree.xpath('//tr//td[position()=3]//span')]
    for i in range(len(dates)):
        event = Event(name=f'{titles[i]} ({calendar_types[i]})', location=calendar_types[i], begin=dates[i],
                      created=datetime.datetime.now())
        event.make_all_day()
        response.events.append(event)
    logging.debug(f'found {len(dates)} events')
    return response


def parse_date(text: str) -> datetime:
    match = re.search('([0-9]{2}\.[0-9]{2}\.[0-9]{4})', text)
    if not match.group(1):
        logging.error(f'Failed to find date from: {text}')
        sys.exit(3)
    return datetime.datetime.strptime(match.group(1), '%d.%m.%Y')


if __name__ == '__main__':
    calendar_all = Calendar()
    calendars = []
    filters = ['Stadt 1', 'Stadt 2', 'Ort 1', 'Ort 2', 'Mutterberatung', 'Stillgruppe']
    for filter in filters:
        calendar = Calendar(creator=filter)
        calendars.append(calendar)
    # page 0
    res = parse_page(crawl_page(0), None)
    for event in res.events:
        calendar_all.events.add(event)
        for calendar in calendars:
            # add special calendar
            if calendar.creator in event.location:
                calendar.events.add(event)
    # pages 1..n
    for page in range(1, res.pages + 1):
        logging.debug(f'sleep for 3s...')
        sleep(3)
        res = parse_page(crawl_page(page), res.pages)
        for event in res.events:
            calendar_all.events.add(event)
            for calendar in calendars:
                # add special calendar
                if calendar.creator in event.location:
                    calendar.events.add(event)
    with codecs.open('zistersdorf.ics', 'w', 'utf-8') as f:
        f.writelines(calendar_all.serialize_iter())
    for calendar in calendars:
        with codecs.open(f'zistersdorf_{calendar.creator.lower().replace(" ", "_")}.ics', 'w', 'utf-8') as f:
            f.writelines(calendar.serialize_iter())
