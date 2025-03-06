import os
import logging
import markupsafe, markdown

from flask import render_template, request, redirect
from showdocs import app, html, annotate, structs, docs, errors, config

logger = logging.getLogger(__name__)

@app.context_processor
def sitename():
    '''Return the site name depending on the host.'''
    s = 'showthedocs'
    if 'explainsql' in request.host:
        s = 'explainsql'
    return {'sitename': s}

def _initplain():
    d = {}
    for name in ['about', 'contributing']:
        md = open(os.path.join(config.ROOT, name + '.md')).read()
        d[name] = markupsafe.Markup(markdown.markdown(md))
    return d
_plain = _initplain()

def _safedocs(docs):
    for path, externaldoc in docs.withcontents():
        yield path, markupsafe.Markup(externaldoc.contents)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    global _plain
    if config.TEST:
        _plain = _initplain()
    return render_template('plain.html',
                           title='about',
                           active_page='about',
                           contents=_plain['about'])

@app.route('/contribute')
def contribute():
    global _plain
    if config.TEST:
        _plain = _initplain()
    return render_template('contribute.html', contents=_plain['contributing'])

@app.route('/query')
def query():
    try:
        q = request.args.get('q', '')
        if not q:
            return redirect('/')

        lang = request.args.get('lang', '')
        if not lang:
            return redirect('/')

        annotated, docs = annotate.annotate(q, lang, True)

        return render_template('query.html',
                               lang=lang,
                               query=markupsafe.Markup(annotated),
                               docs=_safedocs(docs))
    except errors.NoAnnotatorFound as e:
        message = "lang '%s' isn't supported"
        return render_template('error.html',
                               title='oops',
                               message=message % e.args[0])
    except errors.NoDocsError:
        message = ('No docs added for this query. Consider '
                '<a href="/contribute">improving</a> the situation! :)')
        return render_template('queryerror.html',
                               renderlegend=False,
                               lang=lang,
                               query=q,
                               message=markupsafe.Markup(message))
    except errors.ParsingError as e:
        wrappedquery, wrappedmessage = html.formaterror(q, e)
        wrappedmessage = '<span>parsing error</span> ' + wrappedmessage
        return render_template('queryerror.html',
                               lang=lang,
                               query=markupsafe.Markup(wrappedquery),
                               message=markupsafe.Markup(wrappedmessage))
    except:
        if config.TEST:
            raise
        logger.error('uncaught exception: lang=%r query=%r',
                     lang,
                     q,
                     exc_info=True)
        message = 'something went wrong... this was logged and will be checked'
        return render_template('error.html', title='oops', message=message)
