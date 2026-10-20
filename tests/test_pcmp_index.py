#!/usr/bin/env python3
"""
Unit tests for PCMP SQLite Derivative Indexer and Compliance Checker (scripts/pcmp_index.py).
Uses Python standard library unittest (zero dependencies).
"""

import sys
import unittest
from pathlib import Path
import tempfile
import shutil

# Ensure scripts directory is importable
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from pcmp_index import PCMPIndex, TAG_NORMALIZATION


class TestPCMPIndex(unittest.TestCase):
    def setUp(self):
        self.repo_root = REPO_ROOT
        self.indexer = PCMPIndex(self.repo_root)

    def test_compute_sha256(self):
        h1 = PCMPIndex.compute_sha256("hello world")
        h2 = PCMPIndex.compute_sha256("hello world")
        h3 = PCMPIndex.compute_sha256("different content")
        self.assertEqual(h1, h2)
        self.assertNotEqual(h1, h3)

    def test_parse_frontmatter(self):
        text = """---
pcmp_version: "2.1"
revision: 5
updated: 2026-10-20
---

# Title
Body text
"""
        fm, body = self.indexer.parse_frontmatter(text)
        self.assertEqual(fm.get("pcmp_version"), "2.1")
        self.assertEqual(fm.get("revision"), "5")
        self.assertEqual(fm.get("updated"), "2026-10-20")
        self.assertIn("# Title", body)

    def test_tag_normalization(self):
        self.assertEqual(TAG_NORMALIZATION["事实"], "fact")
        self.assertEqual(TAG_NORMALIZATION["假设"], "assumption")
        self.assertEqual(TAG_NORMALIZATION["提议"], "proposal")
        self.assertEqual(TAG_NORMALIZATION["已确认"], "accepted")
        self.assertEqual(TAG_NORMALIZATION["未决"], "open")

    def test_compliance_check_on_current_repo(self):
        """Current repository must pass compliance check without errors."""
        errors, warnings = self.indexer.check_compliance()
        self.assertEqual(errors, [], f"Repository compliance check failed with errors: {errors}")

    def test_compliance_check_detects_unconfirmed_accepted_adr(self):
        """Verify that an Accepted ADR without confirmation source triggers error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            ai_dir = tmp_path / "ai"
            ai_dir.mkdir(parents=True)
            
            # Create valid STATE.md
            (ai_dir / "STATE.md").write_text("""---
pcmp_version: "2.1"
revision: 1
updated: 2026-10-20
---
# State
""", encoding="utf-8")
            
            # Create invalid DECISIONS.md (Accepted without source)
            (ai_dir / "DECISIONS.md").write_text("""---
pcmp_version: "2.1"
revision: 1
updated: 2026-10-20
---
## DEC-999 — Bad Decision
日期: 2026-10-20 | 状态: Accepted
- 决策: Do something risky
""", encoding="utf-8")
            
            tmp_indexer = PCMPIndex(tmp_path)
            errors, warnings = tmp_indexer.check_compliance()
            self.assertTrue(any("DEC-999 is marked 'Accepted' but lacks valid" in e for e in errors),
                            f"Expected missing confirmation source error, got: {errors}")


if __name__ == "__main__":
    unittest.main()
