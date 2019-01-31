import unittest, os.path
from unittest import TestCase

from k2 import cli

class CliTest(TestCase):
    
    def test_get_base_user_group(self):
        base, user, group = cli._get_base_user_group()
        self.assertEqual('test', os.path.basename(base))
        self.assertEqual('simon', user)
        self.assertEqual('staff', group)
    
        base, user, group = cli._get_base_user_group(base='/opt/k2/base')
        self.assertEqual('/opt/k2/base', base)
        self.assertEqual('simon', user)
        self.assertEqual('staff', group)
    
        base, user, group = cli._get_base_user_group(base='/opt/k2/base', user='freddy')
        self.assertEqual('/opt/k2/base', base)
        self.assertEqual('freddy', user)
        self.assertEqual('staff', group)
    
        base, user, group = cli._get_base_user_group(base='/opt/k2/base', user='freddy', group='admin')
        self.assertEqual('/opt/k2/base', base)
        self.assertEqual('freddy', user)
        self.assertEqual('admin', group)
    
    def test_export_k2_base(self):
        self.assertEqual('export K2_BASE=/opt/k2/base', cli._export_k2_base('/opt/k2/base'))
        
    def test_alias_k2(self):
        self.assertEqual('alias k2=/opt/k2/base/venv/bin/k2', cli._alias_k2('/opt/k2/base'))
        
    def test_get_profile(self):
        self.assertEqual('/Users/simon/.bash_profile', cli._get_profile('simon'))
        
    def test_read_profile(self):
        self.assertEqual((False, True), cli._read_profile('simon'))
        
if __name__ == '__main__':
    unittest.main()