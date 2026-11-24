from __future__ import annotations

import hashlib
import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "audit_latex.py"
SPEC = importlib.util.spec_from_file_location("audit_latex", SCRIPT)
assert SPEC and SPEC.loader
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)


class AuditLatexTests(unittest.TestCase):
    def test_bundled_assets_match_expected_versions(self) -> None:
        assets = Path(__file__).parents[1] / "assets"
        expected = {
            "mathtranslations-translation-template.tex": (
                "7887ebed788667eb6cf99eb5be16221a02de8f7771778297d8f8adf3808ca1c6"
            ),
            "logo.pdf": (
                "8b3839adbf870a8c5e825c9f004125816835bbb321617e619e5f589b672fc8d5"
            ),
            "wuyi-logo.svg": (
                "74e624e68eef249bda188cec1fbfd06963af5619bc6e7995e3499e3f376c1628"
            ),
            "wuyi-logo.png": (
                "ccc69555ae29d569560c5056ed761523196d320972a703b24173e04ce72253fe"
            ),
        }

        for name, digest in expected.items():
            with self.subTest(asset=name):
                content = (assets / name).read_bytes()
                self.assertEqual(digest, hashlib.sha256(content).hexdigest())

    def test_clean_project(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "main.tex").write_text(
                "\\label{thm:one}\n"
                "由定理~\\ref{thm:one}可知。\\cite{sample}\n"
                "\\includegraphics{plot}\n",
                encoding="utf-8",
            )
            (root / "refs.bib").write_text(
                "@book{sample, title={Example}}\n", encoding="utf-8"
            )
            (root / "plot.png").write_bytes(b"not-a-real-png")

            errors, warnings = AUDIT.audit(root)

            self.assertEqual([], errors)
            self.assertEqual([], warnings)

    def test_reports_structural_problems(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "main.tex").write_text(
                "\\label{dup}\\label{dup}\n"
                "\\ref{missing}\\cite{unknown}\n"
                "见定理 2.3。TODO\n"
                "\\includegraphics{absent}\n",
                encoding="utf-8",
            )

            errors, warnings = AUDIT.audit(root)

            self.assertTrue(any("duplicate label" in item for item in errors))
            self.assertTrue(any("undefined reference" in item for item in errors))
            self.assertTrue(any("undefined citation" in item for item in errors))
            self.assertTrue(any("missing graphic" in item for item in errors))
            self.assertTrue(any("hard-coded reference" in item for item in warnings))
            self.assertTrue(any("unresolved marker" in item for item in warnings))

    def test_ignores_macro_parameter_references(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "main.tex").write_text(
                "\\newcommand{\\row}[1]{\\pageref*{#1}}\n",
                encoding="utf-8",
            )

            errors, warnings = AUDIT.audit(root)

            self.assertEqual([], errors)
            self.assertEqual([], warnings)

    def test_mathtranslations_profile_accepts_core_contract(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            metadata = {
                "BookTitleCN": "拓扑学",
                "BookTitleEN": "Topology",
                "OriginalAuthor": "Example Author",
                "OriginalEdition": "2nd edition",
                "OriginalPublisher": "Example Press",
                "OriginalYear": "2025",
                "ModelUsed": "Example Model",
                "Reviewer": "曹溪能",
                "TranslationDate": "22 Aug 2026",
            }
            metadata_tex = "\n".join(
                f"\\newcommand{{\\{key}}}{{{value}}}"
                for key, value in metadata.items()
            )
            (root / "main.tex").write_text(
                "% !TeX program = xelatex\n"
                "\\documentclass[UTF8,12pt,fontset=none]{ctexart}\n"
                "\\newcommand{\\newterm}[3]{#2（#3）}\n"
                "\\newcommand{\\printterminology}{}\n"
                "\\newcommand{\\longprooflink}[2]{#2}\n"
                "\\newenvironment{longproof}[2]{}{}\n"
                "\\newenvironment{exercises}{}{}\n"
                "\\newenvironment{answers}[1]{}{}\n"
                "\\usepackage{tikz-cd}\n"
                "\\def\\fonts{FandolSong FandolKai FandolFang cmunrm.otf}\n"
                "\\def\\links{linkcolor=MidnightBlue,citecolor=BrickRed,"
                "urlcolor=MidnightBlue,linktoc=all}\n"
                f"{metadata_tex}\n"
                "\\begin{document}\n"
                "\\begin{titlepage}"
                "\\includegraphics{wuyi-logo.png}"
                "\\end{titlepage}\n"
                "\\newterm{topology}{拓扑}{topology}.\n"
                "封面：Model: \\ModelUsed\\\\审核：\\Reviewer\\\\"
                "Updated: \\TranslationDate.\n"
                "\\longprooflink{main-proof}{查看证明}\n"
                "\\begin{longproof}{main-proof}{主定理}证明.\\end{longproof}\n"
                "\\printterminology\n"
                "\\end{document}\n",
                encoding="utf-8",
            )
            (root / "wuyi-logo.png").write_bytes(b"placeholder")

            errors, warnings = AUDIT.audit(root, profile="mathtranslations")

            self.assertEqual([], errors)
            self.assertEqual([], warnings)

    def test_mathtranslations_profile_rejects_old_cover(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "main.tex").write_text(
                "% !TeX program = xelatex\n"
                "\\documentclass[UTF8,12pt,fontset=none]{ctexart}\n"
                "\\newcommand{\\Reviewer}{曹溪}\n"
                "\\includegraphics{logo.pdf}\n"
                "\\Translator\\ 翻译及重排\n",
                encoding="utf-8",
            )
            (root / "logo.pdf").write_bytes(b"placeholder")

            errors, _ = AUDIT.audit(root, profile="mathtranslations")

            self.assertTrue(any("Reviewer" in item for item in errors))
            self.assertTrue(any("logo.pdf" in item for item in errors))
            self.assertTrue(any("translator credit" in item for item in errors))

    def test_mathtranslations_profile_flags_typesetting_rules(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "main.tex").write_text(
                "% !TeX program = xelatex\n"
                "\\documentclass[UTF8,12pt,fontset=none]{ctexart}\n"
                "\\begin{document}\n"
                "\\[ a+b \\]\n"
                "\\[ c+d \\]\n"
                "中文“引号”示例.\n"
                "1. 手动编号第一条\n"
                "2. 手动编号第二条\n"
                "\\end{document}\n",
                encoding="utf-8",
            )

            _, warnings = AUDIT.audit(root, profile="mathtranslations")

            self.assertTrue(
                any("consecutive display-math" in item for item in warnings)
            )
            self.assertTrue(any("TeX `` and ''" in item for item in warnings))
            self.assertTrue(any("enumerate" in item for item in warnings))

    def test_mathtranslations_profile_reports_drift(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "main.tex").write_text(
                "\\documentclass{article}\n"
                "\\newcommand{\\newterm}[3]{#2}\n"
                "\\newcommand{\\printterminology}{}\n"
                "\\begin{document}\n"
                "\\newterm{bad key}{术语}{term}。\n"
                "\\newterm{bad key}{术语}{term}。\n"
                "\\longprooflink{missing-proof}{查看证明}\n"
                "\\end{document}\n",
                encoding="utf-8",
            )

            errors, warnings = AUDIT.audit(root, profile="mathtranslations")

            self.assertTrue(any("terminology key" in item for item in errors))
            self.assertTrue(any("long-proof key" in item for item in errors))
            self.assertTrue(any("ASCII '.'" in item for item in warnings))
            self.assertTrue(any("XeLaTeX" in item for item in warnings))
            self.assertTrue(any("printterminology" in item for item in warnings))


if __name__ == "__main__":
    unittest.main()
