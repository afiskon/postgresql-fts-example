# postgresql-fts-example

Example of full text search in PostgreSQL: script for parsing Wikipedia dump.

How to use:

1. Download Wikipedia dump from [here][u1].
2. Unpack it: `bzip2 -d -k -v enwiki-20170401-pages-articles.xml.bz2`
3. Import data to PostgreSQL:


```bash
mkvirtualenv postgresql-fts
pip install -r requirements.txt
./parse.py enwiki-20170401-pages-articles.xml
```

[u1]: https://meta.wikimedia.org/wiki/Data_dump_torrents#enwiki
