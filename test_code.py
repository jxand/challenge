import unittest


# File exists to aid in testing in IDE.
# From the command line you can simply call python -m unittest
# Note: this files is not called "test.py" because I'm using a "test" directory, it's not
# recommend to use both.
loader = unittest.TestLoader()
test_dir = loader.discover("test")

runner = unittest.TextTestRunner()
runner.run(test_dir)