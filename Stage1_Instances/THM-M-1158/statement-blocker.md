# Exact-statement gate: blocked

Item: `S56-M-1158-STATEMENT`  
Theorem: `THM-M-1158`  
Base revision: `915e3cad7d9f0c51622da7a7ab548cdacd00db77`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository source record. The
entire mathematical content is the title `单层位势` (single-layer potential) and the phrase
`边界积分表示` (boundary integral representation), attributed only to "many mathematicians" in
the nineteenth century. No primary source, edition, theorem/page, displayed formula, or quantified
claim is identified. The intake dependency correctly freezes this ambiguity rather than selecting
a theorem family.

The missing choices change the proposition rather than merely its notation:

- the ambient dimension, domain, boundary orientation and regularity, and scalar field;
- the fundamental solution, sign and normalization, including the two-dimensional case;
- the density space, boundary measure, and integrability assumptions;
- whether the target is the definition of the potential, a representation formula for a PDE
  solution, harmonicity away from the boundary, a trace theorem, or a jump relation;
- the evaluation region, limiting convention, equality notion, regularity conclusion, and
  excluded singular or degenerate cases.

Those alternatives are inequivalent. In particular, a definition of a single-layer potential is
not itself the same claim as a boundary representation formula, while continuity, harmonicity,
and normal-derivative jump theorems require different hypotheses and conclusions. Selecting any
standard version would therefore broaden or substitute the assigned target.

Consequently the canonical human claim fails before minimal imports, fixed universes and binders,
an elaborated expression fingerprint, checked transports, or meaningful removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations can be established. No Lean
declaration, abstract proxy, assumed predicate, axiom, placeholder, or convenient special case was
introduced. The statement node remains open at `M4`; no statement or theorem completion is
claimed.

## Repository and mathlib boundary

Repository-wide discovery found only the same short catalogue metadata in
`Docs/researches/math_theorems.md` and `Docs/Stage0_Blueprint.md`, plus separate dossiers for the
double-layer potential and jump relations. Those neighboring targets cannot select this target's
claim. The pinned mathlib source contains no theorem-specific single-layer-potential or boundary-
integral API under the searched terminology. That negative search is discovery evidence only and
does not repair the missing source statement.

There is no applicable `lake env lean <target>.lean` check because the expression that such a file
would have to elaborate is precisely what the source fails to determine. Elaborating a freely
chosen abstract interface would be fake statement evidence, not a narrow validation of this
deliverable.

## Pinned environment and validation

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai). Existing canonical `.lake`
artifacts were read only; no update, build, clone, fetch, or dependency mutation was performed.

- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1158` | 0 | Rank 361, planned lifecycle, legacy artifacts unaccepted, theorem incomplete |
| repository `rg` search for the theorem ID, Chinese title and gloss, and English title | 0 | Found only underspecified catalogue metadata and neighboring target references; no exact source proposition |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | Produced the two hashes recorded above |
| pinned-mathlib `rg` search for single-layer potentials, layer potentials, boundary integrals, potential theory, and relevant fundamental solutions | 0 | Only unrelated Pell-equation uses of "fundamental solution" matched; no theorem-specific API was found |

## Retry condition

An accountable source reviewer must pin an immutable primary or authoritative scholarly source by
edition and exact theorem/page, then freeze the displayed formula, ambient dimension, domain and
boundary regularity, kernel normalization, density and measure, quantifier order, hypotheses,
evaluation region, conclusion, and boundary or singular cases. The review must also distinguish
this claim from the separately scheduled double-layer-potential and jump-relation targets and
record errata. A later statement worker can then encode the exact proposition, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile any credited
transports, and execute all four mutation classes.

The assigned phase is not genuinely self-tested to its completion gate. Therefore no
`.stage1-worker-selftest.json` is emitted.
