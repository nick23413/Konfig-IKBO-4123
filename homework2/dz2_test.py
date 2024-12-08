import unittest
import os
import subprocess
import xml.etree.ElementTree as ET
from unittest.mock import patch, MagicMock

# Импортируем функции из вашего скрипта
from dz2 import parse_config, get_dependencies, generate_mermaid_graph, save_mermaid_to_png

class TestVisualizeDeps(unittest.TestCase):

    def test_parse_config(self):
        config_xml = """
        <config>
            <visualizer_path>/path/to/mermaid-cli/mmdc</visualizer_path>
            <package_name>express</package_name>
            <output_image_path>/path/to/output.png</output_image_path>
            <max_depth>2</max_depth>
            <repo_url>https://registry.npmjs.org/</repo_url>
        </config>
        """
        with open("test_config.xml", "w") as f:
            f.write(config_xml)
        
        config = parse_config("test_config.xml")
        self.assertEqual(config['visualizer_path'], '/path/to/mermaid-cli/mmdc')
        self.assertEqual(config['package_name'], 'express')
        self.assertEqual(config['output_image_path'], '/path/to/output.png')
        self.assertEqual(config['max_depth'], 2)
        self.assertEqual(config['repo_url'], 'https://registry.npmjs.org/')
        
        os.remove("test_config.xml")

    

    def test_generate_mermaid_graph(self):
        dependencies = {
            'express': {'dep1': {}, 'dep2': {}}
        }
        mermaid_graph = generate_mermaid_graph(dependencies)
        expected_graph = "graph TD;\n    express --> dep1;\n    express --> dep2;\n"
        self.assertEqual(mermaid_graph, expected_graph)

    @patch('subprocess.run')
    def test_save_mermaid_to_png(self, mock_run):
        mermaid_code = "graph TD;\n    express --> dep1;\n    express --> dep2;\n"
        visualizer_path = '/path/to/mermaid-cli/mmdc'
        output_image_path = '/path/to/output.png'
        
        save_mermaid_to_png(mermaid_code, visualizer_path, output_image_path)
        
        mock_run.assert_called_once_with(f"{visualizer_path} -i temp_mermaid.mmd -o {output_image_path}", shell=True)
        self.assertFalse(os.path.exists("temp_mermaid.mmd"))

if __name__ == '__main__':
    unittest.main()
