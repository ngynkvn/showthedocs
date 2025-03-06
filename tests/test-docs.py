import unittest, os

from showdocs import docs

class TestDocs(unittest.TestCase):
    def test_loadall(self):
        d = docs.loadall()
        self.assertTrue('postgres/sql-select.html' in list(d.keys()))

    def test_badroot(self):
        self.assertRaises(RuntimeError, docs.loadall, os.path.dirname(__file__))

    def test_collection(self):
        path = 'postgres/sql-select.html'

        c = docs.Collection()
        self.assertEqual(len(c), 0)
        self.assertEqual(list(c), [])
        self.assertEqual(list(c.withcontents()), [])

        c.add(path)
        self.assertEqual(len(c), 1)
        self.assertEqual(list(c), [path])
        gotpath, externaldoc = list(c.withcontents())[0]
        self.assertEqual(path, gotpath)
        self.assertTrue(externaldoc.contents > 0)

        c.add(path)
        self.assertEqual(len(c), 1)

        self.assertRaises(ValueError, c.add, 'what')

        c.discard(path)
        self.assertEqual(len(c), 0)
