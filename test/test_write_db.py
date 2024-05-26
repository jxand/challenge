import unittest


class TestWriteDB(unittest.TestCase):

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

    def test_write_single(self):
        """Test writing single RO"""
        self.assertTrue(True)

    def test_write_multiple(self):
        """Test writing single RO"""
        self.assertTrue(True)
