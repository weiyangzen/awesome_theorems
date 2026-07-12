# Exact-statement gate: blocked

Item: `S56-M-0460-STATEMENT`  
Theorem: `THM-M-0460`  
Base revision: `6f53a31f8e3774a09182794cbac7edc5c7a286df`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. The
record contains only the title "Zhang equidistribution theorem", the date 1995, and the gloss
"equidistribution of points of small height". It gives no primary-source theorem/page or exact
wording. The intake correctly treats Shou-Wu Zhang's *Small points and adelic metrics* as a
discovery candidate only, not as a selected and inspected statement.

Those words describe a family of inequivalent arithmetic-geometric theorems. They do not fix:

- the number field, variety, dimension, projectivity, or geometric regularity assumptions;
- the ample line bundle and admissible/semipositive adelic metric hypotheses;
- the height normalization and whether the limit is zero, an essential minimum, or another bound;
- the definition of a generic sequence and its quantifier order;
- the places covered and the archimedean or non-archimedean analytic space;
- the canonical local measure, its normalization, and orbit multiplicities;
- the weak-convergence formulation and its test-function/topology conventions.

These choices change the proposition, including its domains, binders, hypotheses, and conclusion.
Selecting a general adelic-variety statement, an abelian-variety theorem, a curve case, or an
abstract measure-convergence proxy would invent or substitute mathematics. The nearby repository
records also point to later equidistribution and Bogomolov sources, reinforcing that the short
label and year do not uniquely select a root theorem.

Consequently the canonical human claim fails before minimal imports, an elaborated expression
fingerprint, checked transports, or meaningful removed-hypothesis, changed-domain, binder-scope,
and boundary mutations can be established. No Lean declaration, assumed convergence field,
placeholder, axiom, weakened special case, or broadened target was introduced. Machine state
remains `M4`; statement acceptance and theorem completion are false.

## Pinned environment and search

- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

Commands ran inside this worker clone. The existing `.lake` artifacts were read only; no update,
build, clone, or fetch command was used.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0460` | 0 | Rank 308, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| repository `rg` search for the title, English gloss, and candidate paper | 0 | Found only underspecified metadata, the uninspected candidate citation, and related but separately owned theorem dossiers; no source-frozen proposition for this target |
| pinned-mathlib `rg` search for adelic metrics, small points, height equidistribution, essential minima, Berkovich spaces, and orbit measures | 1 | No matching theorem-specific arithmetic-equidistribution API (`rg` exit 1 means no match) |

There is no applicable `lake env lean <target>.lean` validation: an exact expression does not
exist. Elaborating an abstract interface that assumes the desired convergence would be fake
statement evidence, not the assigned deliverable.

## Retry condition

An accountable source review must select an immutable primary-source edition and exact
theorem/page, dispose of errata, and freeze every variety, metric, height, genericity, place,
analytic-space, orbit-measure, and convergence convention listed above. It must also explain the
boundary with the separately scheduled small-height, general equidistribution, and Bogomolov
targets. A later statement run can then produce the exact Lean expression, minimize its pinned
imports, fingerprint the elaboration, crosswalk the source row by row, and run structural mutation
tests.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
