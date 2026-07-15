# THM-M-0554 proof-phase recheck at `44afc5d9`

Item: `S56-M-0554-PROOF`

Intent: `prove`

Verdict: `blocked`

No worker self-test manifest is emitted. This packet closes no obligation and
does not propose `[_]`.

## First Failed Gate

Exact-statement fidelity fails before proof credit. The selected theorem is the
cohomological Atiyah-Hirzebruch spectral sequence for a reduced generalized
cohomology theory on a finite CW complex. The current Lean root instead
quantifies structures whose `pointIsPoint`, exactness, wedge, finite-CW,
exhaustiveness, and cell-attachment fields are proposition *values*, without
proofs of those propositions. Such a field may be `False`, so a genuine AHSS
construction cannot use the advertised hypotheses. Reducedness is absent.

The output is disconnected in the opposite direction. It selects bare
propositions for coefficient convention, strong convergence, and naturality;
`ordinaryCohomology` is not defined as `H^p(X; E^q(pt))`; and the purported
filtration link is the tautology `K.skeleton = K.skeleton`. Hence a zero
spectral-sequence/`True` witness can inhabit the literal proposition while
constructing no AHSS. That candidate is a fake result relative to the
canonical claim and frozen semantic tree, so it is not retained or credited.

Predecessor authority also remains unresolved. `instance.json` is still
`planned` with null canonical-formal identity fields, `task-dag.json` is
unfrozen and marks proof blocked by predecessors, and the obligation-tree item
is only provisional rather than master-accepted.

## Proof Boundary

The existing `Proof.lean` is placeholder-free and kernel-checks field-by-field
conditional composition, but `statementOfBranchFamily` assumes the complete
E2, differential, convergence, and naturality branch family. Section 6.7
therefore forbids closure while those children are open.

`DifferentialProbe.lean` proves the literal `ComplexShape.up'` bidegree relation
by `rfl`. It is not frozen-node composition: registry v1 makes
`M0554-B-DIFFERENTIAL` a nonleaf requiring the still-open
`M0554-C-SPECTRAL`. The probe receives no branch-closure credit.

The current substantive root cut is unchanged:

- `M0554-X-GENCOH`: generalized-cohomology pair, excision, and wedge support;
- `M0554-C-EXACT-COUPLE`: the skeletal-filtration exact couple;
- `M0554-C-E2-MODEL`: the cellular-cohomology E2 identification;
- `M0554-L-STRONG`: strong convergence for the finite filtration.

Pinned mathlib supplies generic spectral-sequence, CW-complex, and singular-
homology substrate only. The spectral-object source still marks the intended
spectral-sequence and homology-data constructors as `TODO`, and the current
pinned-source scan found no terminal AHSS body. The ten proof-relevant inputs
are byte-identical to the prior `a1ba351e` slot16 recheck; intervening commits
only integrate evidence.

## Validation

Base revision: `44afc5d93ff24855c0f4cc5ae48f4b6be094a08e`

Base tree: `4fbba127c10efa3d76cb99767630cf3034a84ada`

The automation-provided `.lake` symlink was reused read-only. No update, build,
clone, fetch, checkout, ref repair, network action, or dependency mutation was
performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard check passed for 15 assurance groups and all 1546 uniform-L0 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Manifest check passed for 1546 unique targets at ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-0554` | 0 | Rank 106; lifecycle `planned`; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0554/check_obligation_tree.py` | 0 | 32 obligations and 91 typed edges passed; denominator `3c72072a...8048b`; root remains open at M4. |
| Isolated `LAKE_NO_UPDATE=1 lake env lean --trust=0 -t0` replay of `Statement.lean`, `Proof.lean`, and `DifferentialProbe.lean` | 0 | Lean 4.29.0 elaborated all three; objects were 429072, 280728, and 15576 bytes. Logs hashed to `f1690fd1...d30`, `8cfbfe08...2a1`, and `30cba6d3...156`. The conditional proof declarations were sorry-free and reported exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| Pinned-package AHSS/generalized-cohomology/exact-couple/strong-convergence `rg` scan | 1 | Expected no-match: no terminal proof candidate exists in the pinned packages. |
| Repo-local proof-candidate scan outside this dossier and `.lake` | 0 | Target-specific matches are legacy `S1_M_106.lean` interfaces and explicit blocker gates, not a terminal AHSS proof. |
| Prohibited-device scan over owned Lean sources | 1 | Expected no-match: no `sorry`, `admit`, `axiom`, `sorryAx`, bodyless constant/opaque, unsafe/oracle, or equivalent device occurs. |
| TODO and SHA-256 audit of mathlib's spectral-object source | 0 | Source hash `2ce62b9d...740aa`; intended constructors remain documented as `TODO`. |
| `git diff --quiet a1ba351e...HEAD --` over the ten proof-relevant inputs | 0 | Inputs are unchanged; intervening commits add evidence only. |

The isolated replay used disposable outputs under `/tmp`; they were removed on
exit. It validates only the frozen statement, conditional composition, and
bidegree diagnostic. It supplies no evidence for the absent AHSS construction
branches or root.

## Retry Condition

First publish and master-accept a source-faithful statement whose assumptions
carry evidence and whose E2, filtration, convergence, and naturality predicates
are tied to the constructed spectral sequence. Reconcile instance/task/
statement authority and issue registry v2 with exact branch fingerprints. Then
implement and compose all four root-cut packages without placeholders. An
alternative is an immutable compatible external Lean 4 AHSS proof passing
exact-type, provenance, trust, and composition checks.

Status boundary: this is durable current-base blocker evidence only. It does
not satisfy `S56-M-0554-PROOF`, close an obligation or root, propose `[_]`,
complete the audit or theorem, enter validation/release, or authorize master
acceptance. Because the proof phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` remains absent.
