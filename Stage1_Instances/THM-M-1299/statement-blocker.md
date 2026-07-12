# Exact-statement gate: blocked

Item: `S56-M-1299-STATEMENT`  
Theorem: `THM-M-1299`  
Base revision: `bce57eae7d429ef0eaa638cf3a12aee8f59fe7c7`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. The
record supplies only the label "Besov spaces", the gloss "refinement of function spaces", the year
1959, and attribution to Oleg Besov. It supplies no primary-source publication, theorem/page,
definition, hypotheses, or conclusion. Its `已验证` value is untrusted discovery metadata, not a
source-statement or kernel receipt. The accepted intake dependency therefore deliberately leaves
the canonical claim unselected at `[H4, M4, R4]`.

"Besov spaces" names a parameterized family of spaces rather than one theorem. The metadata does
not determine any of the following mathematically material choices:

- the ambient domain (`R^n`, a torus, a bounded domain, or another space), dimension, and scalar
  field;
- homogeneous versus inhomogeneous spaces and, in the homogeneous case, the quotient convention;
- the smoothness and integrability indices `s`, `p`, and `q`, including finite and infinite
  endpoints;
- a difference-quotient, Littlewood-Paley, interpolation, approximation, or other definition and
  its normalization;
- whether the intended result is an embedding, extension, trace, interpolation identity,
  equivalent-norm characterization, or a different theorem;
- the exact quantifier order, domain regularity, constants, endpoint exclusions, and conclusion.

These choices yield inequivalent propositions. Selecting a convenient definition, proving
nonemptiness of an invented `BesovSpace`, or choosing an arbitrary embedding would substitute
mathematics for the missing source claim. Nearby records for Littlewood-Paley theory, Sobolev
interpolation, and Triebel-Lizorkin spaces are separately scheduled targets and cannot supply the
root by association.

Consequently this phase fails at canonical human-claim identity, before minimal imports, fixed
binders, an elaborated expression fingerprint, checked alternate-form transports, or meaningful
removed-hypothesis, changed-domain, binder-scope, and boundary mutations can exist. No Lean
declaration, placeholder, axiom, abstract interface, weakened special case, or broadened target was
introduced. Machine state remains `M4`; statement acceptance and theorem completion are false.

## Narrow validation evidence

Commands were run in this worker clone on 2026-07-12 (Asia/Shanghai). The canonical pinned `.lake`
artifacts were read only; no update, build, clone, or fetch command was used.

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
| `python3 scripts/stage1_target.py show THM-M-1299` | 0 | Rank 467, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision recorded above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | Produced the two hashes recorded above |
| repository `rg` search for `besov`, the Chinese title/gloss, and related names | 0 | Found only underspecified catalog metadata, related target dossiers, and noncanonical infrastructure notes; no source-frozen proposition for this target |
| pinned-mathlib `rg` search for Besov, Littlewood-Paley, Triebel-Lizorkin, dyadic-decomposition, and modulus-of-smoothness terms | 1 | No matching Besov API or theorem declaration (`rg` exit 1 means no match) |

There is no honest `lake env lean <target>.lean` check: the required exact expression does not
exist. Elaborating a fabricated generic proposition would be fake statement evidence rather than
the assigned deliverable.

## Retry condition

An accountable source review must select an immutable primary-source edition and exact
theorem/page, check relevant errata, and freeze the complete wording. It must resolve every domain,
space convention, definition/normalization, parameter range, hypothesis, constant, conclusion, and
endpoint listed above and crosswalk them row by row. A later statement run can then encode that
claim, minimize pinned imports, serialize and hash its elaborated expression, compile any credited
transports, and run the four required structural mutation classes.

First failed gate: exact source-statement identity. The assigned phase is not genuinely self-tested
to completion, so no `.stage1-worker-selftest.json` is emitted.
