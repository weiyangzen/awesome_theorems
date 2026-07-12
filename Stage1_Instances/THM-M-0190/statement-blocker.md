# Exact-statement gate: blocked

Item: `S56-M-0190-STATEMENT`  
Theorem: `THM-M-0190`  
Base revision: `3320329db47d2d9804ae3322159af1f5125bbcf7`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. Its
only mathematical wording is "Christoffel problem" and "prescribed curvature problem for the
surface of a convex body." The intake correctly records that this does not select a proposition.
It supplies no primary-source theorem/page and does not distinguish the classical Christoffel
problem from the adjacent Minkowski problem at statement granularity.

The likely Christoffel family still contains materially different roots. A smooth
three-dimensional formulation can prescribe the sum or mean of principal radii as a function of
the outer normal, while a general convex-geometric formulation can prescribe a first area
measure. These choices require different domains, regularity and positivity assumptions,
compatibility conditions, normalizations, notions of solution, treatment of degenerate bodies,
and existence and uniqueness conclusions. In particular, uniqueness normally requires a
translation quotient. Selecting any one formulation from the short metadata would invent missing
mathematics or substitute a narrower theorem.

The historical Christoffel paper and the two Firey papers in the intake crosswalk are discovery
locators only. No immutable edition, exact theorem/page, incorporated definitions, errata
disposition, or independently accepted source mapping exists in the dossier. Consequently the
canonical human claim fails before ordered binders, minimal imports, an elaborated expression
fingerprint, checked transports, or meaningful removed-hypothesis, changed-domain, binder-scope,
and boundary mutations can be established. No proxy predicate, assumed curvature interface,
axiom, placeholder, weakened special case, or broadened statement was introduced. Machine state
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

Commands ran inside this worker clone. The canonical `.lake` link was read only; no update, build,
clone, fetch, or other dependency mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0190` | 0 | Rank 676, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| repository `rg` search for the theorem names, historical title, first area measure, and mean-radius wording | 0 | Found only underspecified metadata and this target's intake discovery records; no source-frozen proposition |
| pinned-mathlib `rg` search for the Christoffel problem, mean/principal radii, and first area measure | 1 | No matching theorem-specific API (`rg` exit 1 means no match) |

There is no applicable `lake env lean <target>.lean` validation because the required exact
expression does not exist. Elaborating a locally invented abstract interface would be fake
statement evidence rather than the assigned deliverable.

## Retry condition

An accountable source review must preserve and hash an immutable primary or authoritative modern
source, select and transcribe one exact existence-and-uniqueness theorem with all incorporated
definitions and assumptions, resolve errata, and independently approve its relationship to the
repository label. It must freeze dimension, convex-body category, prescribed datum and
normalization, compatibility and regularity conditions, translation equivalence, and degenerate
cases while explicitly separating the neighboring Minkowski problem. A later statement run can
then encode that same claim with real Lean definitions, minimize its pinned imports, fingerprint
the elaboration, compile credited transports, and run all four required mutation classes.

This is the first failed gate, not completion of the statement node or any later node. The assigned
phase is not genuinely self-tested to its completion gate, so no `.stage1-worker-selftest.json` is
emitted.
