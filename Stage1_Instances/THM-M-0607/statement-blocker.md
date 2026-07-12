# Exact-statement gate: blocked

Item: `S56-M-0607-STATEMENT`  
Theorem: `THM-M-0607`  
Base revision: `502a74572b018a38dfc7a0f6160f4a2be221fdcf`

## Decision

The repository does not supply an exact mathematical proposition that can be truthfully
elaborated. Its complete claim is the topic fragment `拓扑流形的光滑结构` ("smooth structures on
topological manifolds"). It does not fix:

- the dimension or whether dimension four is included;
- the Hausdorff, countability, boundary, corners, or compactness conventions;
- the model space and topological-manifold definition;
- whether a PL structure, triangulation, stable lift, or obstruction-vanishing premise is assumed;
- the precise compatibility relation between the original topology/atlas and the requested smooth
  atlas; or
- whether the conclusion is existence, uniqueness up to diffeomorphism, or a classification.

These omissions are mathematically decisive. An unrestricted universal reading is false because
topological manifolds need not be smoothable. Restricting to dimensions at most three, assuming a
PL structure, or adding high-dimensional smoothing-obstruction hypotheses would select a different
theorem without source authority. The intake therefore correctly leaves `canonical_statement`
unset and records `[H4, M4, R4]`.

The first failed gate is canonical human-claim identity. Without it there is no exact Lean
expression, minimal import set, expression fingerprint, checked alternate encoding, or meaningful
removed-hypothesis/domain/binder-scope/boundary mutation suite. The assigned statement phase is not
complete.

## Legacy Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_254.lean` was inspected only as unaccepted legacy
discovery material. Its `StatementShape` asks for a `SmoothStructurePackage` after the caller
supplies a `SmoothabilityHypotheses` package. The low-dimensional package itself contains an
arbitrary proposition named `lowDimensionalSmoothingInput` and its proof; the high-dimensional
package similarly receives obstruction APIs and vanishing conditions as caller-provided data.
Thus this is a conditional interface describing desired inputs and output, not a formalization of
an identified source theorem establishing those inputs.

The legacy module also deliberately chooses a disjunction of dimensions at most three and
dimensions at least five, excludes dimension four, and introduces its own atlas compatibility
predicate. None of those choices is determined by the repository's source fragment. Its successful
elaboration therefore receives no rev-5.6 exact-statement credit, and its nine direct mathlib
imports cannot establish minimal imports for an unidentified target.

## Required unblock

An accountable source reviewer must select a stable primary source and record its edition,
theorem/page, exact wording, hypotheses, and conventions. In particular, the review must freeze the
dimension regime, manifold and boundary model, separation/countability assumptions, smoothability
premises, compatibility predicate, and exact conclusion. A later statement worker can then encode
that proposition without substitution, minimize pinned imports, print and hash its elaborated
expression, check transports, and run the required mutations.

## Narrow validation evidence

Commands ran from this worker clone on 2026-07-12. Lean commands ran from `Formalizations/Lean`
against the existing pinned Lake environment. No dependency update, fetch, or build was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0607` | 0 | rank 254, planned, legacy artifacts unaccepted, theorem incomplete |
| `lake env lean AwesomeTheorems/Stage1/S1_M_254.lean` | 0 | legacy conditional boundary elaborated and printed its audit probes; this is discovery evidence only |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C .lake/packages/mathlib rev-parse HEAD` | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum lean-toolchain lake-manifest.json` | 0 | `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` and `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` |

Known failures are exact claim identity, canonical target elaboration, import minimization,
expression fingerprinting, transports, and mutation tests. No statement-node receipt, audit or
theorem completion, or downstream-node credit is claimed. Because the assigned deliverable is not
genuinely self-tested as complete, no worker self-test manifest is emitted.
