"""Static resource/connected-contract checks, not model or hosted acceptance."""
import json
import re
import unittest
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / 'plugins/xmemo/skills'
CONTRACT = json.loads((ROOT / 'submission/connected-tool-contract.json').read_text())['tools']

class SkillContractTests(unittest.TestCase):
    def test_local_references_resolve_inside_package(self):
        for path in SKILLS.rglob('*.md'):
            text = path.read_text()
            links = re.findall(r'\]\(([^)#]+)(?:#[^)]*)?\)', text)
            links += re.findall(r'`((?:\.\./|references/|assets/)[^`]+\.md)`', text)
            for link in links:
                if '://' in link:
                    continue
                target = (path.parent / link).resolve()
                self.assertTrue(target.is_relative_to(SKILLS.resolve()), (path, link))
                self.assertTrue(target.is_file(), (path, link))

    def test_routing_names_match_connected_inventory(self):
        path = SKILLS / 'xmemo-memory-steward/references/tool-routing.md'
        routed = set(re.findall(r'\| `([a-z_]+)` \|', path.read_text()))
        self.assertEqual(routed, set(CONTRACT))

    def test_temporal_examples_match_exposed_parameters_and_windows(self):
        path = SKILLS / 'xmemo-memory-steward/references/temporal-queries.md'
        cases = re.findall(r'```json\n(.*?)\n```', path.read_text(), re.S)
        self.assertTrue(cases)
        for raw in cases:
            call = json.loads(raw)
            args = call['arguments']
            self.assertLessEqual(set(args), set(CONTRACT[call['tool']]['parameters']))
            self.assertTrue(args.get('query'))
            if args.get('query_mode') == 'activity_log':
                self.assertTrue(args.get('since') and args.get('until'))
            if 'time_order' in args:
                self.assertIn(args['time_order'], ('asc', 'desc'))
            if 'since' in args and 'until' in args:
                start, end = (datetime.fromisoformat(args[k]) for k in ('since', 'until'))
                self.assertIsNotNone(start.tzinfo)
                self.assertIsNotNone(end.tzinfo)
                self.assertGreater(end - start, timedelta(0))
                self.assertLessEqual(end - start, timedelta(days=90))

if __name__ == '__main__':
    unittest.main()
