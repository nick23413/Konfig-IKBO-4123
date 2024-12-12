# Домашняя работа номер 1
Url на мой репозиторий с дз: https://github.com/nick23413/Konfig-IKBO-4123/tree/main/homework1
## Задание:
> Разработать эмулятор для языка оболочки ОС. Необходимо сделать работу эмулятора как можно более похожей на сеанс shell в UNIX-подобной ОС. Эмулятор должен запускаться из реальной командной строки, а файл с
> виртуальной файловой системой не нужно распаковывать у пользователя. Эмулятор принимает образ виртуальной файловой системы в виде файла формата tar. Эмулятор должен работать в режиме CLI. Ключами командной строки задаются:
> • Путь к архиву виртуальной файловой системы.
> • Путь к лог-файлу.
> Лог-файл имеет формат csv и содержит все действия во время последнего сеанса работы с эмулятором. Необходимо поддержать в эмуляторе команды ls, cd и exit, а также следующие команды:
> 1. tail.
> 2. du.
> Все функции эмулятора должны быть покрыты тестами, а для каждой из поддерживаемых команд необходимо написать 3 теста.

## Выполнение:

Созданная нами виртуальная система: https://disk.yandex.ru/d/n84hbmhy-FaocA

Лог файл: https://github.com/nick23413/Konfig-IKBO-4123/blob/main/homework1/syslog.csv

Основной код программы:

```
import argparse #обработка аргументов командной строки
import tarfile
import csv
from datetime import datetime
import shlex #Модуль для разделения строки на токены, аналогично командной строке

class VFS:
    def __init__(self, tar_path):
        self.root = {}
        self.current_dir = self.root
        self.load_tar(tar_path)
        #грузим архив
    def load_tar(self, tar_path):
        with tarfile.open(tar_path, 'r') as tar:
            for member in tar.getmembers():
                path = member.name.replace('\\', '/').lstrip('/')
                parts = path.split('/')
                node = self.root
                for part in parts[:-1]:
                    if part not in node:
                        node[part] = {}
                    node = node[part]
                filename = parts[-1]
                if member.isfile():
                    content = tar.extractfile(member).read().decode('utf-8', errors='ignore')
                    node[filename] = {'type': 'file', 'content': content, 'size': member.size}
                elif member.isdir():
                    node[filename] = {}
            #открытие архива и создание структуры данных
    def exists(self, path):
        parts = path.strip('/').split('/')
        node = self.root
        for part in parts:
            if part in node:
                node = node[part]
            else:
                return False
        return True
        #проверка и разбивка на части
    def get_dir_contents(self, path):
        parts = path.strip('/').split('/')
        node = self.root
        for part in parts:
            if part in node:
                node = node[part]
            else:
                return None
        return node
        #получение директории или none, если нет сущ пути
    def get_file_content(self, path):
        parts = path.strip('/').split('/')
        node = self.root
        for part in parts:
            if part in node:
                node = node[part]
            else:
                return None
        if isinstance(node, dict) and node.get('type') == 'file':
            return node.get('content')
        else:
            return None
        #аналогично, но тут путь не ведет к файлу
    def get_file_size(self, path):
        parts = path.strip('/').split('/')
        node = self.root
        for part in parts:
            if part in node:
                node = node[part]
            else:
                return None
        if isinstance(node, dict) and node.get('type') == 'file':
            return node.get('size')
        else:
            return None
        #получение размера
    def change_dir(self, path):
        if path == '/':
            self.current_dir = self.root
            return '/'
        parts = path.strip('/').split('/')
        new_dir = self.root
        for part in parts:
            if part in new_dir:
                new_dir = new_dir[part]
            else:
                return None
        self.current_dir = new_dir
        return '/' + '/'.join(parts)
        
    def get_total_size(self, path):
        parts = path.strip('/').split('/')
        node = self.root
        for part in parts:
            if part in node:
                node = node[part]
            else:
                return None
        if isinstance(node, dict) and not node.get('type'):
            total = 0
            for item in node.values():
                if item.get('type') == 'file':
                    total += item['size']
                elif isinstance(item, dict):
                    sub_size = self.get_total_size('/'.join(parts + [item]))
                    if sub_size is not None:
                        total += sub_size
            return total
        elif isinstance(node, dict) and node.get('type') == 'file':
            return node['size']
        else:
            return None
    #общ размер
class Logger:
    def __init__(self, log_path):
        self.log_file = open(log_path, mode='w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.log_file)
        self.writer.writerow(['timestamp', 'command_line', 'success', 'error_message'])
    
    def log_action(self, command_line, success, error_message=''):
        timestamp = datetime.now().isoformat()
        self.writer.writerow([timestamp, command_line, success, error_message])
    
    def close(self):
        self.log_file.close()

def main(tar_path, log_path):
    vfs = VFS(tar_path)
    logger = Logger(log_path)
    cwd = '/'
    prompt = f'[{cwd}]$ '
    
    while True:
        try:
            user_input = input(prompt)
            if not user_input.strip():
                continue
            parts = shlex.split(user_input)
            command = parts[0]
            args = parts[1:]
            
            if command == 'ls':
                if not args:
                    contents = vfs.get_dir_contents(cwd)
                    if contents:
                        print('\n'.join(contents.keys()))
                    else:
                        print(f"bash: ls: {cwd}: No such file or directory")
                        logger.log_action(user_input, False, "Directory not found")
                else:
                    target = args[0]
                    if target.startswith('/'):
                        path = target
                    else:
                        path = cwd + '/' + target
                    path = path.replace('//', '/')
                    contents = vfs.get_dir_contents(path)
                    if contents:
                        print('\n'.join(contents.keys()))
                    else:
                        print(f"bash: ls: {target}: No such file or directory")
                        logger.log_action(user_input, False, "Directory not found")
            elif command == 'cd':
                if len(args) != 1:
                    print("bash: cd: too many arguments")
                    logger.log_action(user_input, False, "Too many arguments")
                    continue
                target = args[0]
                if target == '-':
                    # Support for previous directory is not implemented
                    print("bash: cd: -: No such file or directory")
                    logger.log_action(user_input, False, "Directory not found")
                    continue
                new_cwd = vfs.change_dir(target)
                if new_cwd:
                    cwd = new_cwd
                    prompt = f'[{cwd}]$ '
                else:
                    print(f"bash: cd: {target}: No such file or directory")
                    logger.log_action(user_input, False, "Directory not found")
            elif command == 'tail':
                if len(args) != 1:
                    print("bash: tail: filename argument required")
                    logger.log_action(user_input, False, "Filename argument required")
                    continue
                filename = args[0]
                if filename.startswith('/'):
                    path = filename
                else:
                    path = cwd + '/' + filename
                    path = path.replace('//', '/')
                content = vfs.get_file_content(path)
                if content:
                    lines = content.split('\n')
                    print('\n'.join(lines[-10:]))
                else:
                    print(f"bash: tail: {filename}: No such file")
                    logger.log_action(user_input, False, "File not found")
            elif command == 'du':
                if len(args) != 1:
                    print("bash: du: filename argument required")
                    logger.log_action(user_input, False, "Filename argument required")
                    continue
                target = args[0]
                if target.startswith('/'):
                    path = target
                else:
                    path = cwd + '/' + target
                    path = path.replace('//', '/')
                size = vfs.get_total_size(path)
                if size is not None:
                    print(f"{size}\t{target}")
                else:
                    print(f"bash: du: {target}: No such file or directory")
                    logger.log_action(user_input, False, "File or directory not found")
            elif command == 'exit':
                logger.close()
                break
            else:
                print(f"bash: {command}: command not found")
                logger.log_action(user_input, False, "Command not found")
            logger.log_action(user_input, True)
        except Exception as e:
            print(f"An error occurred: {e}")
            logger.log_action(user_input, False, str(e))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='VFS Emulator')
    parser.add_argument('tar_path', help='Path to the tar archive')
    parser.add_argument('log_path', help='Path to the log file')
    args = parser.parse_args()
    main(args.tar_path, args.log_path)
```

## Тесты для кода:

```
import unittest
import tempfile
import tarfile
import os
from dz1 import VFS

class TestCommands(unittest.TestCase):
    def setUp(self):
        self.tar_fd, self.tar_path = tempfile.mkstemp(suffix='.tar')
        os.close(self.tar_fd)
        
        with tarfile.open(self.tar_path, 'w') as tar:
            tar.addfile(tarfile.TarInfo(name='etc/'))
            tar.addfile(tarfile.TarInfo(name='etc/hosts'), fileobj=None)
            tar.addfile(tarfile.TarInfo(name='etc/passwd'), fileobj=None)
            tar.addfile(tarfile.TarInfo(name='test.txt'), fileobj=None)
        
        self.vfs = VFS(self.tar_path)
    
    def test_ls_root(self):
        contents = self.vfs.get_dir_contents('etc')
        self.assertIsNotNone(contents)
        self.assertIn('hosts', contents)
        self.assertIn('passwd', contents)
    
    def test_cd_subdirectory(self):
        cwd = self.vfs.change_dir('etc')
        self.assertEqual(cwd, '/etc')
        contents = self.vfs.get_dir_contents('/etc')
        self.assertIn('hosts', contents)
        self.assertIn('passwd', contents)
    
    def test_tail_file(self):
        content = self.vfs.get_file_content('test.txt')
        self.assertIsNotNone(content)
        self.assertTrue(isinstance(content, str))
    
    def test_du_directory(self):
        size = self.vfs.get_total_size('test.txt')
        self.assertIsNotNone(size)
        self.assertEqual(size, 0)
    
    def test_exit_command(self):
        pass
    
    def tearDown(self):
        os.remove(self.tar_path)

if __name__ == '__main__':
    unittest.main()
```
