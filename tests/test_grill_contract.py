"""Static skill-contract regressions; not a model/UI behavior benchmark.

Run: python -m unittest discover -s tests -v
These tests inspect the actual distributed instructions. They do not simulate
permission enforcement or claim that an LLM always follows the instructions.
"""
from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "grill-me"


class ApprovalBoundaryTests(unittest.TestCase):
    def test_understanding_choice_authorization_execution_are_separate(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("理解 ≠ 选择 ≠ 授权 ≠ 执行", text)
        self.assertIn("clarify / AskUserQuestion 不是审批工具", text)
        self.assertIn("跳过审批题不代表同意或拒绝", text)
        self.assertIn("既有授权", text)
        self.assertNotIn("确认后按需执行 / 保存", text)


class TeachingSupportTests(unittest.TestCase):
    def test_confusion_pauses_questions_and_teaches_before_choice(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        for rule in (
            "先教后问（Teach → Check → Decide）",
            "讲解期间暂停整批问题",
            "术语白话 → 一个具体例子 → 选项的后果",
            "不懂不是偏好",
            "强度与讲解深度独立",
            "只恢复 1 题",
        ):
            self.assertIn(rule, text)
        for obsolete in (
            "不接受「都行 / 随便」",
            "讲解仅在用户要求时展开",
        ):
            self.assertNotIn(obsolete, text)


class ActivationBoundaryTests(unittest.TestCase):
    def test_loading_for_maintenance_does_not_start_an_interview(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        for rule in (
            "仅在当前用户明确要求开始或继续多轮访谈时启用",
            "加载不等于启动访谈",
            "历史记忆、引用文本或技能名称的出现不是启动指令",
            "普通计划、代码修改、权限审批不自动切入",
        ):
            self.assertIn(rule, text)


class ArtifactBaselineTests(unittest.TestCase):
    """Packaging/instruction guards, not live platform permission tests."""

    def test_frontmatter_is_bounded_and_versioned(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        front, body = text[4:].split("\n---\n", 1)
        self.assertRegex(front, r"(?m)^name: grill-me$")
        descriptions = re.findall(r'(?m)^description: "(.*)"$', front)
        self.assertEqual(len(descriptions), 1)
        description = descriptions[0]
        self.assertLessEqual(len(description), 60)
        self.assertTrue(description.endswith("."))
        self.assertIn('version: "2.5.0"', front)
        self.assertTrue(body.strip())

    def test_internal_skill_references_exist(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        paths = re.findall(r"`((?:references|templates)/[^`]+\.md)`", text)
        self.assertTrue(paths)
        for relative in paths:
            with self.subTest(relative=relative):
                self.assertTrue((SKILL / relative).is_file())

    def test_session_template_separates_permission_and_execution(self):
        text = (SKILL / "templates/session.grill.md").read_text(encoding="utf-8")
        for field in (
            "interview_status: in-progress", "execution_status: not-started",
            "## Understanding gaps", "## Authorization", "## Memory writes",
            "native_gate", "unknown", "not a substitute",
        ):
            self.assertIn(field, text)

    def test_example_question_payload_is_valid_hermes_shape(self):
        text = (SKILL / "references/example-round.md").read_text(encoding="utf-8")
        blocks = re.findall(r"```json\n(.*?)\n```", text, re.S)
        self.assertEqual(len(blocks), 1)
        questions = json.loads(blocks[0])["questions"]
        self.assertGreater(len(questions), 0)
        self.assertLessEqual(len(questions), 5)
        for q in questions:
            self.assertTrue(q["question"])
            self.assertGreaterEqual(len(q["choices"]), 2)
            self.assertLessEqual(len(q["choices"]), 4)
            self.assertFalse(q.get("multi_select", False))

    def test_examples_cover_skips_denials_and_pending_memory(self):
        text = (SKILL / "references/example-round.md").read_text(encoding="utf-8")
        for scenario in ("跳过", "不撤销", "拒绝", "待审", "重档", "不是新一轮"):
            self.assertIn(scenario, text)

    def test_portable_skill_does_not_include_private_paths(self):
        for path in SKILL.rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertNotRegex(text, r"(?<![A-Za-z])[A-Za-z]:[/\\]")
                self.assertNotRegex(text, r"/(?:home|Users)/[^/<>\s`]+")
                self.assertNotIn("USER.md.snapshot-2026", text)


class ResumeBoundaryTests(unittest.TestCase):
    def test_legacy_done_is_not_evidence_of_execution(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("旧版单一 done", text)
        self.assertIn("execution_status=unknown", text)
        self.assertIn("没有新的待决问题时不机械追加问卷", text)


class NeedsDiscoveryTests(unittest.TestCase):
    def test_vague_goals_are_explored_without_command_approval_questions(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("不要求用户先有完整计划", text)
        self.assertIn("模糊想法 → 需求探索 → 方案取舍 → 清晰计划", text)
        self.assertIn("不在访谈中询问命令批准", text)

    def test_explanation_request_is_queued_for_the_next_round(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        for rule in ("needs-explanation", "下一轮优先解释", "多选同时", "保留其他问题已回答的内容"):
            self.assertIn(rule, text)
        self.assertNotIn("表单有空位可作选项", text)

    def test_every_example_choice_question_has_a_visible_help_option(self):
        text = (SKILL / "references/example-round.md").read_text(encoding="utf-8")
        blocks = re.findall(r"```json\n(.*?)\n```", text, re.S)
        self.assertTrue(blocks)
        help_label = "我不懂这个问题，先讲解"
        for block in blocks:
            for question in json.loads(block)["questions"]:
                choices = question.get("choices", [])
                if choices:
                    self.assertIn(help_label, choices)
                    self.assertEqual(choices[-1], help_label)
                    self.assertLessEqual(len(choices), 4)
                    self.assertGreaterEqual(len(choices[:-1]), 2)


if __name__ == "__main__":
    unittest.main()
