# THM-M-0605 proof phase: blocked at base 6bf9ee93

Item: `S56-M-0605-PROOF`

Recorded: `2026-07-16T04:52:48+08:00`

Base revision: `6bf9ee93a322e7d25cf9249226222095f95d1cff`

## Verdict

`blocked`. No placeholder-free Lean body for
`Stage1.THM_M_0605.ExoticSevenSphereExists` exists in the repository or the
pinned dependency closure. This run added the mandatory v2 dependency-reuse
ledger, but no proof body, closed obligation, or composition certificate. The
proof item stays `[ ]`, lifecycle stays `planned`, the root stays
`[H1, M4, R3]`, and audit and theorem completion remain false.

The dependency ledger reproduces the exact v2 context: there are no hard
parents, transitive hard ancestors, hard edges, or reuse hints. The only
shared group is the nonblocking weak co-mention of
`Mathlib.Geometry.Manifold.PoincareConjecture`. Its closest member,
`THM-M-0578`, has no root proof body; its composer also assumes the complete
exotic-sphere witness. It moreover freezes infinity-smooth regularity, while
the current THM-M-0605 target requires analytic regularity. The group is
therefore truthfully recorded as `not_applicable` and transfers no proof
credit.

The first master-closure failure is dependency legality: the assigned proof
node depends on `S56-M-0605-OBLIGATION_TREE`, whose state is still provisional
`[_]`, not accepted `[x]`. Independent of that cursor gate, statement fidelity
also fails. The frozen target requires `IsManifold (mathcal-R 7) omega`, while
the human smooth claim and actual pinned mathlib marker use infinity-smooth
regularity. Trust-zero probes prove the orders differ and establish only the
analytic-to-smooth direction; the converse fails.

The immediate mathematical root cut is `M0605-T-WITNESS`: one analytic
seven-manifold, a homeomorphism to the standard seven-sphere, and an `IsEmpty
Diffeomorph` certificate. The first absent construction is `M0605-C-BUNDLE`,
the selected Milnor 3-sphere bundle over the 4-sphere with its clutching and
characteristic data. Its total-space, homotopy-sphere, topological-recognition,
bounding-manifold, smooth-obstruction, standard-comparison,
nondiffeomorphism, and terminal-witness packages remain open.

The checked theorem `exoticSevenSphereExists_of_witness` merely pairs a full
witness already supplied as premises. The standard sphere is not a shortcut,
because its identity diffeomorphism contradicts the required `IsEmpty`
certificate. Pinned mathlib contains the nearby smooth signature only as
`proof_wanted exists_homeomorph_isEmpty_diffeomorph_sphere_seven`, which is
discarded during elaboration. A scoped search found no retained Milnor-sphere,
clutching, homotopy-sphere, Eells-Kuiper, or Kervaire-Milnor proof package
among 9,676 pinned-package Lean files.

## Validation

The exact structured command ledger is in the companion JSON. The target
manifest checks passed, the dependency ledger passed the repository's exact
validator, and both target structural checkers passed while reporting the
root open at M4. Fresh trust-zero checks elaborated the exact statement, the
conditional composer, the analytic-to-smooth implication, the regularity
mismatch, and the standard-sphere rejection. The expected smooth-to-analytic
negative check failed at instance synthesis. The composer uses only
`propext`, `Classical.choice`, and `Quot.sound`; the owned Lean surface contains
no prohibited proof device.

The repository-wide standard and v2 DAG validators were attempted but were
resource-starved by the concurrently saturated Stage1 host and yielded no
fresh result, so no pass is claimed for either. The existing pinned `.lake`
artifacts were reused read-only. No `lake update`, `lake build`, dependency
clone/fetch, network request, or `.lake` mutation occurred.

## Retry condition

First obtain master acceptance `[x]` for the obligation-tree prerequisite.
Then correct the statement/anchor regularity mismatch or supply a checked
equivalence justifying the stronger analytic target. Finally implement the
frozen Milnor construction and obstruction packages without placeholders, or
pin an immutable compatible proof-bearing declaration, and rerun all exact
type, trust, provenance, composition, and structural gates.

This is blocker evidence, not a proof receipt. It does not satisfy
`S56-M-0605-PROOF`, promote scheduler state, or support theorem completion.
Because the assigned phase is incomplete, `.stage1-worker-selftest.json`
remains absent.
