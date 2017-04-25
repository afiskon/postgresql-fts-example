#!/usr/bin/env python3

import sys
import postgresql
from bs4 import BeautifulSoup

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <fname>")
    sys.exit(1)

fname = sys.argv[1]

processed_pages = 0
total_pages = 17_434_651
xml = ""
in_page = False

db = postgresql.open('pq://eax@localhost:5432/eax')

db.execute('create table if not exists ' +
  'articles(id serial primary key, title varchar(128), content text)');

#db.execute("create index if not exists idx_fts_articles on articles " +
#  "using gin((setweight(to_tsvector('english', title),'A') ||" +
#  "setweight(to_tsvector('english', content), 'B')))");

insert = db.prepare('insert into articles (title, content) values ($1, $2)');

def process_page(page_xml):
    global processed_pages, insert
    doc = BeautifulSoup(f"<page>{page_xml}</page>", 'xml')
    title = doc.page.title.string
    content = doc.page.revision.findAll('text')[0].string
    processed_pages += 1
    print(f"Processing page {processed_pages} of {total_pages} " +
          f"({processed_pages * 100 / total_pages}%) with title '{title}'")
    insert(title, content)

with open(fname) as f:
    for line in f:
       if line.strip() == '<page>':
           xml = ""
           in_page = True
           continue
       elif line.strip() == '</page>':
           process_page(xml)
           in_page = False

       if in_page:
           xml += line
