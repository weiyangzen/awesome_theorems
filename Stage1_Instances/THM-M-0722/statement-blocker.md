# Exact-statement gate: blocked

Item: `S56-M-0722-STATEMENT`  
Theorem: `THM-M-0722`  
Base revision: `d19d83e12b57432e75cbb1c35f4577d5b0645cf9`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the accepted source record. The
repository gives only the title "Karp's 21 NP-complete problems" and the gloss "classic
NP-complete problems". Stage0 leaves the exact definitions, assumptions, proof path, axioms, and
machine artifact open. The intake identifies Karp's 1972 chapter and its collective displayed
claim, "All the problems on the following list are complete", but explicitly leaves the exact
inventory, counting convention, definitions, side conditions, and source review open.

Those omissions affect the proposition rather than merely its proof. A canonical target must fix
the source's language encoding, input-length measure, deterministic and nondeterministic machine
models, polynomial bound convention, polynomial reducibility relation, completeness definition,
and the concrete instance predicate and malformed/degenerate-input policy for every list entry.
The source headings and later conventional names are not a self-authenticating 21-element Lean
index. An arbitrary supplied family of 21 predicates would weaken the historical theorem, while a
single SAT, CLIQUE, coloring, or Hamiltonian result would substitute a different theorem.

Consequently there is no exact expression to fingerprint and no sound removed-hypothesis,
changed-domain, binder-scope, or boundary mutation suite. In particular, mathlib's
`ManyOneReducible` checks computable many-one reduction and cannot silently stand for Karp's
polynomial reduction. The first rev-5.6 statement gate therefore fails at exact source inventory
and encoding freeze. Machine state remains `M4`; no statement or proof credit is claimed.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated to distinguish a working pinned Lean environment
from the missing canonical proposition. Its imports expose `Language`, computable
`ManyOneReducible`, and representative finite-graph APIs. This is only substrate evidence, not the
21-component statement. No `sorry`, `admit`, or `axiom` occurs in the target's Lean source.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The canonical `.lake` artifacts were reused read-only;
no update, build, clone, or fetch was run.

## Validation evidence

Commands ran in this worker clone on `2026-07-12` (`Asia/Shanghai`).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets; ranks 1 through 1546; all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0722` | 0 | rank 759; planned; legacy artifacts unaccepted; theorem_complete false |
| `rg -n -C 12 'THM-M-0722\|Karp的21个\|经典的NP完全问题\|Reducibility among Combinatorial Problems' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md Stage1_Instances/THM-M-0722` | 0 | found only underspecified repository metadata and the intake's explicitly open source/encoding boundary |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean version and commit shown above |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake version shown above |
| `(cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json)` | 0 | hashes `651c8acc...b1d2` and `321626c8...5cb2` |
| `git -C "$(readlink -f Formalizations/Lean/.lake)/packages/mathlib" rev-parse HEAD` | 0 | pinned mathlib revision shown above |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0722/IntakeProbe.lean)` | 0 | six substrate declarations elaborated; no canonical statement asserted |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0722 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom found |

## Retry condition and status boundary

An accountable source reviewer must preserve and hash an immutable edition of Karp's chapter,
independently transcribe and approve the complete list and counting convention, and provide a
row-by-row record of definitions, assumptions, boundary cases, proof pages, and errata. The formal
encoding review must then freeze the models, sizes, polynomial bounds, reduction direction, and
all 21 concrete decision predicates. Only then can a statement worker choose minimal pinned
imports, elaborate and fingerprint that exact proposition, check transports, and execute all four
mutation classes.

This statement node remains `[ ]` and blocked. The root remains `[H1, M4, R4]`, with
`audit_complete: false` and `theorem_complete: false`. Because the assigned deliverable did not
pass its gate, no `.stage1-worker-selftest.json` is emitted.
