# Exact-statement gate: blocked

Item: `S56-M-0671-STATEMENT`  
Theorem: `THM-M-0671`  
Base revision: `72e619798c0efb1ca66df0782a61d8eed273bc3d`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. The
record supplies only the title "model completeness", the year 1956, the attribution to Abraham
Robinson, and the gloss "conditions for a theory to be model complete". It supplies no primary
edition, theorem/page, exact wording, or assumptions. The accepted intake therefore freezes a
theorem family and explicitly leaves the source proposition open.

Several inequivalent propositions fit that record:

- the definition that every embedding between models of a theory is elementary;
- a semantic criterion involving existentially closed substructures or extensions;
- a syntactic Robinson test involving formulas equivalent modulo the theory to existential or
  universal formulas;
- a theorem that a particular theory is model complete.

These are not interchangeable encodings. Selecting among them changes the root proposition and
may change consistency, completeness, inductiveness, model-existence, parameter, formula-fragment,
embedding, and quantifier-order assumptions. Even after selecting a criterion, the record does not
fix whether theories are arbitrary sentence sets or deductively closed, whether structures are
nonempty, which direction of formula conversion is asserted, how parameters and free variables are
represented, or how inconsistent theories and theories without models are treated.

The intake names Robinson's 1956 *A Result on Consistency and its Application to the Theory of
Definition* only as an uninspected bibliographic lead. Promoting a familiar modern formulation
without selecting and inspecting an immutable primary-source theorem would invent the missing
mathematics. Encoding the definition alone would also substitute a definition for the requested
"conditions" theorem. A structure or hypothesis carrying the desired elementarity or formula
equivalence would be a forbidden assumed conclusion rather than statement evidence.

The phase consequently fails at exact human-claim identity, before ordered binders, minimal
imports, a canonical elaborated expression, expression fingerprint, checked transports, or the
required removed-hypothesis, changed-domain, binder-scope, and boundary mutations can exist. No
Lean declaration, axiom, placeholder, weakened special case, or broadened target was introduced.
Machine debt remains `M4`; statement acceptance and theorem completion are false.

## Pinned environment and narrow validation

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai). The existing canonical `.lake`
artifact was read only. No update, build, clone, fetch, or dependency mutation was performed.

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
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0671` | 0 | Rank 715, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| repository `rg` search for the Chinese title, "model completeness", and `modelComplete` spellings | 0 | Found only the underspecified source metadata, this intake dossier, exclusions in adjacent dossiers, and mathlib's unrelated complete-theory API |
| pinned-mathlib `rg` search for model-completeness and existential-closure spellings | 0 | Found no model-completeness criterion API; matches were only `completeTheory` in `Semantics.lean` and its use in `ElementaryMaps.lean` |
| `git diff --check -- Stage1_Instances/THM-M-0671` | 0 | No whitespace errors |

There is no applicable `lake env lean <target>.lean` command: no exact target exists. Elaborating a
chosen proxy would be false positive evidence rather than the assigned deliverable.

## Retry condition

An accountable source review must select an immutable primary edition and exact theorem/page,
inspect its definitions and errata, and freeze every theory, model, embedding, formula-fragment,
parameter, consistency/model-existence, and boundary convention above. It must distinguish the
selected criterion from the definition of model completeness and from theory-specific
applications. A later statement run can then crosswalk the source row by row, elaborate the exact
Lean expression with minimal pinned imports, fingerprint it and its environment, provide checked
transports, and run all four required mutation classes.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
