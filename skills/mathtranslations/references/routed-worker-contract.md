# Routed Translation Worker Contract

Execute the unit described by `TASK.json` in one translation pass. Batch-read
the task, extracted source text, terms, and local context together, then write
the requested outputs once. Read only the files listed there. Do not search
for an older translation, load general workflow documentation, or inspect
material outside this packet. Open targeted PDF pages only when the text
extraction is ambiguous or visual structure must be resolved.

## Source authority

- `source/source.pdf` is authoritative for visible content, mathematics, and
  structure.
- `source/source.txt` is a searchable extraction aid. If it conflicts with the
  PDF or looks damaged, follow the PDF and record the ambiguity.
- Use only the supplied terms and local context. Apply a glossary translation
  only in its stated context; when the source usage falls outside that context
  or is ambiguous, record the conflict and translate by meaning. Do not
  silently invent or modernize facts, citations, labels, definitions, or
  missing proof steps.

## Translation

- Produce natural, concise Chinese while preserving meaning, qualifications,
  definitions, hypotheses, notation, equations, references, footnotes,
  figures, tables, lists, and hierarchy.
- Preserve mathematical dependencies and the force of words such as “if”,
  “only if”, “unique”, and “respectively”. Keep mathematics in LaTeX.
- Reuse stable labels, macros, citation keys, and supplied terminology. Record
  a terminology conflict instead of choosing silently.
- Use `enumerate` for ordered lists, TeX `` and '' for Chinese double quotes,
  and the supplied project's display-math conventions. Preserve ordinary
  figures faithfully and keep arrow-and-node mathematical diagrams editable.
- Do not split or omit a proof, derivation, figure-caption pair, algorithm, or
  paragraph that belongs to this unit.
- Do not hard-code numbered references when a supplied label can be used.

## Output boundary

Write only the TeX path and report path named by `TASK.json`. The report must
be JSON with these fields:

```json
{
  "unit_id": "...",
  "status": "complete|blocked",
  "source_coverage": "...",
  "terms_added_or_changed": [],
  "ambiguities": [],
  "missing_assets": [],
  "notes_for_controller": []
}
```

Do not compile, run a project-wide audit, re-extract the complete PDF, package
the book, or perform a general visual review. The controller owns those steps.
If a supplied file is insufficient, stop with `status: blocked` and name the
specific missing evidence rather than expanding the search scope.

After writing the TeX and report, stop. Do not start a self-review or rewrite
loop. The controller may later provide one bounded repair request containing
only failed passages, their immediate context, and concrete findings. In that
case, change only those passages and stop after the repair; do not reread or
rewrite the complete unit.
