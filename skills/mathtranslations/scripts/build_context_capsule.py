#!/usr/bin/env python3
"""Build a bounded, hash-backed packet for one routed translation unit."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import unicodedata
from pathlib import Path


ROOT = Path(__file__).parents[1]
CONTRACT = ROOT / "references" / "routed-worker-contract.md"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def text_chars(path: Path) -> int:
    return len(path.read_text(encoding="utf-8"))


def split_markdown_row(line: str) -> list[str]:
    """Split a simple Markdown table row without breaking escaped pipes."""
    content = line.strip().strip("|")
    cells: list[str] = []
    current: list[str] = []
    escaped = False
    for char in content:
        if char == "|" and not escaped:
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(char)
        escaped = char == "\\" and not escaped
        if char != "\\":
            escaped = False
    cells.append("".join(current).strip())
    return cells


def is_separator_row(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def source_column(headers: list[str]) -> int | None:
    names = {
        "english term",
        "source term",
        "source",
        "英文术语",
        "原文术语",
        "原文",
    }
    for index, header in enumerate(headers):
        normalized = re.sub(r"[*_`]", "", header).strip().casefold()
        if normalized in names:
            return index
    return None


def term_forms(cell: str) -> list[str]:
    cleaned = re.sub(r"[*_`]", "", cell).strip()
    forms = [cleaned]
    forms.extend(re.findall(r"\(([^()]+)\)", cleaned))
    forms.append(re.sub(r"\s*\([^()]+\)\s*$", "", cleaned))
    for separator in (" / ", ";"):
        forms.extend(part.strip() for part in cleaned.split(separator))
    return sorted({form for form in forms if len(form) >= 2}, key=len, reverse=True)


def normalize_match_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).casefold()
    text = re.sub(r"[‐‑‒–—−]+", "-", text)
    text = re.sub(r"-{2,}", "-", text)
    text = text.replace("’", "'").replace("‘", "'")
    return re.sub(r"\s+", " ", text)


def term_occurs_in_normalized_source(term: str, source: str) -> bool:
    term = normalize_match_text(term)
    if re.search(r"[\u3400-\u9fff]", term):
        return term in source
    escaped = re.escape(term)
    left = r"(?<![\w])" if term[0].isalnum() else ""
    right = r"(?![\w])" if term[-1].isalnum() else ""
    return re.search(left + escaped + right, source) is not None


def term_occurs(term: str, source: str) -> bool:
    return term_occurs_in_normalized_source(term, normalize_match_text(source))


def filter_markdown_terms(glossary: str, source: str) -> tuple[str, dict[str, object]]:
    """Keep glossary rows used by the unit plus explicitly book-wide rows."""
    lines = glossary.splitlines()
    tables: list[tuple[int, list[str], int]] = []
    for index in range(len(lines) - 1):
        headers = split_markdown_row(lines[index])
        separator = split_markdown_row(lines[index + 1])
        column = source_column(headers)
        if column is not None and len(separator) == len(headers) and is_separator_row(separator):
            tables.append((index, headers, column))

    if len(tables) != 1:
        reason = "no recognized Markdown glossary table"
        if len(tables) > 1:
            reason = "multiple recognized Markdown glossary tables"
        return glossary, {
            "applied": False,
            "reason": reason,
            "input_chars": len(glossary),
            "output_chars": len(glossary),
        }

    index, headers, column = tables[0]
    normalized_source = normalize_match_text(source)
    rows: list[str] = []
    cursor = index + 2
    while cursor < len(lines) and lines[cursor].lstrip().startswith("|"):
        rows.append(lines[cursor])
        cursor += 1

    kept: list[str] = []
    matched = 0
    global_rows = 0
    for row in rows:
        cells = split_markdown_row(row)
        if column >= len(cells):
            continue
        is_global = any(
            marker in row.casefold() for marker in ("book-wide", "bookwide", "全书")
        )
        is_match = any(
            term_occurs_in_normalized_source(form, normalized_source)
            for form in term_forms(cells[column])
        )
        if is_match:
            matched += 1
        if is_global:
            global_rows += 1
        if is_match or is_global:
            kept.append(row)

    output_lines = lines[:index] + [lines[index], lines[index + 1], *kept] + lines[cursor:]
    output = "\n".join(output_lines).rstrip() + "\n"
    return output, {
        "applied": True,
        "total_rows": len(rows),
        "matched_rows": matched,
        "global_rows": global_rows,
        "output_rows": len(kept),
        "input_chars": len(glossary),
        "output_chars": len(output),
    }


def require_file(path: Path, label: str) -> Path:
    path = path.resolve()
    if not path.is_file():
        raise ValueError(f"{label} is not a readable file: {path}")
    return path


def prepare_output(path: Path) -> Path:
    path = path.resolve()
    if path.exists() and any(path.iterdir()):
        raise ValueError(f"output directory is not empty: {path}")
    path.mkdir(parents=True, exist_ok=True)
    return path


def copy_record(
    source: Path, destination: Path, role: str, packet_root: Path
) -> dict[str, object]:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    return {
        "role": role,
        "path": destination.relative_to(packet_root).as_posix(),
        "bytes": destination.stat().st_size,
        "sha256": sha256(destination),
    }


def file_record(path: Path, role: str, packet_root: Path) -> dict[str, object]:
    return {
        "role": role,
        "path": path.relative_to(packet_root).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def build_packet(args: argparse.Namespace) -> Path:
    output = prepare_output(Path(args.output_dir))
    source_pdf = require_file(Path(args.source_pdf), "source PDF")
    source_text = require_file(Path(args.source_text), "source text")
    terms = require_file(Path(args.terms), "terms")
    context = require_file(Path(args.context), "context")

    records: list[dict[str, object]] = []
    records.append(
        copy_record(CONTRACT, output / "CONTRACT.md", "worker_contract", output)
    )
    records.append(
        copy_record(source_pdf, output / "source" / "source.pdf", "authority", output)
    )
    records.append(
        copy_record(
            source_text, output / "source" / "source.txt", "extraction_aid", output
        )
    )
    glossary = terms.read_text(encoding="utf-8")
    source_body = source_text.read_text(encoding="utf-8")
    filtered_terms, term_stats = filter_markdown_terms(glossary, source_body)
    packet_terms = output / "source" / "terms.md"
    packet_terms.write_text(filtered_terms, encoding="utf-8")
    records.append(file_record(packet_terms, "unit_terms", output))
    records.append(
        copy_record(context, output / "source" / "context.md", "unit_context", output)
    )

    task_files = {
        "author_tex": [],
        "figures": [],
    }
    for role, values, directory in (
        ("author_tex", args.author_tex, "tex"),
        ("figures", args.figure, "figures"),
    ):
        seen_names: set[str] = set()
        for value in values:
            source = require_file(Path(value), role)
            if source.name in seen_names:
                raise ValueError(f"duplicate {role} filename: {source.name}")
            seen_names.add(source.name)
            relative = Path("source") / directory / source.name
            records.append(copy_record(source, output / relative, role, output))
            task_files[role].append(relative.as_posix())

    output_path = (Path("output") / args.output_name).as_posix()
    report_path = (Path("output") / "WORKER_REPORT.json").as_posix()
    (output / "output").mkdir(exist_ok=True)
    task = {
        "unit_id": args.unit_id,
        "source_pdf": "source/source.pdf",
        "source_text": "source/source.txt",
        "terms": "source/terms.md",
        "context": "source/context.md",
        **task_files,
        "output_tex": output_path,
        "output_report": report_path,
        "execution_limits": {
            "initial_translation_passes": 1,
            "targeted_repair_passes": 1,
            "batch_text_reads": True,
            "worker_compilation": False,
            "worker_project_audit": False,
            "worker_pdf_reextraction": False,
        },
    }
    (output / "TASK.json").write_text(
        json.dumps(task, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    records.append(
        {
            "role": "task",
            "path": "TASK.json",
            "bytes": (output / "TASK.json").stat().st_size,
            "sha256": sha256(output / "TASK.json"),
        }
    )

    source_chars = text_chars(output / "source" / "source.txt")
    support_chars = text_chars(output / "source" / "terms.md") + text_chars(
        output / "source" / "context.md"
    )
    manifest = {
        "schema_version": 1,
        "unit_id": args.unit_id,
        "source_text_chars": source_chars,
        "support_text_chars": support_chars,
        "support_to_source_ratio": (
            round(support_chars / source_chars, 6) if source_chars else None
        ),
        "context_smaller_than_source": bool(source_chars and support_chars < source_chars),
        "terms_source_sha256": sha256(terms),
        "terms_filter": term_stats,
        "files": records,
    }
    (output / "PACKET_MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return output


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--output-dir", required=True)
    result.add_argument("--unit-id", required=True)
    result.add_argument("--source-pdf", required=True)
    result.add_argument("--source-text", required=True)
    result.add_argument("--terms", required=True)
    result.add_argument("--context", required=True)
    result.add_argument("--author-tex", action="append", default=[])
    result.add_argument("--figure", action="append", default=[])
    result.add_argument("--output-name", default="unit.tex")
    return result


def main() -> int:
    try:
        output = build_packet(parser().parse_args())
    except ValueError as error:
        print(f"error: {error}")
        return 2
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
