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
