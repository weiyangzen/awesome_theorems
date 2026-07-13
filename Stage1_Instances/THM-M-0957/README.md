# THM-M-0957 rev-5.6 dossier

This directory is the fail-closed `planned` intake dossier for Behrend's construction. The
repository supplies only the gloss "large sets without three-term arithmetic progressions,"
attributes it to Felix Behrend in 1946, and labels it verified. Under rev-5.6 that label is
untrusted inventory metadata, not source or proof evidence.

The original two-page paper was inspected through NLM/PMC scans. It defines `v(N)` as the maximum
cardinality of a subset of the nonnegative integers at most `N` containing no three distinct terms
`A, A', A''` with `A + A' = 2 A''`. For every positive epsilon and sufficiently large `N`, it
derives

`v(N) > N^(1 - (2 * sqrt (2 * log 2) + epsilon) / sqrt (log N))`.

This is a strong primary-source lead, but not an accepted `H0` packet: the remote scan was not
admitted as an immutable repository artifact, the formula has not received independent
transcription review, and no correction or errata audit is recorded. The paper's inclusive
`{0, ..., N}` convention also differs from mathlib's `Finset.range N` convention.

Pinned mathlib contains the proof-bearing module
`Mathlib.Combinatorics.Additive.AP.Three.Behrend`. `IntakeProbe.lean` checks its 3AP predicate,
extremal-set specification, construction lemmas, and terminal bound
`Behrend.roth_lower_bound`. The terminal declaration gives an explicit all-`N` lower bound for
`rothNumberNat N`, but intake does not claim exact statement identity, audit its terminal body or
axioms, or promote it to `M0-W`.

The statement phase subsequently froze the exact historical inclusive-interval target in
`Statement.lean`, and the anchor audit classified the pinned construction as a credible partial
family while excluding the fixed constant-four terminal from the exact root route. Both remain
provisional pending dependency-ordered master acceptance.

## Obligation-tree result

Registry version 1 freezes 45 canonical architecture records, including 28 required machine
obligations and non-machine overlays, with denominator
`84f7eaea7de3659e4324dc64f7849fde4024dd057d4d320c879b0b59dd692a63`. The proof graph uses the
single pinned `Behrend.bound_aux` bridge and isolates twelve unimplemented mathematical leaves
after a second split of the high-risk analytic packages. Each unimplemented leaf has an ordered
local proof plan, but its proof-budget status remains literally `unchecked`. The construction and
inclusive-index leaves are checked candidates, not accepted closure. The visible sphere and digit
internals are informational refinements of the same imported terminal body, not duplicate proof
credit.

`typed-graphs.json` separates proof, refinement, provenance, evidence, trust, documentation, and
workflow edges. `ObligationTree.lean` checks twelve exact child-to-parent composition certificates,
including direct `ExactAssembly`-to-root composition, plus the pinned construction and
inclusive-index adapters. The composed harness checks identity with the actual canonical statement.
These are conditional architecture checks only. The accepted
obligation set remains empty, the root stays `[H1, M3, R3]`, and `task-dag.json` remains open. No
H0, accepted M0, R0, audit completion, theorem completion, release, or master acceptance is claimed.
Only the root fingerprint is a statement-phase elaborated-expression hash. The other registry
fingerprints are explicitly planned architecture identities; proof-phase acceptance must replace
or independently bind them before any M0 claim.
