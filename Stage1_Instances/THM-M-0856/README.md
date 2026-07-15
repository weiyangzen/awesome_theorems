# THM-M-0856 rev-5.6 dossier

This directory is the fail-closed `planned` dossier for `THM-M-0856`, the repository's
`Tutte定理` (Tutte theorem). The catalog gives William Tutte, 1947, and only the gloss
`完美匹配存在的条件` (a condition for the existence of a perfect matching). Its `已验证`
field is untrusted metadata and supplies no source or proof credit.

## Intake result

The name, date, and gloss strongly identify Tutte's 1-factor theorem for finite graphs: a finite
graph has a perfect matching exactly when deleting every vertex subset `U` leaves at most `|U|`
connected components of odd order. The leading primary-source identity is W. T. Tutte, *The
Factorization of Linear Graphs*, Journal of the London Mathematical Society s1-22(2) (1947),
107-111, DOI `10.1112/jlms/s1-22.2.107`. Crossref and OpenAlex metadata confirm that identity, but
no full primary text, exact theorem locator, incorporated definitions, correction history, or
independent source review is admitted. The source mapping therefore remains `H1`, not `H0`.

## Formal boundary

Pinned mathlib contains a direct proof-bearing candidate in
`Mathlib.Combinatorics.SimpleGraph.Tutte`: `SimpleGraph.tutte` states that a finite simple graph has
a perfect matching if and only if it has no `IsTutteViolator`. The violator predicate unfolds to
strictly more odd connected components after deleting `U` than vertices in `U`. `IntakeProbe.lean`
checks these exact interfaces and records the candidate axiom report. This is unusually strong
intake discovery, but statement identity, minimal-import and mutation gates, terminal-body
provenance, and master acceptance belong to later ordered phases. The candidate is classified
provisionally as `M3`, not credited as `M0-W`.

The intake's provisional vector is `[H1, M3, R4]`. Its historical receipt supplies no canonical
Lean statement, accepted proof state, H0, M0, R0, audit completion, theorem completion, accepted
receipt, or master acceptance.

## Statement result

`Statement.lean` now freezes the intake-selected conventional claim as
`Stage1Instances.THM_M_0856.TutteOneFactorTarget`: every finite simple graph has a perfect matching
if and only if every vertex deletion leaves at most as many odd connected components as deleted
vertices. Its only direct import is `Mathlib.Combinatorics.SimpleGraph.Matching`, which provides the
statement vocabulary without importing the proof-bearing `SimpleGraph.Tutte` module.

`check_statement.py`, `statement.json`, `statement-validation.md`, and `statement-receipt.json`
record the explicit expression and environment fingerprints, two checked `Iff` transports, sole-
import deletion, and the four required structural mutations. `check_statement_artifacts.py`
replays and reconciles that packet. This is a worker-self-tested statement proposal pending
dependency-ordered master acceptance. The vector remains `[H1, M3, R4]`; no upstream proof body,
anchor audit, accepted state, audit completion, or theorem completion is claimed.

## Anchor-audit result

The immutable anchor inventory identifies one distinct exact terminal body:
`SimpleGraph.tutte` in pinned mathlib revision `8a178386ffc0`. `AnchorAudit.lean` checks a literal
adapter from its no-violator interface to the frozen target and reports only `propext`,
`Classical.choice`, and `Quot.sound`. The Atlas result is a duplicate wrapper over the same body,
not an independent closure. This is an exact `M0-W`-shaped candidate route, but its worker evidence
is below release-grade E1 and not master accepted, so the legal root classification remains `M3`.

## Obligation-tree result

`obligation-registry.json` freezes 56 stable semantic obligations before proof-phase credit.
`typed-graphs.json` separates proof, refinement, provenance, evidence, trust, documentation, and
workflow edges. The evidence graph is empty because every current worker packet is mutable,
unaccepted, and non-content-addressed. The proof architecture follows the pinned body through the
necessity injection, odd/even parity split, maximal matching-free supergraph, universal-vertex
clique construction, and the nonclique near-matching symmetric-difference argument.
`ObligationSignatures.lean` elaborates every planned proof-node interface, while
`ObligationTree.lean` checks only the literal terminal wrapper, exact adapter, and root composition.
All 16 internal source-body
relations remain explicitly unverified decomposition plans pending exact child-to-parent harnesses.

This worker-self-tested architecture keeps `accepted_closed_obligations=[]` and the root at
`[H1, M3, R4]`. Primary-source H0, proof-phase acceptance, release-grade provenance and trust,
readable R0, hermetic replay, independent validation, `AUDIT-Z`, theorem completion, and master
acceptance all remain open.

## Proof result

`Proof.lean` now installs `SimpleGraph.tutte` from manifest-pinned mathlib revision
`8a178386ffc0` at the frozen terminal interface. It checks the exact canonical root through
`compose_root terminal_adapter pinnedTerminal` and independently through a direct exact-target
wrapper. Lean reports the terminal and all three proof declarations sorry-free, with exactly
`propext`, `Classical.choice`, and `Quot.sound` in their axiom closures. Both root wrappers share
one upstream terminal body and receive no duplicate proof credit.

This is provisional proof-node evidence for an `M0-W` root proposal. It maps the pinned body to all
44 proof-reachable required-machine IDs but gives exact declaration evidence only to the root,
terminal, and adapter. The 16 internal source-body decomposition plans still lack abstract-child
composition certificates and receive no individual closure credit. The accepted instance remains
`[H1, M3, R4]`; validation, release, H0/R0, complete trust and provenance, master acceptance, and
theorem completion remain open.
