# Statement-phase blocker

Item: `S56-M-0713-STATEMENT`  
Theorem: `THM-M-0713`  
Worker base revision: `136ebf643dcdcbc42cef34e415177189578060ef`

## Gate decision

The exact Lean 4 target cannot be elaborated truthfully from the accepted intake and repository
source record. The record gives only the name "Matiyasevich theorem" and the gloss "the negative
solution of Hilbert's tenth problem". It does not provide an immutable primary-source pinpoint,
ordered binders, definitions, hypotheses, or a conclusion. Stage0 explicitly leaves the exact
definitions and premises open.

At least three inequivalent propositions remain compatible with that metadata:

1. the final Matiyasevich step, that natural-number exponentiation has a Diophantine graph;
2. the MRDP characterization of computably enumerable sets as Diophantine sets;
3. the undecidability consequence for integer-polynomial solvability.

The neighboring target `THM-M-0714` separately names MRDP. A separate computer-science record also
names the undecidability consequence, but it is not the source authority for this theorem ID. Thus
selecting any of the three without a source decision and crosswalk would broaden or substitute the
target rather than elaborate the exact claim.

Pinned mathlib does contain a real partial anchor: `Mathlib.NumberTheory.Dioph` documents
`Dioph.pow_dioph` as "a version of Matiyasevic's theorem". The same module explicitly lists
"Finish the solution of Hilbert's tenth problem" as TODO. The existing `IntakeProbe.lean` therefore
was re-elaborated only to establish that the pinned environment and candidate APIs are available.
It is not a canonical target and receives no statement or proof credit.

Because no canonical proposition is selected, there is no sound expression to serialize or hash,
no alternate encoding to transport, and no meaningful removed-hypothesis, changed-domain,
changed-binder-scope, or boundary mutation suite. The rev-5.6 section 5.1 statement gate fails
before proof evidence may be inspected.

## Exact validation record

Validation date: `2026-07-12` (`Asia/Shanghai`). The existing canonical `.lake` artifacts were used
read-only. No update, build, dependency fetch, or clone was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets; ranks 1..1546; all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0713` | 0 | rank 752; planned; legacy artifacts unaccepted; theorem_complete false |
| `rg -n -C 4 'THM-M-0713\|Matiyasevich\|马季亚谢维奇\|希尔伯特第10' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md Docs -g '*.md'` | 0 | found only the ambiguous theorem gloss, distinct neighboring MRDP record, and distinct CS undecidability record; Stage0 exact definitions remain open |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0713/IntakeProbe.lean)` | 0 | `Poly`, `Dioph`, `DiophFn`, `Pell.matiyasevic`, `pell_dioph`, and `pow_dioph` elaborated; no canonical root asserted |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0713 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom found |

## Required unblocker and status boundary

The first unblocker is an immutable, independently inspected primary-source passage selecting one
exact proposition and fixing its definitions, domains, binder order, hypotheses, conclusion,
translation, and errata disposition. The selection must explicitly reconcile the adjacent MRDP
target and the separate undecidability record. Only then can the exact Lean expression be encoded
with minimal imports, serialized and fingerprinted, related encodings transported, and all four
required mutation classes executed.

This statement node remains `[ ]` and blocked at `M4`. The root remains `[H1, M4, R4]`, with
`audit_complete: false` and `theorem_complete: false`. No worker self-test manifest is emitted,
because the assigned statement deliverable did not pass its gate.
