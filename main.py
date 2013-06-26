#!/data/project/commonsinterwiki/python/bin/python
from __future__ import unicode_literals
"""
Copyright (C) 2013 Legoktm

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
"""

from flask import Flask, request
import bootstrap
import pywikibot
from wsgiref.handlers import CGIHandler
from werkzeug.debug import DebuggedApplication

app = Flask(__name__)


def form():
    """Why is this a function???"""
    return """ <form class="form-signin" action="/commonsinterwiki/cgi-bin/main.py/" method="get">
<h2 class="form-signin-heading">Please enter an id.</h2>
<input type="text" class="input-block-level" name="id" placeholder="Q##">
<!--<input type="text" class="input-block-level" name="site" placeholder="en">-->
<button class="btn btn-large btn-primary" type="submit">Check</button>
</form>"""


@app.route('/')
def main():
    qid = request.args.get('id', '')
    if not qid:
        return bootstrap.main(tool='copypaste.py', stuff=form(), title='CommonsInterwiki')
    site = pywikibot.Site('wikidata', 'wikidata').data_repository()
    item = pywikibot.ItemPage(site, qid)
    item.get('sitelinks')  # Does this even work? Oh well.
    dbnames = sorted(list(item.sitelinks))
    links = list()
    for site in dbnames:
        lang = site.replace('wiki','').replace('_','-')
        link = item.sitelinks[site]
        links.append('[[{0}:{1}]]'.format(lang, link))
    text = '\n'.join(links)
    text = '<textarea rows="30" cols="100">'+text+'</textarea>'
    return bootstrap.main(tool='copypaste.py', stuff=text, title='CommonsInterwiki')

CGIHandler().run(DebuggedApplication(app))
