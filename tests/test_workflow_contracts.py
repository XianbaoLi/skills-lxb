"""Static workflow contract checks; not OCR or translation quality benchmarks."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / "workflows"


class WorkflowInventoryTests(unittest.TestCase):
    def test_catalogue_and_workflows_exist(self):
        expected = (
            "README.md",
            "scan-pdf-to-source-markdown.md",
            "source-markdown-to-chinese-candidate.md",
            "scanned-pdf-to-chinese-candidate.md",
            "review-and-accept-translation.md",
        )
        for name in expected:
            with self.subTest(name=name):
                self.assertTrue((WORKFLOWS / name).is_file())

    def test_each_workflow_has_required_metadata(self):
        for path in WORKFLOWS.glob("*.md"):
            if path.name == "README.md":
                continue
            text = path.read_text(encoding="utf-8")
            self.assertTrue(text.startswith("---\n"), path.name)
            front = text.split("---", 2)[1]
            for field in ("workflow_id:", "version:", "status: specification"):
                with self.subTest(path=path.name, field=field):
                    self.assertIn(field, front)

    def test_internal_markdown_links_resolve(self):
        for path in WORKFLOWS.glob("*.md"):
            text = path.read_text(encoding="utf-8")
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
                target = target.split("#", 1)[0]
                if target:
                    resolved = (path.parent / target).resolve()
                    with self.subTest(path=path.name, target=target):
                        self.assertTrue(resolved.is_file())

    def test_skill_references_resolve(self):
        skill_names = {
            p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md")
        }
        known_names = {
            "mineru", "stem-notes", "mathtranslations", "book-to-skill",
            "study-atlas", "scientific-writing", "scientific-visualization",
            "scientific-schematics", "scientific-critical-thinking",
            "peer-review", "citation-management", "grill-me",
        }
        for path in WORKFLOWS.glob("*.md"):
            text = path.read_text(encoding="utf-8")
            for name in re.findall(r"(?<![A-Za-z0-9_-])([a-z][a-z0-9-]+)(?![A-Za-z0-9_-])", text):
                if name in known_names:
                    self.assertIn(name, skill_names, f"{path.name}: {name}")

    def test_scanned_pdf_workflow_is_local_first_and_non_destructive(self):
        text = (WORKFLOWS / "scan-pdf-to-source-markdown.md").read_text(encoding="utf-8")
        for required in (
            "original PDF unchanged",
            "Do not use remote parsing",
            "mineru parse",
            "next_request",
            "source-reviewed",
            "待核对",
        ):
            self.assertIn(required, text)

    def test_translation_candidate_is_not_automatically_final(self):
        text = (WORKFLOWS / "source-markdown-to-chinese-candidate.md").read_text(encoding="utf-8")
        self.assertIn(".zh-CN.candidate.md", text)
        self.assertIn("not automatically accepted", text)
        self.assertIn("Do not solve exercises", text)
        self.assertIn("translation_status: candidate", text)

    def test_end_to_end_workflow_composes_the_two_stages(self):
        text = (WORKFLOWS / "scanned-pdf-to-chinese-candidate.md").read_text(encoding="utf-8")
        self.assertIn("WF-DOC-01", text)
        self.assertIn("WF-TR-01", text)
        self.assertIn("BLOCKED", text)
        self.assertIn("candidate", text)

    def test_promotion_requires_explicit_user_approval(self):
        text = (WORKFLOWS / "review-and-accept-translation.md").read_text(encoding="utf-8")
        self.assertIn("explicitly approves", text)
        self.assertIn("Never infer acceptance from silence", text)
        self.assertIn(".zh-CN.md", text)


if __name__ == "__main__":
    unittest.main()
