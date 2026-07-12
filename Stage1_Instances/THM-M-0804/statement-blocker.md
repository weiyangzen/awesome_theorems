# THM-M-0804 statement-phase blocker

## Attempted item

- Item: `S56-M-0804-STATEMENT`
- Base revision: `8f8873f36acbc62e9b41b932a8bb65bf355c8ccf`
- Requested deliverable: elaborate the exact Lean 4 target with minimal pinned imports
- Verdict: `blocked`; no canonical Lean declaration or expression was created

## First failed gate

The exact-statement identity gate fails before Lean elaboration. The complete repository source
record is the title `核心模型` ("core model"), the attribution "Ronald Jensen/John Steel", the
period "1990s", and the phrase `大基数的内模型` ("an inner model for large cardinals"). It has no
publication, theorem number, page, ambient theory, definition of the core model, large-cardinal
boundary, hypotheses, or conclusion. Stage0 explicitly leaves definitions, assumptions,
equivalent formulations, axioms, proof process, and machine artifacts unresolved.

These omissions do not leave a merely syntactic choice. Existence, iterability, comparison,
universality, and covering are different propositions, while Jensen-style and extender core
models have different definitions and consistency-strength boundaries. Therefore there is no
exact human claim from which the ordered Lean binders and result can be truthfully derived.

Creating a predicate named `CoreModel`, postulating its properties, selecting a theorem from the
literature without a source crosswalk, or replacing the entry with a generic theorem about
`ZFSet` would broaden or substitute the target. Those actions are prohibited by the rev-5.6
statement gate. The existing `IntakeProbe.lean` checks only the pinned foundational ZFC API and is
not a canonical target.

## Gate consequences

The following required statement fields remain unavailable rather than guessed:

| Field | Status |
|---|---|
| canonical human statement | absent from repository sources |
| domain, universes, and ordered quantifiers | cannot be derived |
| hypotheses and excluded boundary cases | cannot be derived |
| conclusion | cannot be derived |
| minimal Lean imports | cannot be selected before the target is known |
| elaborated expression and fingerprint | unavailable because no exact expression exists |
| alternate encodings and checked transports | unavailable |
| mutation tests | impossible without a canonical expression |

Consequently `S56-M-0804-STATEMENT` is not self-tested and no
`.stage1-worker-selftest.json` is emitted. The root remains `[H3, M4, R4]`; this report supplies no
statement, proof, audit-completion, or theorem-completion credit.

## Validation evidence

Executed from the worker automation clone on 2026-07-12 (Asia/Shanghai):

| Command | Exact result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | exit 0; `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0804` | exit 0; rank 807, `planned`, `L0`, `rework_required: true`, `legacy_artifacts_accepted: false`, `theorem_complete: false` |
| `rg -n -C 6 '核心模型|THM-M-0804' Docs/researches Docs/Stage0_Blueprint.md Docs/Stage1_Targets_rev-5.6.json` | exit 0; found only the metadata above and Stage0's unresolved fields; no exact theorem statement |

`lake env lean` was deliberately not run against a fabricated statement: parser or elaborator
success for an invented `Prop` would not validate statement identity. No dependency update,
download, clone, fetch, or `.lake` mutation was performed.

## Retry condition

Retry this item only after an independently inspected, immutable primary-source passage is added
to the dossier with publication metadata, theorem/page, exact core-model version, ambient
foundation, all hypotheses (including the large-cardinal boundary and iterability conventions),
and the precise conclusion. The statement phase can then encode that passage, select minimal
pinned imports, elaborate and fingerprint the expression, and perform the four required mutation
tests.
