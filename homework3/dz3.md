# Домашняя работа номер 3
Url на мой репозиторий с дз: https://github.com/nick23413/Konfig-IKBO-4123/tree/main/homework3
## Задание:
> Разработать инструмент командной строки для учебного конфигурационного языка, синтаксис которого приведен далее. Этот инструмент преобразует текст из входного формата в выходной. Синтаксические ошибки выявляются с выдачей
> сообщений. Входной текст на языке xml принимается из файла, путь к которому задан ключом командной строки. Выходной текст на учебном конфигурационном языке попадает в файл, путь к которому задан ключом командной строки.
> Однострочные комментарии:
> * Это однострочный комментарий
> Массивы:
> #( значение, значение, значение, ... )
> Словари:
> ([
>  имя : значение,
>  имя : значение,
>  имя : значение,
>  ...
> ])
> Имена:
> [_a-zA-Z][_a-zA-Z0-9]*
> Значения:
> • Числа.
> • Массивы.
> • Словари.
> Объявление константы на этапе трансляции:
> var имя значение
> Вычисление константы на этапе трансляции:
> ${имя}
> Результатом вычисления константного выражения является значение. Все конструкции учебного конфигурационного языка (с учетом их возможной вложенности) должны быть покрыты тестами. Необходимо показать 3
> примера описания конфигураций из разных предметных областей.

# Выполнение:

Входной файл формата xml:
```
﻿<config>
		<!-- Это однострочный комментарий -->
		<constant name="server_name">
				<number>webserver</number>
		</constant>
		<constant name="port">
				<number>8080</number>
		</constant>
		<constant name="version">
				<number>1.0</number>
		</constant>
		<dict key="server_config">
				<number key="name">${server_name}</number>
				<number key="port">${port}</number>
				<number key="version">${version}</number>
		</dict>
		<array>
				<number>1</number>
				<number>2</number>
				<number>3</number>
		</array>
		<dict key="nested_dict">
				<dict key="inner_dict">
						<number key="inner_key">inner_value</number>
				</dict>
		</dict>
</config>
```

Парсер:
```
import re

class ConfigParser:
    def __init__(self):
        self.constants = {}
        self.comments = []

    def parse_value(self, value):
        if isinstance(value, dict):
            if 'array' in value:
                return self.parse_array(value['array'])
            elif 'dict' in value:
                return self.parse_dict(value['dict'])
            elif 'number' in value:
                return self.parse_number(value['number'])
            elif 'constant' in value:
                return self.parse_constant(value['constant'])
        return value.strip() if value else ''

    def parse_array(self, array):
        return '#( ' + ', '.join(self.parse_value(child) for child in array) + ' )'

    def parse_dict(self, dictionary, indent=0):
        items = []
        for key, value in dictionary.items():
            items.append(f'{"    " * (indent + 1)}{key} : {self.parse_value(value)}')
        return '([' + '\n' + ',\n'.join(items) + '\n' + '    ' * indent + '])'

    def parse_number(self, number):
        return number.strip()

    def parse_constant(self, constant):
        name = constant['name']
        value = self.parse_value(constant['value'])
        self.constants[name] = value
        return f'var {name} {value}'

    def parse_xml(self, xml_content):
        # Извлечение комментариев
        comment_pattern = re.compile(r'<!--\s*(.*?)\s*-->', re.DOTALL)
        for match in comment_pattern.finditer(xml_content):
            comment = match.group(1)
            self.comments.append(f'* {comment}')

        # Извлечение констант
        constant_pattern = re.compile(r'<constant name="(\w+)">\s*<number>(.*?)</number>\s*</constant>', re.DOTALL)
        for match in constant_pattern.finditer(xml_content):
            name = match.group(1)
            value = match.group(2)
            self.constants[name] = value

        # Создаем результирующий конфиг и добавляем константы
        config = {}
        for name, value in self.constants.items():
            config[name] = value

        # Извлечение словаря
        dict_pattern = re.compile(r'<dict key="(\w+)">\s*(.*?)\s*</dict>', re.DOTALL)
        for match in dict_pattern.finditer(xml_content):
            key = match.group(1)
            value = match.group(2)
            config[key] = self.parse_value({'dict': self.parse_dict_content(value)})

        # Извлечение массива
        array_pattern = re.compile(r'<array>\s*(.*?)\s*</array>', re.DOTALL)
        for match in array_pattern.finditer(xml_content):
            value = match.group(1)
            config['array'] = self.parse_value({'array': self.parse_array_content(value)})

        return config

    def parse_dict_content(self, content):
        dict_items = {}
        item_pattern = re.compile(r'<number key="(\w+)">(.*?)</number>', re.DOTALL)
        for match in item_pattern.finditer(content):
            key = match.group(1)
            value = match.group(2)
            dict_items[key] = self.resolve_constants(value)
        return dict_items

    def parse_array_content(self, content):
        array_items = []
        item_pattern = re.compile(r'<number>(.*?)</number>', re.DOTALL)
        for match in item_pattern.finditer(content):
            value = match.group(1)
            array_items.append(self.resolve_constants(value))
        return array_items

    def resolve_constants(self, value):
        def replace_constant(match):
            name = match.group(1)
            return self.constants.get(name, match.group(0))

        return re.sub(r'\$\{(\w+)\}', replace_constant, value)

    def format_config(self, config):
        formatted_config = self.comments.copy()
        for key, value in config.items():
            if key in self.constants:
                formatted_config.append(f'var {key} {value}')
            else:
                formatted_config.append(f'{value}')
        return '\n'.join(formatted_config)

    def parse_file(self, input_file, output_file):
        try:
            with open(input_file, 'r', encoding='utf-8') as file:
                xml_content = file.read()
        except Exception as e:
            print(f"Error reading input file: {e}")
            return

        config = self.parse_xml(xml_content)
        if config is None:
            return

        formatted_config = self.format_config(config)

        try:
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(formatted_config)
        except Exception as e:
            print(f"Error writing output file: {e}")
```

Основной код программы:
```
import argparse
from dz3 import ConfigParser

def main():
    parser = argparse.ArgumentParser(description='Convert XML to custom configuration language.')
    parser.add_argument('input_file', type=str, help='Path to the input XML file')
    parser.add_argument('output_file', type=str, help='Path to the output configuration file')

    args = parser.parse_args()

    config_parser = ConfigParser()
    config_parser.parse_file(args.input_file, args.output_file)

if __name__ == '__main__':
    main()
```

Выходной файл формата cfg:
```
* Это однострочный комментарий
var server_name webserver
var port 8080
var version 1.0
([
    name : webserver,
    port : 8080,
    version : 1.0
])
([
    inner_key : inner_value
])
#( 1, 2, 3 )
```

## Тесты
```
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
```
