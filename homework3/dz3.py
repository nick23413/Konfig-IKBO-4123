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
