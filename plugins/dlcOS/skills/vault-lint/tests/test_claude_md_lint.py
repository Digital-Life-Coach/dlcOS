import datetime as dt
import subprocess
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
import claude_md_lint as L  # noqa: E402

FIX = HERE / "fixture-vault"
TODAY = dt.date(2026, 11, 18)


class Lint(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.res = L.run(FIX.resolve(), today=TODAY)
        cls.by = {}
        for f in cls.res["findings"]:
            cls.by.setdefault(f["check"], []).append(f)

    def test_size_ranking_and_count(self):
        self.assertEqual(self.res["file_count"], 2)
        sizes = [p["bytes"] for p in self.res["profiles"]]
        self.assertEqual(sizes, sorted(sizes, reverse=True))

    def test_startup_load_chain(self):
        row = next(r for r in self.res["loads"] if r["folder"] == "Clients/Acme")
        self.assertEqual(row["chain"], ["CLAUDE.md", "Clients/Acme/CLAUDE.md"])
        total = sum(p["bytes"] for p in self.res["profiles"])
        self.assertEqual(row["bytes"], total)

    def test_dead_pointers_only(self):
        targets = " ".join(f["evidence"] for f in self.by["pointers"])
        self.assertIn("Missing Page", targets)
        self.assertIn("Reference/gone.md", targets)
        self.assertNotIn("notes.md", targets)
        self.assertEqual(len(self.by["pointers"]), 2)

    def test_stale_inferred(self):
        self.assertEqual(len(self.by["inferred"]), 1)
        fresh = L.check_inferred(L.Ctx(FIX.resolve(), None), [FIX / "CLAUDE.md"], dt.date(2026, 1, 20), 30)
        self.assertEqual(fresh, [])

    def test_session_context_overfull(self):
        self.assertEqual([f["path"] for f in self.by["sessions"]], ["CLAUDE.md"])

    def test_story_section_flagged(self):
        acme = next(p for p in self.res["profiles"] if p["path"].endswith("Acme/CLAUDE.md"))
        self.assertEqual(acme["story_sections"], ["The invoice bug"])
        self.assertGreater(acme["story_share"], 0.3)
        root = next(p for p in self.res["profiles"] if p["path"] == "CLAUDE.md")
        self.assertEqual(root["story_sections"], [])

    def test_duplicate_rule(self):
        self.assertEqual(len(self.by["dupes"]), 1)

    def test_no_hardcoded_personal_paths(self):
        src = (HERE.parent / "scripts" / "claude_md_lint.py").read_text()
        for needle in ("justin", "Bradshaw", "jcbshaw", "Work/Automation", "GTD/"):
            self.assertNotIn(needle, src)

    def test_root_resolution(self):
        import os
        self.assertEqual(L.resolve_root(str(FIX), Path("/")), FIX.resolve())
        with self.assertRaises(SystemExit):
            old = os.environ.pop("VAULT_ROOT", None)
            try:
                L.resolve_root(None, Path("/nonexistent"))
            finally:
                if old:
                    os.environ["VAULT_ROOT"] = old

    def test_marker_resolution(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "CLAUDE.md").write_text(f"<!-- dlcOS:vault-root --> {FIX.resolve()}\n")
            self.assertEqual(L.resolve_root(None, Path(d)), FIX.resolve())

    def test_cli_runs(self):
        p = subprocess.run([sys.executable, str(HERE.parent / "scripts" / "claude_md_lint.py"),
                            "--vault", str(FIX)], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("Startup load", p.stdout)


if __name__ == "__main__":
    unittest.main()
