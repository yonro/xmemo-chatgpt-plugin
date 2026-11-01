import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from validate_repo import ROOT, package_path, validate_repository
from package_plugin import build

class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        for name in ('plugins', 'submission', '.agents'):
            shutil.copytree(ROOT / name, self.root / name)
        self.plugin = self.root / 'plugins/xmemo'
    def tearDown(self):
        self.temp.cleanup()
    def test_deterministic(self):
        path = build(self.root, 'v1.0.2')
        first = path.read_bytes()
        self.assertEqual(first, build(self.root).read_bytes())
    def test_tag_mismatch(self):
        with self.assertRaises(ValueError): build(self.root, '9.9.9')
        self.assertFalse((self.root / 'dist').exists())
    def test_traversal(self):
        with self.assertRaises(ValueError): package_path(self.plugin, './../outside')
    def test_symlink(self):
        (self.plugin / 'assets/leak.png').symlink_to(ROOT / 'README.md')
        with self.assertRaises(ValueError): build(self.root)
    def test_unexpected_file(self):
        (self.plugin / '.env').write_text('LOCAL_CONFIG=private')
        with self.assertRaises(ValueError): build(self.root)
    def test_auth_downgrade(self):
        p = self.plugin / '.mcp.json'
        data=json.loads(p.read_text());data['mcpServers']['xmemo']['extensions']['com.openai']['auth']['type']='none';p.write_text(json.dumps(data))
        with self.assertRaises(ValueError): validate_repository(self.root)
    def test_metadata_limits(self):
        p=self.plugin / '.codex-plugin/plugin.json'
        original=json.loads(p.read_text())
        for value in ('x'*31, 'line\nbreak'):
            data=json.loads(json.dumps(original));data['interface']['shortDescription']=value;p.write_text(json.dumps(data))
            with self.assertRaises(ValueError): validate_repository(self.root)
    def test_normalized_duplicate_prompts(self):
        p=self.plugin / '.codex-plugin/plugin.json';data=json.loads(p.read_text());data['interface']['defaultPrompt']=['Resume work','Resume  work'];p.write_text(json.dumps(data))
        with self.assertRaises(ValueError): validate_repository(self.root)

if __name__ == '__main__': unittest.main()
