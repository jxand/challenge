import unittest
from main import parse_xml


class TestParseXML(unittest.TestCase):

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

    def test_parse_single(self):
        """Test parsing single file"""
        res = parse_xml([self.test_data_01])
        self.assertEqual(len(res), 2)  # each part should have it's own line
        self.assertEqual(list(res["part_row"]), [0,1])
        self.assertEqual(list(res["file_name"]), ["test01.txt"] * 2)

    def test_parse_multiple(self):
        """Test parsing multiple file"""
        contents = [self.test_data_01, self.test_data_02]
        res = parse_xml(contents)
        self.assertEqual(len(res), 5)  # each part should have it's own line
