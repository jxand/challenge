import unittest
from main import parse_xml
from main import window_by_datetime


class TestWindowByDatetime(unittest.TestCase):

    test_data_01 = '''
    <event>
        <order_id>101</order_id>
        <date_time>2023-08-10T10:00:00</date_time>
        <status>In Progress</status>
        <cost>50.25</cost>
        <repair_details>
            <technician>Jane Smith</technician>
            <repair_parts>
                <part name="Air Filter" quantity="1"/>
                <part name="Air Filter2" quantity="2"/>
            </repair_parts>
        </repair_details>
        <file_name>test01.txt</file_name>
    </event>
    '''

    test_data_02 = '''
    <event>
        <order_id>101</order_id>
        <date_time>2023-08-10T10:00:00</date_time>
        <status>In Progress</status>
        <cost>50.25</cost>
        <repair_details>
            <technician>Jane Smith</technician>
            <repair_parts>
                <part name="Air Filter" quantity="1"/>
                <part name="Air Filter2" quantity="2"/>
                <part name="Air Filter3" quantity="3"/>
            </repair_parts>
        </repair_details>
        <file_name>test02.txt</file_name>
    </event>
    '''

    def test(self):
        """test"""
        df = parse_xml([self.test_data_01, self.test_data_02])
        d = window_by_datetime(df, '1D')
        self.assertEqual(len(d.keys()), 1)
        self.assertEqual(list(d.keys()), ['2023-08-10 00:00:00'])

    # need to define more unit tests for the helper functions in util.py