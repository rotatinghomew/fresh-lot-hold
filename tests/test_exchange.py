"""核对交换资料的客户编号、时序和关联条件。"""
import json
from pathlib import Path
import unittest


SAMPLES = Path(__file__).resolve().parents[1] / "samples"


def rows(name):
    content = (SAMPLES / f"{name}.ndjson").read_text(encoding="utf-8")
    return [json.loads(line) for line in content.splitlines()]


class ExchangeSampleTest(unittest.TestCase):
    def test_records_are_json_objects(self):
        files = sorted(SAMPLES.glob("*.ndjson"))
        self.assertEqual(len(files), 4)
        for path in files:
            with self.subTest(path=path.name):
                records = rows(path.stem)
                self.assertTrue(records)
                self.assertTrue(all(isinstance(row, dict) for row in records))

    def test_related_records_preserve_source_evidence(self):
        lineage = rows("lineage")
        self.assertFalse(any(row["lot"] == lineage[6]["lot"] for row in lineage[:6]))
        self.assertIn(lineage[6]["lot"], lineage[5]["input"])
        self.assertEqual(lineage[3]["lot"], lineage[-1]["lot"])
        self.assertIn(lineage[3]["lot"], lineage[4]["input"])
        self.assertNotIn(lineage[3]["lot"], rows("corrections")[0]["input"])
        moves = rows("transfers")
        self.assertEqual(moves[0]["piece"], moves[3]["piece"])
        self.assertEqual(moves[0]["order"], moves[1]["order"])
        self.assertLess(moves[3]["occurred_at"], rows("notices")[0]["effective_at"])
