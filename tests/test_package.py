import json
import shutil
import sys
import tempfile
import unittest
import zipfile
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
    def test_memory_steward_is_required(self):
        shutil.rmtree(self.plugin / 'skills/xmemo-memory-steward')
        with self.assertRaisesRegex(ValueError, 'Unexpected skill set'):
            build(self.root)

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
    def test_existing_connection_rejects_auth_overrides(self):
        p = self.plugin / '.mcp.json'
        original = json.loads(p.read_text())
        for auth in ({'type': 'oauth', 'baseScopes': ['memory:read', 'memory:write']},
                     {'type': 'none'}, {'type': 'mixed'}, {'type': 'api_key'}, {}, None):
            with self.subTest(auth=auth):
                data = json.loads(json.dumps(original))
                data['mcpServers']['xmemo']['extensions'] = {'com.openai': {'auth': auth}}
                p.write_text(json.dumps(data))
                with self.assertRaisesRegex(ValueError, 'Keep the existing MCP connection'):
                    build(self.root)
                self.assertFalse((self.root / 'dist').exists())

    def test_manifest_rejects_auth_overrides(self):
        p = self.plugin / '.codex-plugin/plugin.json'
        original = json.loads(p.read_text())
        for override in ({'auth': {'type': 'oauth'}},
                         {'authentication': {'type': 'none'}},
                         {'extensions': {'com.openai': {'auth': {'type': 'oauth'}}}}):
            with self.subTest(override=override):
                data = json.loads(json.dumps(original))
                data.update(override)
                p.write_text(json.dumps(data))
                with self.assertRaisesRegex(ValueError, 'Keep the existing MCP connection'):
                    build(self.root)

    def test_existing_connection_rejects_endpoint_drift_and_headers(self):
        p = self.plugin / '.mcp.json'
        original = json.loads(p.read_text())
        for change in ({'url': 'https://example.com/mcp'},
                       {'headers': {'X-Test': 'synthetic'}}, {'type': 'stdio'}):
            with self.subTest(change=change):
                data = json.loads(json.dumps(original))
                data['mcpServers']['xmemo'].update(change)
                p.write_text(json.dumps(data))
                with self.assertRaises(ValueError):
                    build(self.root)

    def test_zip_preserves_connection_without_auth_override(self):
        with zipfile.ZipFile(build(self.root)) as archive:
            manifest = json.loads(archive.read('.codex-plugin/plugin.json'))
            self.assertEqual(manifest['name'], 'app-6a112deb1d4881919bde555b7c16b24b')
            self.assertEqual(manifest['version'], '1.0.2')
            self.assertEqual(manifest['mcpServers'], './.mcp.json')
            self.assertEqual(json.loads(archive.read('.mcp.json')), {
                'mcpServers': {'xmemo': {'type': 'http', 'url': 'https://xmemo.dev/mcp'}}})
            for name in ('.codex-plugin/plugin.json', '.mcp.json'):
                keys = []
                json.loads(archive.read(name), object_pairs_hook=lambda pairs: keys.extend(k for k, _ in pairs) or dict(pairs))
                self.assertFalse({'auth', 'authentication', 'headers'}.intersection(keys))
            self.assertEqual(sum(name.endswith('/SKILL.md') for name in archive.namelist()), 8)
            self.assertIn('skills/xmemo-memory-steward/SKILL.md', archive.namelist())
            self.assertIn('skills/xmemo-memory-steward/agents/openai.yaml', archive.namelist())

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
