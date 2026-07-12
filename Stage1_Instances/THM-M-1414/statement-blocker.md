# Exact-statement gate: blocked

Item: `S56-M-1414-STATEMENT`

Theorem: `THM-M-1414`

Base revision: `508f92b22d15ce42276877b26d34b9da3cac695c` (tree
`765daac67cdaffd2b797474b4c1a3d12f4f99933`).

## Decision

The exact Lean 4 target cannot yet be truthfully elaborated. The accepted dependency is only a
provisional worker intake, not a master-accepted node, and that intake deliberately leaves both the
canonical mathematical statement and formal target null. More importantly, the repository record
fixes only Stephen Smale, 1967, and the gloss "decomposition of Axiom A systems." It does not say
which of two materially different spectral-decomposition theorems in the cited paper is intended.

Smale's theorem (6.2), printed page 777, is explicitly titled "Spectral decomposition of
diffeomorphisms." For a compact-manifold diffeomorphism satisfying Axiom A, it uniquely decomposes
the nonwandering set into finitely many disjoint, closed, invariant, indecomposable pieces on which
the map is topologically transitive. Part II theorem (5.2), printed page 803, instead concerns a
continuous-time flow satisfying Axiom A'. Its premise separately treats hyperbolic fixed points and
the closure of closed orbits, and its conclusion concerns flow-invariant pieces. These are different
claims, not alternate Lean encodings joined by an evident checked transport.

The title of theorem (6.2) makes the diffeomorphism result the leading candidate, but selecting it
without the source review required by the accepted intake would replace unresolved repository scope
with a worker inference. Even after variant selection, the source-to-Lean mapping still needs
reviewed decisions about the manifold and diffeomorphism category, the nonwandering-set and Axiom A
definitions, the hyperbolic splitting, the meaning of indecomposable, topological transitivity,
finite-family representation, uniqueness up to reindexing or as a finite set, and empty or singleton
boundary cases. Pinned mathlib exposes generic ingredients but no source-faithful Axiom A or
nonwandering interface that silently resolves these choices.

Consequently there is no canonical expression on which to establish a minimal import set,
serialized kernel-expression fingerprint, credited alternate transport, or meaningful removed-
hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations. Adding an abstract
predicate for the unavailable notions, assuming the desired decomposition as structure data, or
choosing the more convenient theorem would be a placeholder or substituted target. No such Lean
declaration was added. The first failed hard gate is exact source-statement identity, so the
statement node remains unfinished at `M4`.

## Pinned Lean boundary

The intake's `IntakeProbe.lean` imports `Mathlib.Dynamics.Flow`,
`Mathlib.Dynamics.PeriodicPts.Defs`, and `Mathlib.Dynamics.Transitive`. In the pinned environment it
re-elaborates only generic `IsInvariant`, periodic-point, density, action-transitivity, and `Flow`
interfaces. This is the narrowest real Lean validation available without inventing the target. It
states no spectral-decomposition theorem, and its imports are not claimed minimal for an unknown
canonical expression.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The `lean-toolchain`, `lake-manifest.json`, and probe
SHA-256 values are respectively `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`,
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`, and
`f4afefea7651ef4d61ee967e62e51287545b71e656f565ce43e0644ed4c32de6`.

The automation-provided `Formalizations/Lean/.lake` link existed before this phase, points to the
canonical checkout's pinned artifacts, and was used read-only. No `lake update`, `lake build`,
dependency clone/fetch, or other `.lake` mutation was run.

## Validation evidence

Commands ran from this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1414` | 0 | rank 913, planned, legacy artifacts unaccepted, theorem incomplete |
| `git status --short && git rev-parse HEAD && git rev-parse HEAD^{tree}` | 0 | base revision and tree above; only the pre-existing untracked `.lake` link was present before this phase |
| `sha256sum /tmp/smale1967.pdf` and `pdftotext -layout /tmp/smale1967.pdf -` with bounded theorem searches | 0 | independently rechecked the intake's PDF hash and the incompatible theorem (6.2) and Part II theorem (5.2) texts; the temporary source copy is not delivered |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Stage1_Instances/THM-M-1414/IntakeProbe.lean` | 0 | hashes agree with the environment fingerprint above |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1414/IntakeProbe.lean` | 0 | eight generic candidate interfaces elaborated; no target theorem was stated |
| bounded exact-topic search under pinned `Mathlib/Dynamics` | 1 | expected no-match result for spectral decomposition, Axiom A, nonwandering, hyperbolic splitting, basic components, and dynamical indecomposability; not an anchor audit |

## Retry condition and status boundary

The integration lane must first accept the intake dependency. An accountable source reviewer must
then select theorem (6.2) or Part II theorem (5.2), preserve the immutable source and pinpoint
crosswalk, inspect incorporated definitions, cited source [117], and errata, and independently
approve the exact variant and translation. The selection must freeze every domain, ordered binder,
hypothesis, conclusion, uniqueness convention, transitivity/indecomposability meaning, and boundary
case listed above. A later statement worker can then encode that same claim using real definitions,
minimize its pinned imports, serialize and hash the expression and environment, compile every
credited transport, and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
later node. The root remains `[H1, M4, R3]`, with `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the phase is not genuinely
self-tested to its completion gate, no `.stage1-worker-selftest.json` is emitted and no receipt or
master acceptance is claimed.
