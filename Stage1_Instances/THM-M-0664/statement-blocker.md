# Exact-statement gate: blocked

Item: `S56-M-0664-STATEMENT`  
Theorem: `THM-M-0664`  
Base revision: `9dd26b41d0fd448cfe71600d74accc729bff401b`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. Its
entire mathematical wording is "cell decomposition in o-minimal structures", attributed to Anand
Pillay and Charles Steinhorn in 1988. It supplies no primary-source title, edition, theorem number,
page, verbatim statement, or incorporated definitions. The accepted intake therefore identifies a
provisional theorem family, not a source-frozen proposition.

Several choices left open by that wording change the proposition rather than merely its Lean
encoding:

- decomposition of one definable set, a finite family of definable sets, or definable functions;
- fixed dimension, induction in dimension, or a theorem quantified over every dimension;
- named parameters, parameters from a set, or parameter-free definability;
- Cartesian powers represented by `Fin n -> M` or by an iterated product, including the `n = 0`
  convention;
- the recursive definition of cells, graph and strip cases, and finite or infinite endpoints;
- decomposition of all ambient space or only a definable subset;
- coverage, pairwise disjointness, compatibility, and continuity/preparation conclusions;
- density, endpoint, and order-expansion hypotheses on the underlying structure.

Selecting a familiar modern finite-family cylindrical-decomposition formulation would invent these
missing decisions. Selecting only the unary finite-points-and-intervals characterization, or an
arbitrary finite definable partition, would substitute a weaker theorem. Encoding o-minimality or
cell decomposition as an unconstrained predicate/structure field would assume the desired content
and be a forbidden placeholder.

Repository search found only the same underspecified catalogue metadata, this intake dossier, and
a legacy Pila-Wilkie discovery module which explicitly models o-minimality as an unproved predicate
slot. Pinned-mathlib search found definability and ordered-structure infrastructure but no named
o-minimality or cell-decomposition API. Neither result resolves the source statement. The intake's
mention of van den Dries's 1998 book is explicitly a candidate locator and has not been accepted as
the source behind the Pillay/Steinhorn 1988 row.

Consequently the statement phase fails at exact human-claim identity, before minimal imports, an
elaborated expression fingerprint, checked transports, or meaningful removed-hypothesis,
changed-domain, binder-scope, and boundary mutation tests can be established. Machine state remains
`M4`; statement acceptance, audit completion, and theorem completion are false. No Lean
declaration, axiom, `sorry`, assumed interface, weakened special case, or broadened theorem was
introduced.

## Pinned environment

- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

The existing untracked `Formalizations/Lean/.lake` link/artifact was used read-only. No update,
build, clone, fetch, or dependency mutation was performed.

## Narrow validation evidence

Commands ran inside this worker clone.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0664` | 0 | rank 708, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | produced the pinned mathlib revision recorded above |
| repository `rg` for the theorem ID, Chinese/English labels, Pillay, Steinhorn, o-minimality, and cell decomposition | 0 | found only underspecified metadata, the intake dossier, and the explicit legacy missing-API boundary; no exact proposition |
| pinned-mathlib `rg` for o-minimality and cell decomposition | 1 for theorem-specific terms | no named o-minimality or cell-decomposition API; generic uses of the word `minimal` are unrelated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0664/IntakeProbe.lean` | 0 | generic language, structure, definability, order, interval, finite-family, and disjointness ingredients elaborate; this is not target elaboration |

There is no applicable `lake env lean <canonical-statement>.lean` validation because the exact
proposition has not been identified. Manufacturing an abstract statement merely to obtain a
successful elaboration would be fake evidence.

## Retry condition

An accountable source reviewer must preserve an immutable primary-source edition, resolve the
Pillay/Steinhorn/year attribution, select and transcribe the exact numbered theorem with page and
incorporated definitions, dispose of errata, and independently approve the crosswalk. That review
must freeze the set/function variant, order assumptions, parameter convention, tuple and cell
encodings, graph/strip and infinity conventions, compatibility conditions, quantifier order, and
all degenerate cases. A later statement run can then implement that same proposition, minimize its
pinned imports, serialize and hash the elaborated expression, compile checked transports, and run
the four required mutation classes.

This records the first failed gate and does not complete this node or any downstream node. The
assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
