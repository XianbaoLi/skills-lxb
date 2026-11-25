from __future__ import annotations

import argparse
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "build_context_capsule.py"
SPEC = importlib.util.spec_from_file_location("build_context_capsule", SCRIPT)
assert SPEC and SPEC.loader
CAPSULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CAPSULE)


class ContextCapsuleTests(unittest.TestCase):
    def inputs(self, root: Path) -> argparse.Namespace:
        (root / "source.pdf").write_bytes(b"%PDF-1.4 bounded unit")
        (root / "source.txt").write_text("source paragraph\n" * 100, encoding="utf-8")
        (root / "terms.md").write_text("bias: 偏见\n", encoding="utf-8")
        (root / "context.md").write_text("Previous: chapter 20.\n", encoding="utf-8")
        return argparse.Namespace(
            output_dir=str(root / "packet"),
            unit_id="chapter-21",
            source_pdf=str(root / "source.pdf"),
            source_text=str(root / "source.txt"),
            terms=str(root / "terms.md"),
            context=str(root / "context.md"),
            author_tex=[],
            figure=[],
            output_name="chapter21.tex",
        )

    def test_builds_bounded_hash_backed_packet(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = CAPSULE.build_packet(self.inputs(root))
            task = json.loads((output / "TASK.json").read_text(encoding="utf-8"))
            manifest = json.loads(
                (output / "PACKET_MANIFEST.json").read_text(encoding="utf-8")
            )

            self.assertEqual("chapter-21", task["unit_id"])
            self.assertEqual("output/chapter21.tex", task["output_tex"])
            self.assertEqual(1, task["execution_limits"]["initial_translation_passes"])
            self.assertEqual(1, task["execution_limits"]["targeted_repair_passes"])
            self.assertTrue(task["execution_limits"]["batch_text_reads"])
            self.assertFalse(task["execution_limits"]["worker_compilation"])
            self.assertTrue((output / "CONTRACT.md").is_file())
            self.assertTrue((output / "source" / "source.pdf").is_file())
            self.assertTrue(manifest["context_smaller_than_source"])
            self.assertEqual(6, len(manifest["files"]))
            self.assertTrue(all(item["sha256"] for item in manifest["files"]))

    def test_filters_markdown_glossary_to_matches_and_bookwide_rows(self) -> None:
        glossary = (
            "# Glossary\n\n"
            "| English term | Preferred Chinese | Context |\n"
            "|---|---|---|\n"
            "| deep learning | 深度学习 | local |\n"
            "| bias | 偏差 | local |\n"
            "| generalization | 泛化 | Book-wide |\n"
            "| field | 场 | local |\n"
        )
        output, stats = CAPSULE.filter_markdown_terms(
            glossary, "Deep learning is not a battlefield metaphor."
        )

        self.assertTrue(stats["applied"])
        self.assertEqual(4, stats["total_rows"])
        self.assertEqual(2, stats["output_rows"])
        self.assertIn("deep learning", output)
        self.assertIn("generalization", output)
        self.assertNotIn("| bias |", output)
        self.assertNotIn("| field |", output)

    def test_copies_unrecognized_term_format_without_loss(self) -> None:
        terms = "bias: 偏差\nvariance: 方差\n"
        output, stats = CAPSULE.filter_markdown_terms(terms, "bias")

        self.assertFalse(stats["applied"])
        self.assertEqual(terms, output)

    def test_matches_common_pdf_typography_variants(self) -> None:
        self.assertTrue(
            CAPSULE.term_occurs("Landau--Ginzburg", "the Landau–Ginzburg model")
        )
        self.assertTrue(CAPSULE.term_occurs("Fisher's theorem", "Fisher’s theorem"))

    def test_preserves_trailing_notes_after_filtered_table(self) -> None:
        glossary = (
            "# Glossary\n\n"
            "| Source term | Preferred Chinese | Context |\n"
            "|---|---|---|\n"
            "| policy | 策略 | reinforcement learning |\n\n"
            "Do not force context-specific senses.\n"
        )
        output, stats = CAPSULE.filter_markdown_terms(glossary, "public policy")

        self.assertTrue(stats["applied"])
        self.assertIn("reinforcement learning", output)
        self.assertIn("Do not force context-specific senses.", output)

    def test_copies_multiple_glossary_tables_without_truncation(self) -> None:
        glossary = (
            "| Source term | Chinese |\n|---|---|\n| bias | 偏差 |\n\n"
            "| English term | Chinese |\n|---|---|\n| policy | 政策 |\n"
        )
        output, stats = CAPSULE.filter_markdown_terms(glossary, "bias policy")

        self.assertFalse(stats["applied"])
        self.assertIn("multiple recognized", stats["reason"])
        self.assertEqual(glossary, output)

    def test_refuses_nonempty_output_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            args = self.inputs(root)
            packet = Path(args.output_dir)
            packet.mkdir()
            (packet / "existing.txt").write_text("keep", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "not empty"):
                CAPSULE.build_packet(args)

            self.assertEqual("keep", (packet / "existing.txt").read_text())

    def test_reports_oversized_support_without_hiding_it(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            args = self.inputs(root)
            Path(args.source_text).write_text("short", encoding="utf-8")
            output = CAPSULE.build_packet(args)
            manifest = json.loads(
                (output / "PACKET_MANIFEST.json").read_text(encoding="utf-8")
            )

            self.assertFalse(manifest["context_smaller_than_source"])
            self.assertGreater(manifest["support_to_source_ratio"], 1)

    def test_routed_contracts_preserve_core_quality_boundaries(self) -> None:
        references = Path(__file__).parents[1] / "references"
        worker = (references / "routed-worker-contract.md").read_text(
            encoding="utf-8"
        )
        reviewer = (references / "routed-review-contract.md").read_text(
            encoding="utf-8"
        )

        for anchor in (
            "source.pdf",
            "mathematical dependencies",
            "status: blocked",
            "one translation pass",
            "one bounded repair request",
            "only in its stated context",
            "Batch-read",
        ):
            self.assertIn(anchor, worker)
        for anchor in ("published PDF", "model identity", "severe", "one review pass"):
            self.assertIn(anchor, reviewer)


if __name__ == "__main__":
    unittest.main()
