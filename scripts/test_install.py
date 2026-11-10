"""Installer and skill-location regressions; uses temporary public fixtures only."""

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "scripts" / "install.py"


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="job-workflow-test-")
        self.addCleanup(self.temporary.cleanup)
        self.target = Path(self.temporary.name).resolve()

    def install(self, target=None):
        return subprocess.run(
            [sys.executable, str(INSTALLER), str(target or self.target)],
            cwd=tempfile.gettempdir(), capture_output=True, text=True,
        )

    def test_complete_bundle_and_repeat_install(self):
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stderr)
        names = {p.parent.name for p in (self.target / ".agents/skills").glob("*/SKILL.md")}
        self.assertEqual(len(names), 9)
        self.assertIn("resume-writer", names)
        self.assertIn("application-review", names)
        self.assertFalse((self.target / "skills").exists())
        self.assertEqual(len(list((self.target / ".codex/agents").glob("*.toml"))), 6)
        for relative in (
            ".agents/skills/resume-writer/verbs.md",
            ".agents/skills/user-json-memory/user.schema.json",
            ".codex/hooks/subagent_start.py",
            "formatter/format_resume.py", "AGENTS.md", "instruction.md", "shared-rules.md",
        ):
            self.assertEqual((self.target / relative).read_bytes(), (ROOT / relative).read_bytes())
        self.assertFalse((self.target / "config.json").exists())
        self.assertFalse((self.target / "data").exists())
        self.assertFalse((self.target / "retired").exists())
        self.assertFalse((self.target / ".git").exists())
        self.assertEqual(self.install().returncode, 0)
        (self.target / "config.json").write_text('{"user_name":"private"}')
        (self.target / "data").mkdir()
        self.assertEqual(self.install().returncode, 0)
        self.assertEqual((self.target / "config.json").read_text(), '{"user_name":"private"}')

    def test_conflict_leaves_target_untouched(self):
        original = self.target / "instruction.md"
        original.write_text("custom instructions")
        result = self.install()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Conflicting file:", result.stderr)
        self.assertEqual(original.read_text(), "custom instructions")
        self.assertEqual(list(self.target.iterdir()), [original])

    def test_preserves_custom_codex_configuration(self):
        config = self.target / ".codex/config.toml"
        config.parent.mkdir()
        config.write_text("# custom config")
        result = self.install()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(config.read_text(), "# custom config")
        self.assertFalse((self.target / "AGENTS.md").exists())

    def test_rejects_symlinks_and_non_directory_ancestors(self):
        for name in (".agents", ".codex"):
            with self.subTest(directory=name), tempfile.TemporaryDirectory() as outside:
                link = self.target / name
                link.symlink_to(outside, target_is_directory=True)
                result = self.install()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Destination symlink:", result.stderr)
                self.assertEqual(list(Path(outside).iterdir()), [])
                link.unlink()
        (self.target / ".agents").write_text("a file")
        result = self.install()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Conflicting directory:", result.stderr)
        self.assertFalse((self.target / "AGENTS.md").exists())

    def test_installed_memory_validator_resolves_project_schema(self):
        self.assertEqual(self.install().returncode, 0)
        script = self.target / ".agents/skills/user-json-memory/validate_user_memory.py"
        spec = importlib.util.spec_from_file_location("installed_memory_validator", script)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(module.ROOT, self.target)
        self.assertTrue(module.SCHEMA_PATH.is_file())
        schema = module.load_json(module.SCHEMA_PATH)
        self.assertIn("$defs", schema)

    def test_hook_still_returns_handoff_context(self):
        self.assertEqual(self.install().returncode, 0)
        result = subprocess.run(
            [sys.executable, str(self.target / ".codex/hooks/subagent_start.py")],
            input="{}", capture_output=True, text=True, cwd=self.target,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)["hookSpecificOutput"]
        self.assertEqual(payload["hookEventName"], "SubagentStart")
        self.assertTrue(payload["additionalContext"])


if __name__ == "__main__":
    unittest.main()
