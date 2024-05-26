import unittest
from main import read_files_from_dir


class TestReadFilesFromDir(unittest.TestCase):
    def test_import_files(self):
        """Test Reading files from data01"""
        res = read_files_from_dir("test/data01")
        self.assertEqual(len(res), 2)
        self.assertFalse('' in res)

    def test_import_invalid_named_files(self):
        """Test Reading invalid name files from data02"""
        res = read_files_from_dir("test/data02")
        self.assertEqual(len(res), 0)

    def test_import_invalid_xml_files(self):
        """Test Reading invalid name files from data03"""
        res = read_files_from_dir("test/data03")
        self.assertEqual(len(res), 1)