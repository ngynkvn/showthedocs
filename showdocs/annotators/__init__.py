from showdocs import errors

from . import sql, nginx, gitconfig

_all = [sql.SqlAnnotator, nginx.NginxAnnotator, gitconfig.GitConfigAnnotator]
_annotators = {}

for a in _all:
    for alias in a.alias:
        if alias in _annotators:
            raise ValueError('annotator %s alias %r collides with %s' %
                             (a.__name__, alias, _annotators[alias].__name__))
        _annotators[alias] = a

def get(lang):
    acls = _annotators.get(lang, None)
    if not acls:
        raise errors.NoAnnotatorFound(lang)

    return acls(lang)
