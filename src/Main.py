#!/usr/bin/env python
""" 
This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.
This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "Faria Afrin Haque"
__contact__ = "st169393@stud-uni.stuttgart.de"
__copyright__ = "Copyright 2022, Uni Stuttgart"
__date__ = "2022/02/25"
__deprecated__ = False
__email__ =  "st169393@stud-uni.stuttgart.de"
__license__ = "GPLv3"
__maintainer__ = "developer"
__status__ = "Production"
__version__ = "0.0.1"


from xml.dom import minidom

import mysql.connector
from pybtex.database.input import bibtex

#open a bibtex file
parser = bibtex.Parser()
bibdata = parser.parse_file("../data/abstracts.bib")

###########################################################
#                     convert into XML                    #
###########################################################

# Create Document for XML
doc = minidom.Document()
root = doc.createElement('Bibliography')
doc.appendChild(root)

# for holding the values for table in sql database
val = []
# id for sql table primary key
id = 0

#loop through the individual references
for bib_id in bibdata.entries:
    b = bibdata.entries[bib_id].fields

    # create xml nodes
    citation = doc.createElement('citation')
    citation.setAttribute('id', bib_id)

    if not 'title' in b.keys():
        b["title"] = ''
    titlenode = doc.createElement('title')
    title = doc.createTextNode(b["title"])
    titlenode.appendChild(title)
    citation.appendChild(titlenode)

    if not 'booktitle' in b.keys():
        b["booktitle"] = ''
    booktitlenode = doc.createElement('booktitle')
    booktitle = doc.createTextNode(b["booktitle"])
    booktitlenode.appendChild(booktitle)
    citation.appendChild(booktitlenode)

    if not 'month' in b.keys():
        b["month"] = ''
    monthnode = doc.createElement('month')
    month = doc.createTextNode(b["month"])
    monthnode.appendChild(month)
    citation.appendChild(monthnode)

    if not 'year' in b.keys():
        b["year"] = ''
    yearnode = doc.createElement('year')
    year = doc.createTextNode(b["year"])
    yearnode.appendChild(year)
    citation.appendChild(yearnode)

    if not 'address' in b.keys():
        b["address"] = ''
    addressnode = doc.createElement('address')
    address = doc.createTextNode(b["address"])
    addressnode.appendChild(address)
    citation.appendChild(addressnode)

    if not 'publisher' in b.keys():
        b["publisher"] = ''
    publishernode = doc.createElement('publisher')
    publisher = doc.createTextNode(b["publisher"])
    publishernode.appendChild(publisher)
    citation.appendChild(publishernode)

    if not 'url' in b.keys():
        b["url"] = ''
    urlnode = doc.createElement('url')
    url = doc.createTextNode(b["url"])
    urlnode.appendChild(url)
    citation.appendChild(urlnode)

    if not 'doi' in b.keys():
        b["doi"] = ''
    doinode = doc.createElement('doi')
    doi = doc.createTextNode(b["doi"])
    doinode.appendChild(doi)
    citation.appendChild(doinode)

    if not 'pages' in b.keys():
        b["pages"] = ''
    pagesnode = doc.createElement('pages')
    pages = doc.createTextNode(b["pages"])
    pagesnode.appendChild(pages)
    citation.appendChild(pagesnode)

    if not 'abstract' in b.keys():
        b["abstract"] = ''
    abstractnode = doc.createElement('abstract')
    abstract = doc.createTextNode(b["abstract"])
    abstractnode.appendChild(abstract)
    citation.appendChild(abstractnode)

    if 'editor' in bibdata.entries[bib_id].persons.keys():
        editors = doc.createElement('editors')
        for e in bibdata.entries[bib_id].persons["editor"]:
            editor = doc.createElement('editor')
            efs = ''
            for ef in e.first():
                efs += ef + ' '
            els = ''
            for el in e.last():
                els += el + ' '
            editor.setAttribute('firstname', efs[:-1])
            editor.setAttribute('lastname', els[:-1])
            editors.appendChild(editor)
        citation.appendChild(editors)

    if 'author' in bibdata.entries[bib_id].persons.keys():
        authors = doc.createElement('authors')
        for a in bibdata.entries[bib_id].persons["author"]:
            author = doc.createElement('author')
            afs = ''
            for af in a.first():
                afs += af + ' '
            als = ''
            for al in a.last():
                als += al + ' '
            author.setAttribute('firstname', afs[:-1])
            author.setAttribute('lastname', als[:-1])
            authors.appendChild(author)
        citation.appendChild(authors)
    root.appendChild(citation)

    # append a citation into val
    val.append(tuple((id, bib_id, b["title"], b["booktitle"], b["month"], b["year"], b["address"], b["publisher"], b["url"], b["doi"], b["pages"], b["abstract"],  "",  "")))

xml_str = doc.toprettyxml(indent="\t")
# write into xml file
with open("../result/citation.xml", "w", encoding="utf-8") as f:
    f.write(xml_str)

print("written into citation.xml")

###########################################################
#                     insert into Database               #
###########################################################

# MySQL connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="testDB"
)
# insert into Bibliography Table
mycursor = mydb.cursor()

# increase packet size
mycursor.execute('set global max_allowed_packet=1048576000')

# drop table if exists
dropsql = 'DROP TABLE IF EXISTS Bibliography;'
mycursor.execute(dropsql)

# create new table
createsql = 'CREATE TABLE Bibliography ( id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, ' \
            'bib_id VARCHAR(255) NOT NULL, title TEXT NOT NULL, booktitle TEXT, ' \
            'month VARCHAR(50), year VARCHAR(50), address VARCHAR(255), ' \
            'publisher TEXT, url TEXT, doi VARCHAR(255), pages VARCHAR(50), ' \
            'abstract TEXT, author TEXT, editor TEXT, ' \
            'FULLTEXT (title, abstract)) ENGINE=InnoDB;'
mycursor.execute(createsql)

# inseart data into table
insertsql = 'INSERT INTO Bibliography (id, bib_id, title, booktitle, month, year, ' \
             'address, publisher, url, doi, pages, abstract, author, editor) ' \
             'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
mycursor.executemany(insertsql, val)

mydb.commit()

print(mycursor.rowcount, "was inserted.")