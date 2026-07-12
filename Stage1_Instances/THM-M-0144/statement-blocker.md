# Exact-statement gate: blocked

Item: `S56-M-0144-STATEMENT`  
Theorem: `THM-M-0144`  
Base revision: `12c908b3643c2473ee5e87f188ece1d3d8081640`

## Decision

No exact Lean 4 target can be truthfully elaborated from the repository record. The entire
theorem-specific record is the Chinese label "Manin correspondence" (`曼宁对应`), Yuri Manin, the
year 1974, and the gloss "formal groups and cohomology theories" (`形式群与上同调理论`). It gives no
publication, theorem/page, wording, hypotheses, or definition of "correspondence". The intake
therefore correctly freezes only a discovery boundary and records the canonical claim as
unresolved.

The gloss does not select one proposition. In particular, it leaves open:

- whether the formal object is a formal group or a one-dimensional commutative formal group law,
  and over which coefficient ring;
- whether the cohomology object is an axiomatized generalized theory, a multiplicative theory, a
  represented ring spectrum, or a complex-oriented theory;
- the grading, orientation, coordinate, and strict versus non-strict isomorphism conventions;
- whether "correspondence" asserts only the construction of a formal group law from an
  orientation, a functorial association, a classification/equivalence, or a converse realization;
- the exact quantifier order, hypotheses, conclusion, and treatment of degenerate coefficient
  rings or changes of coordinate.

These alternatives have materially different domains and conclusions. Choosing the standard
complex-orientation construction, Quillen's theorem, a Lazard-ring classification, or a realization
theorem would invent or substitute mathematics. An abstract structure carrying an assumed
`Corresponds` proposition would likewise be fake statement evidence.

Consequently the canonical human claim fails before minimal imports can be determined. There is no
honest declaration/expression to elaborate or serialize, no expression fingerprint, no alternate
encoding to transport, and no meaningful removed-hypothesis, changed-domain, binder-scope, or
boundary mutation to run. No Lean file, `sorry`, axiom, proxy predicate, weakened special case, or
broadened target was introduced. Machine state remains `M4`; statement acceptance, audit
completion, and theorem completion are false.

## Pinned environment and validation

Commands ran inside this worker clone on 2026-07-12 (Asia/Shanghai). The existing canonical
`.lake` artifacts were read only; no update, build, clone, or fetch command was used.

- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0144` | 0 | Rank 319, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| repository `rg` search for `曼宁对应`, `Manin correspondence`, and the formal-groups/cohomology gloss | 0 | Found only the sparse inventory metadata and this intake dossier; no source-frozen proposition or theorem-specific Lean artifact |
| pinned-mathlib `rg` search for Manin correspondence, formal groups with cohomology theories, and complex orientations with formal groups | 1 | No matching theorem-specific source declaration (`rg` exit 1 means no match) |

There is no applicable `lake env lean <target>.lean` check because an exact target does not exist.
Elaborating a nearby formal-group theorem or an assumed correspondence interface would not validate
the assigned statement.

## Retry condition

An accountable source review must identify an immutable primary-source edition and exact
theorem/page, check attribution and the meaning of the 1974 date, dispose of errata and translation
issues, and freeze every formal-group, cohomology-theory, orientation, coefficient, coordinate,
isomorphism, functoriality, and converse/realization choice above. It must also distinguish the
selected claim from Quillen's and Lazard's nearby results. A later statement run can then encode the
source-faithful proposition, minimize pinned imports, fingerprint its elaboration, compile checked
transports, and run all four required mutation classes.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
