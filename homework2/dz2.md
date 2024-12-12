# Домашняя работа номер 2

## Задание:
> Разработать инструмент командной строки для визуализации графа зависимостей, включая транзитивные зависимости. Сторонние средства для получения зависимостей использовать нельзя. 
> Зависимости определяются по имени пакета языка JavaScript (npm). Для описания графа зависимостей используется представление Mermaid. Визуализатор должен выводить результат в виде сообщения об успешном
> выполнении и сохранять граф в файле формата png. Конфигурационный файл имеет формат xml и содержит:
> • Путь к программе для визуализации графов.
> • Имя анализируемого пакета.
> • Путь к файлу с изображением графа зависимостей.
> • Максимальная глубина анализа зависимостей.
> • URL-адрес репозитория.
> Все функции визуализатора зависимостей должны быть покрыты тестами

## Выполнение:

Созданный нами config файл формата xml:
```
﻿<config>
		<visualizer_path>C:\Users\nickr\AppData\Roaming\npm\mmdc.cmd</visualizer_path>
		<package_name>express</package_name>
		<output_image_path>C:\Users\nickr\Pictures\graph.png</output_image_path>
		<max_depth>2</max_depth>
		<repo_url>https://registry.npmjs.org/</repo_url>
</config>
```

Основной код программы:
```
import os
import subprocess
import xml.etree.ElementTree as ET

def parse_config(config_path):
    tree = ET.parse(config_path)
    root = tree.getroot()
    
    config = {
        'visualizer_path': root.find('visualizer_path').text,
        'package_name': root.find('package_name').text,
        'output_image_path': root.find('output_image_path').text,
        'max_depth': int(root.find('max_depth').text),
        'repo_url': root.find('repo_url').text
    }
    
    return config

def get_dependencies(package_name, max_depth):
    dependencies = {}
    queue = [(package_name, 0)]
    
    while queue:
        current_package, depth = queue.pop(0)
        if depth > max_depth:
            continue
        
        cmd = f"npm view {current_package} dependencies --json"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Ошибка при выборке зависимостей для {current_package}: {result.stderr}")
            continue
        
        try:
            deps = result.stdout
            deps_json = eval(deps)
            dependencies[current_package] = deps_json
            
            for dep in deps_json.keys():
                queue.append((dep, depth + 1))
        except Exception as e:
            print(f"Ошибка при разборе зависимостей для {current_package}: {e}")
    
    return dependencies

def generate_mermaid_graph(dependencies):
    mermaid_graph = "graph TD;\n"
    
    for package, deps in dependencies.items():
        for dep in deps.keys():
            mermaid_graph += f"    {package} --> {dep};\n"
    
    return mermaid_graph

def save_mermaid_to_png(mermaid_code, visualizer_path, output_image_path):
    with open("temp_mermaid.mmd", "w") as f:
        f.write(mermaid_code)
    
    cmd = f"{visualizer_path} -i temp_mermaid.mmd -o {output_image_path}"
    subprocess.run(cmd, shell=True)
    
    os.remove("temp_mermaid.mmd")

def main(config_path):
    config = parse_config(config_path)
    
    dependencies = get_dependencies(config['package_name'], config['max_depth'])
    mermaid_graph = generate_mermaid_graph(dependencies)
    
    save_mermaid_to_png(mermaid_graph, config['visualizer_path'], config['output_image_path'])
    
    print(f"фото сохранено {config['output_image_path']}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        sys.exit(1)
    
    main(sys.argv[1])
```

Полученный граф: 
![image](https://github.com/user-attachments/assets/0f85344c-4d64-49f1-a5fb-22d693c03e85)

#Тесты:
```
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
```
