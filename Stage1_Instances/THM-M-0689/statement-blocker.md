# Exact-statement gate: blocked

Item: `S56-M-0689-STATEMENT`  
Theorem: `THM-M-0689`  
Base revision: `6d9089613f4343925b2ff1ec1a221f0575a93b5f`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository record. The complete
mathematical wording for this target is the title `证明复杂性` ("proof complexity") and the gloss
`证明长度的下界` ("lower bounds on proof length"), attributed to Stephen Cook and dated 1971.
Stage0 marks the precise definitions, prerequisites, proof route, dependencies, axioms, and formal
artifacts as `待补充`. No primary-source edition, theorem number, page, or exact proposition is
selected.

This wording does not determine a theorem. At minimum it leaves all of the following open:

- the proof system, such as resolution, bounded-depth Frege, Frege, extended Frege, cutting
  planes, polynomial calculus, or an abstract Cook-Reckhow system;
- the tautology or contradiction family, or whether the claim is instead an existential
  worst-case result;
- the measure, such as lines, symbols, clauses, degree, width, or encoded bit length;
- the lower-bound function and whether the quantifier is pointwise, infinitely often, eventual,
  or worst-case;
- soundness, completeness, uniformity, constructibility, encoding, and small-index hypotheses.

These choices change the domains, ordered binders, hypotheses, conclusion, and boundary cases.
Choosing any one of them would substitute a more specific theorem for the catalog label. In
particular, the separately scheduled Haken pigeonhole lower bound and the later generic
`证明复杂性下界` entry cannot be imported into this target. The attribution and year also do not
identify a lower-bound theorem: they are compatible with historical framework material while the
catalog wording asserts an unspecified lower bound.

Consequently the rev-5.6 section 5.1 gate fails at exact human-claim identity. There is no
canonical expression whose imports can be minimized or whose kernel expression can be hashed, and
there are no sound removed-hypothesis, changed-domain, changed-binder-scope, or boundary mutations
to test. Introducing an abstract predicate or assuming a lower-bound relation would be a
placeholder rather than elaboration of the source claim. No Lean declaration, axiom, weakened
special case, or broadened target was added.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated to distinguish a working pinned environment from
the missing mathematical statement. Its generic encoding, list-length, eventual-filter, and
asymptotic APIs are possible ingredients only; they define neither a propositional proof system nor
a hard family or lower bound and receive no statement or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The `lean-toolchain` SHA-256 is
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`; the
`lake-manifest.json` SHA-256 is
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`. The pre-existing canonical
`.lake` symlink and artifacts were used read-only. No update, build, clone, fetch, or dependency
mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-12 (`Asia/Shanghai`).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0689` | 0 | rank 730, planned, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean version and commit recorded above |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake version recorded above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | produced the pinned mathlib revision recorded above |
| repository `rg` search for the theorem ID, Chinese and English labels, and lower-bound gloss | 0 | found only the underspecified metadata, intake dossier, distinct Haken target, and distinct later proof-complexity-lower-bound target; no exact proposition |
| pinned-mathlib `rg` search for proof complexity, Cook-Reckhow systems, Frege systems, propositional proof systems, and proof-length lower bounds | 1 | no matching proof-complexity API or theorem (`rg` exit 1 means no match) |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0689/IntakeProbe.lean)` | 0 | all six generic substrate checks elaborated; no canonical target asserted |
| `rg -n '\\b(sorry|admit)\\b|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0689 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom found |

## Retry condition and status boundary

An accountable reviewer must preserve and inspect an immutable primary source, select and
transcribe one exact proposition, audit its errata, and independently approve the mapping. The
selection must freeze the proof system, syntax, hard family, proof and formula encodings, size
measure, lower-bound rate, quantifier order, all assumptions, and degenerate cases, while explaining
its boundary from the separately scheduled Haken and later proof-complexity targets. A later
statement run can then encode that same claim, minimize imports, fingerprint its elaborated kernel
expression, check alternate transports, and run all four required mutation classes.

The statement node remains open and blocked at `M4`; the root remains `[H3, M4, R4]` with
`audit_complete: false` and `theorem_complete: false`. The assigned phase did not pass its
completion gate, so no `.stage1-worker-selftest.json` is emitted and no downstream-node credit is
claimed.
