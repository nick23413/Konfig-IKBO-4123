import unittest
from dz3 import ConfigParser

class TestConfigParser(unittest.TestCase):

    def test_parse_constants(self):
        xml_content = '''
        <config>
            <constant name="server_name">
                <number>webserver</number>
            </constant>
            <constant name="port">
                <number>8080</number>
            </constant>
            <constant name="version">
                <number>1.0</number>
            </constant>
        </config>
        '''
        parser = ConfigParser()
        config = parser.parse_xml(xml_content)
        expected_config = {
            'server_name': 'webserver',
            'port': '8080',
            'version': '1.0'
        }
        self.assertEqual(config, expected_config)

    def test_parse_dict(self):
        xml_content = '''
        <config>
            <dict key="server_config">
                <number key="name">${server_name}</number>
                <number key="port">${port}</number>
                <number key="version">${version}</number>
            </dict>
        </config>
        '''
        parser = ConfigParser()
        parser.constants = {
            'server_name': 'webserver',
            'port': '8080',
            'version': '1.0'
        }
        config = parser.parse_xml(xml_content)
        expected_config = {
            'server_config': '([ name : webserver, port : 8080, version : 1.0 ])'
        }
        self.assertEqual(config, expected_config)

    def test_parse_array(self):
        xml_content = '''
        <config>
            <array>
                <number>1</number>
                <number>2</number>
                <number>3</number>
            </array>
        </config>
        '''
        parser = ConfigParser()
        config = parser.parse_xml(xml_content)
        expected_config = {
            'array': '#( 1, 2, 3 )'
        }
        self.assertEqual(config, expected_config)

    def test_parse_nested_dict(self):
        xml_content = '''
        <config>
            <dict key="nested_dict">
                <dict key="inner_dict">
                    <number key="inner_key">inner_value2</number>
                </dict>
            </dict>
        </config>
        '''
        parser = ConfigParser()
        config = parser.parse_xml(xml_content)
        expected_config = {
            'nested_dict': '([ inner_key : inner_value2 ])'
        }
        self.assertEqual(config, expected_config)

    def test_parse_comments(self):
        xml_content = '''
        <!-- Это однострочный комментарий -->
        <config>
            <constant name="server_name">
                <number>webserver</number>
            </constant>
        </config>
        '''
        parser = ConfigParser()
        config = parser.parse_xml(xml_content)
        expected_config = {
            'server_name': 'webserver'
        }
        self.assertEqual(config, expected_config)
        self.assertEqual(parser.comments, ['* Это однострочный комментарий'])

    def test_format_config(self):
        config = {
            'server_name': 'webserver',
            'port': '8080',
            'version': '1.0',
            'server_config': '([ name : webserver, port : 8080, version : 1.0 ])',
            'array': '#( 1, 2, 3 )',
            'nested_dict': '([ inner_key : inner_value2 ])'
        }
        parser = ConfigParser()
        parser.comments = ['* Это однострочный комментарий']
        formatted_config = parser.format_config(config)
        expected_formatted_config = '''* Это однострочный комментарий
var server_name webserver
var port 8080
var version 1.0
([
    name : webserver,
    port : 8080,
    version : 1.0
])
([
    inner_key : inner_value2
])
#( 1, 2, 3 )'''
        self.assertEqual(formatted_config, expected_formatted_config)

if __name__ == '__main__':
    unittest.main()
