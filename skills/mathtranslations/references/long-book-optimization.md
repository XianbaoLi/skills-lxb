# Long-Book Context And Model Routing

Use this only for book-length or multi-chapter work where repeated context and
model calls are a material cost. Ordinary papers and short chapters should use
the main workflow directly.

## Fixed Posture

- Default and ceiling: `gpt-5.6-sol` with `medium` reasoning.
- Optional downshift: `gpt-5.6-terra` with `medium` reasoning.
- Do not use higher reasoning efforts or Luna in the first-stage workflow.
- Route once before a complete semantic unit. Do not dynamically select a
  model turn by turn and do not create a separate routing agent.
- Prefer deterministic tools for coverage, labels, references, figures,
  compilation, pages, fonts, archives, and hashes.
- Keep one writer and one canonical output directory per book.

This routing is an experiment until measured. A cheaper Terra call is not by
itself evidence that the whole workflow uses fewer raw tokens or credits.

## Route A Unit

Keep the unit on Sol medium if any of these signals is present:

1. proofs, continuous derivations, new core definitions, key approximations,
   or explanations of complex formulas;
2. conflict among the published PDF, author TeX, OCR, captions, or context;
3. an open mathematical, symbolic, terminology, or source-text issue;
4. less than a complete major section, or handoff context too large relative
   to the source unit to amortize the switch.

When a signal cannot be decided quickly, keep Sol medium. Final issue rulings,
mathematical review, delivery judgment, and completion sign-off also stay on
Sol medium.

Terra medium may translate a unit only when no signal is present and all of the
following are true:

- the content is mostly continuous technical narrative, examples, historical
  background, applications, or explanation of already-defined concepts;
- formulas are sparse and introduce no core derivation or definition;
- the PDF text is clear and supporting TeX does not visibly conflict with it;
- needed terminology is already stable in `GLOSSARY.md`;
- the unit is a complete major section or chapter, normally at least ten source
  PDF pages;
- structural prechecks found no missing pages, labels, figures, or citations;
- the context capsule is clearly smaller than the unit body.

Do not combine unrelated passages merely to reach the Terra threshold.

## Use A Small Context Capsule

Provide only:

- the current source PDF pages and necessary author TeX, formulas, and figures;
- the preceding and following transition text;
- the chapter outline;
- terms and symbols actually used by the unit;
- relevant open issues;
- a short summary of the latest passed checkpoint.

Do not routinely include the complete conversation, build history, old review
logs, or full-book glossary. Load broader evidence only for final integration
or a concrete ambiguity.

Build the packet once before dispatch:

```bash
python3 scripts/build_context_capsule.py \
  --output-dir work/units/chapter-4-section-2 \
  --unit-id chapter-4-section-2 \
  --source-pdf work/source/chapter-4-section-2.pdf \
  --source-text work/source/chapter-4-section-2.txt \
  --terms GLOSSARY.md \
  --context work/source/chapter-4-section-2-context.md
```

The controller prepares the bounded PDF and the single auxiliary text
extraction. The packet builder deterministically keeps glossary rows whose
source terms occur in the unit, plus rows marked `book-wide`, `bookwide`, or
`全书`; it uses no model call. If the glossary is not a recognized Markdown
table, or contains multiple recognized tables, it is copied unchanged rather
than filtered speculatively. Matching selects candidate rows; the worker must
still obey each row's stated context and must not force a context-specific
translation onto a different sense. The worker
reads only the generated `CONTRACT.md`, `TASK.json`, and files named by that
task. It must not run another whole-unit text extraction or load the general
skill and reference files. The published PDF remains the authority;
`source/source.txt` is only a searchable aid.

The worker batch-reads the packet, writes the requested TeX and short structured
report in one translation pass, then stops. A Codex agent may require several
internal inference steps for file I/O; the invariant is one translation pass
without exploratory rereads or a self-review loop, not a fabricated one-call
claim.
Compilation, deterministic audit, coverage counts, hashes, and visual review
belong to the controller. Return only concrete errors to the worker for one
targeted repair pass; the repair receives only failed passages and immediate
context, never the complete unit or build logs. This is a context
boundary, not a reduction in the verification standard.

`PACKET_MANIFEST.json` records hashes and character counts. If
`context_smaller_than_source` is false, do not downshift merely because the
packet was generated: reduce the support material or keep the unit on Sol.

## Checkpoints And Minimal State

Checkpoint at a chapter, section, or complete derivation boundary. Do not split
a theorem from its proof, a figure from its caption, or an algorithm from its
explanation. Add one line to `PROGRESS.md`:

```text
scope | source pages/anchor | output file | status | output SHA-256 | next unit
```

For an active long-book run, maintain only `RUN_STATE.json` and
`PHASE_EVENTS.jsonl` in addition to the normal project files. A minimal state
record is:

```json
{
  "thread_id": "...",
  "pid": 0,
  "model": "gpt-5.6-sol",
  "reasoning_effort": "medium",
  "phase": "translate",
  "current_unit": "chapter-4-section-2",
  "last_passed_checkpoint": "chapter-4-section-1",
  "updated_at": "RFC3339 timestamp"
}
```

Append no more than one event per completed turn:

```json
{"ts":"...","thread_id":"...","turn_id":"...","phase":"translate","unit":"chapter-4-section-2","model":"gpt-5.6-terra","reasoning_effort":"medium","route_reason":"routine-prose-all-downshift-gates-passed","input_tokens":0,"cached_input_tokens":0,"output_tokens":0,"reasoning_output_tokens":0,"handoff_input_tokens":0,"status":"completed"}
```

Allowed phases are `translate`, `source_check`, `terminology`, `compile_fix`,
`review_language`, `review_math`, `review_visual`, `package`, `recovery`, and
`monitor`. Add `rework_reason` only when rework occurs. Mark unavailable usage
as unavailable; do not estimate it as zero.

Count each `turn_id` once. Report raw tokens as `input + output`, with cached
input and reasoning output shown separately rather than added again. Report
weighted credits separately using the official per-model rates applicable on
the run date. Do not assume cache sharing between models.

## Review And Stop Rules

Terra may perform a fresh-context language review of its ordinary unit, but it
cannot close mathematical issues or sign off the book. Sol medium reviews all
high-risk units and blindly samples at least one Terra unit in every chapter
that contains Terra work. Hide the producing model from the reviewer and
prioritize definitions, formula-adjacent prose, figures or tables, and chapter
conclusions.

The Sol reviewer performs one complete review pass over the authoritative
source and anonymized candidate, with the unit terms,
[routed-review-contract.md](routed-review-contract.md), and a compact list of
deterministic findings. It does not need the translation worker's conversation,
tool transcript, complete skill text, or successful compiler output. Provide
full logs only when diagnosing a concrete failure.

Return the current unit to Sol medium and record the rework when there is a
substantive formula, definition, symbol, reference, omission, structural, or
terminology error; when repair approaches retranslation; or when handoff and
cache loss erase the expected saving.

One severe sampled issue expands review to all Terra work in that chapter. Two
consecutive sampled units with the same serious failure, or two consecutive
units requiring substantive Sol retranslation, stop Terra routing for that
task class in the rest of the book.

## Recovery And Completion

Resume the same thread and model after an ordinary interruption. If the thread
is unavailable, give the replacement only the context capsule, last passed
checkpoint, and next unit. Confirm that only one writer is active and run one
local build before continuing. Do not re-review earlier passed units whose
content hash is unchanged.

The completion controller may create `BATCH_COMPLETE.json` only after the
named delivery evidence and deterministic gates are closed, including the
editable source, final PDF, glossary, issue log, progress, three review passes,
manifest, hashes, archive integrity, clean-directory rebuild, and final visual
inspection. Mechanical success is not proof of translation correctness.

## Adoption Gate

Before making Terra routine, compare all-Sol medium with routed Sol/Terra on
three eligible complete units and one high-risk Sol negative control. Use the
same evidence and standards, isolate outputs, and have a fresh Sol-medium
context review them blindly.

Adopt routing only when total weighted credits fall after handoff, blind review,
and rework; raw tokens do not materially rise; severe issues do not increase;
and Terra outputs do not pass only because Sol retranslates them. Otherwise
retain the context and checkpoint improvements and stop model downshifting.
