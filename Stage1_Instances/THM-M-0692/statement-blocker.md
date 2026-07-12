# Exact-statement gate: blocked

Item: `S56-M-0692-STATEMENT`  
Theorem: `THM-M-0692`  
Base revision: `6d9089613f4343925b2ff1ec1a221f0575a93b5f`

## Decision

The exact Lean 4 target cannot be truthfully selected or elaborated from the repository record.
The complete catalogue wording is only `相继式演算中的切割消去` ("cut elimination in sequent
calculus"), attributed to Gerhard Gentzen and dated 1934. It gives no primary work, theorem or
page, calculus, language, rules, or precise elimination conclusion. The intake therefore correctly
leaves the canonical claim and formal target open at `M4`.

This label denotes materially different metatheorems. A statement must at least choose classical
`LK` or intuitionistic `LJ`, propositional or first-order syntax, one- or two-sided sequents,
list/multiset/set contexts, the structural and logical rules (including equality and eigenvariable
conditions), and whether the result asserts cut admissibility, existence of a cut-free derivation
of the same end-sequent, an explicit normalization function, or a complexity bound. These choices
change the domains, binders, hypotheses, conclusion, and boundary cases. Selecting a convenient
variant would broaden or substitute the unidentified source theorem and violate sections 5 and 5.1
of the rev-5.6 standard.

The intake names Gentzen's *Untersuchungen uber das logische Schliessen. I and II* (1935) only as a
discovery candidate. This dossier has no accepted immutable copy, content hash, pinpoint Hauptsatz
passage, exact `LK`/`LJ` crosswalk, errata audit, or independent source review. Consequently there
is no canonical human proposition from which to freeze ordered Lean binders, a normalized kernel
expression, alternate-form transports, or meaningful removed-hypothesis, changed-domain,
binder-scope, and boundary mutations.

## Nearby artifacts do not identify the target

A scoped search found no cut-elimination or sequent-calculus declaration in pinned mathlib. The
existing `IntakeProbe.lean` elaborates only `List`, `Multiset`, `WellFounded`, and
`WellFounded.fix`; these are possible encoding ingredients, not a calculus or theorem.

The historical repository file
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_298.lean` also elaborates, but cannot be reused as
the target. It defines a small natural-deduction kernel with no cut constructor. Its theorem
`ProofCalculus.Derivation.cutFree` merely proves that derivations in this no-cut datatype satisfy a
recursive `CutFree` predicate. The file explicitly says that no separate sequent-calculus
cut-elimination theorem has been proved and that such a theorem remains formalization debt. Using
this construction would replace cut elimination with a tautological invariant of a calculus in
which cut cannot occur.

## Pinned environment

Commands ran in the worker automation clone on 2026-07-12. The existing `.lake` artifacts were
used read-only; no update, build, clone, or fetch was performed.

- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Validation evidence

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0692` | 0 | rank 733, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | pinned Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | pinned Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | produced the pinned mathlib revision recorded above |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0692/IntakeProbe.lean` | 0 | all four generic API checks elaborated; no target credit |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_298.lean` | 0 | historical no-cut natural-deduction artifact elaborated; its own output records the sequent-calculus theorem as debt |
| `rg -n -i 'cut[ -]?elimin\|cutfree\|cut_free\|Hauptsatz\|sequent calculus\|sequentCalculus' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no matching pinned-mathlib source occurrence |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0692 -g '*.lean'` | 1 | expected no-match result; no prohibited placeholder or axiom in target Lean files |

## Gate result and retry condition

First failed gate: exact canonical-claim identity, before Lean target elaboration. Machine debt
remains `M4`. No expression hash, mutation certificate, statement receipt, proof credit, audit
completion, or theorem completion is claimed.

Retry requires an accountable reviewer to preserve and hash an immutable primary source, pinpoint
and transcribe one exact theorem, audit its corrections, and independently approve a crosswalk that
fixes the calculus, syntax, contexts, complete rule set, side conditions, binders, conclusion, and
degenerate cases. A later statement run can then encode that exact proposition, minimize pinned
imports, serialize the elaborated expression and environment, and execute all four required
mutation classes.

The assigned statement phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
