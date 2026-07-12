# Statement-phase blocker

Item: `S56-M-0728-STATEMENT`  
Theorem: `THM-M-0728`  
Worker base revision: `f12b1ccbda307337d488a2993eddbf883b722be6`

## Gate decision

The exact Lean 4 target cannot be elaborated truthfully from the accepted intake and repository
source record. The record supplies only `IP = PSPACE`, the gloss "interactive proofs equal
PSPACE", an attribution, and a discovery citation. It does not freeze the definitions incorporated
by that equality. The intake explicitly leaves the canonical expression null and the primary text
uninspected. Selecting definitions now would invent mathematics rather than elaborate the exact
source target.

In particular, all of the following materially change the proposition and remain unresolved:

1. the input alphabet, language encoding, input-length convention, and uniformity policy;
2. private-coin versus public-coin interaction, round and message bounds, verifier totality, and
   the representation of adaptive prover strategies;
3. the probability space and ordered quantifiers over inputs, provers, verifier coins, and
   polynomial bounds;
4. exact completeness and soundness thresholds, strict versus non-strict inequalities, small-input
   exceptions, and whether amplification is incorporated or a separate bridge;
5. the deterministic machine model, work-tape accounting, halting condition, and polynomial-space
   convention defining `PSPACE`;
6. equality of sets of languages versus two inclusions and the transports between alternative
   encodings.

These choices are robustly equivalent only after substantial theorems; they are not definitionally
interchangeable. Encoding a generic proposition parameterized by assumed predicates, defining both
classes to be equal, assuming either inclusion, or formalizing only one direction would be a
broadened, tautological, or substituted target forbidden by the assignment. Consequently there is
no canonical expression to fingerprint and no sound removed-hypothesis, changed-domain,
changed-scope, or boundary mutation suite. The exact-statement gate fails before proof search.

The existing `IntakeProbe.lean` was re-elaborated only to distinguish a working pinned Lean
environment from a missing mathematical specification. It checks generic language and
deterministic polynomial-time APIs; it is not an `IP = PSPACE` statement and receives no statement
or proof credit. A scoped search of pinned mathlib found no `PSPACE` or interactive-proof interface
to reuse.

## Exact validation record

Validation ran on `2026-07-12` (`Asia/Shanghai`) inside the worker clone. The canonical pinned
`.lake` artifacts were used read-only. No update, build, clone, or fetch command was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets; ranks 1..1546; all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0728` | 0 | rank 765; planned; legacy artifacts unaccepted; theorem_complete false |
| `sed -n '5356,5375p' Docs/researches/math_theorems.md` | 0 | only the short equality gloss, attribution, year, importance, and untrusted status occur |
| `sed -n '19884,19918p' Docs/Stage0_Blueprint.md` | 0 | exact definitions, assumptions, proof route, axioms, and formal artifacts are all open |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake 5.0.0-src+98dc76e |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `651c8a...1d2` and `321626...d81` |
| `rg -n -i '\\bPSPACE\\b|interactive[ -]proof|interactiveproof' Formalizations/Lean/.lake/packages/mathlib/Mathlib -g '*.lean'` | 1 | expected no-match exit; no such pinned mathlib source interface found |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0728/IntakeProbe.lean)` | 0 | generic `Language` and deterministic polynomial-time declarations elaborated; no canonical theorem asserted |

## Required unblocker and status boundary

The first unblocker is an immutable, independently inspected primary-source passage with its
incorporated definitions, assumptions, theorem location, edition relationship, and errata
disposition. An accountable source reviewer must map that passage to one fully specified class
equality and approve the mapping. Only then can this phase implement the missing protocol,
probability, and space-complexity interfaces, minimize imports, elaborate and fingerprint the exact
expression, check alternate transports, and run the required structural mutations.

This statement node remains `[ ]` and blocked at `M4`. The root remains `[H4, M4, R4]`, with
`audit_complete: false` and `theorem_complete: false`. No worker self-test manifest is emitted
because the assigned exact-statement deliverable did not pass its gate.
