# showthedocs

showthedocs annotates code to show you the relevant pieces of its
documentation, read more [here](http://showthedocs.com/about).

## Requirements

You will need:

- [python3.13](https://www.python.org/downloads/)+
- [sass](https://sass-lang.com/install/#command-line) available in `$PATH`
- (optional) [direnv](https://direnv.net/)

## Running locally

    git clone https://github.com/idank/showthedocs.git
    cd showthedocs
    pip install -r requirements.txt
    ./getdocs clone
    python runserver.py

These commands will clone this repo, install the dependencies, download the
processed docs and run a local server.

## Fork Notes

The repository has been updated to work on a modern installation of python.

This is an experiment to see if [treesitter](https://tree-sitter.github.io/tree-sitter/) works well for this application.
