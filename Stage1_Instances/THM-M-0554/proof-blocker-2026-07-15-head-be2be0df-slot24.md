# THM-M-0554 proof-phase recheck at `be2be0df`

Item: `S56-M-0554-PROOF`

Intent: `prove`

Verdict: `blocked`

No worker self-test manifest is emitted. This packet closes no obligation and
does not propose `[_]`.

## First failed gate

Exact-statement fidelity fails before proof credit. The selected theorem is the
cohomological Atiyah-Hirzebruch spectral sequence for a reduced generalized
cohomology theory on a finite CW complex. The current Lean root instead
quantifies structures whose `pointIsPoint`, exactness, wedge, finite-CW,
exhaustiveness, and cell-attachment fields are proposition *values*, without
proofs of those propositions. Such a field may be `False`, so a genuine AHSS
construction cannot use the advertised hypotheses.

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

## Proof boundary

The existing `Proof.lean` is placeholder-free and kernel-checks field-by-field
conditional composition, but `statementOfBranchFamily` assumes the complete
E2, differential, convergence, and naturality branch family. Section 6.7
therefore forbids closure while those children are open.

`DifferentialProbe.lean` proves the literal `ComplexShape.up'` bidegree relation
by `rfl`. It is not a frozen-node composition: registry v1 makes
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
pinned-source scan found no terminal AHSS body.

## Validation

Base revision: `be2be0dfe2f4f2cbdd35f1f2397e5a372d199eb9`

Base tree: `2d3961f99039c515141bdff4511470530d799581`

The automation-provided `.lake` symlink was inspected and reused read-only.
No update, build, clone, fetch, checkout, ref repair, or other dependency
mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard check passed for 15 assurance groups and all 1546 uniform-L0 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Manifest check passed for 1546 unique targets at ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-0554` | 0 | Rank 106; lifecycle `planned`; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0554/check_obligation_tree.py` | 0 | 32 obligations and 91 typed edges passed; denominator `3c72072a...8048b`; root remains open at M4. |
| `timeout 60 lake env lean --version` from `Formalizations/Lean` | 1 | The required Lake gate failed before Lean because `flt-regular` could not resolve `HEAD` to a commit. |
| `LAKE_NO_UPDATE=1 timeout -k 2 15 lake env lean --version` from `Formalizations/Lean` | 124 | A bounded retry timed out before output. Immutable inspection confirms `flt-regular/.git/HEAD` points to nonexistent `refs/heads/.invalid`; it was not repaired. |
| Direct pinned Lean 4.29.0 `--trust=0 -t0` replay using existing olean paths | 0 | `Statement.lean`, `Proof.lean`, and `DifferentialProbe.lean` elaborated to disposable objects of 429072, 280728, and 15576 bytes. The three conditional proof declarations were sorry-free and reported only `propext`, `Classical.choice`, and `Quot.sound`. |
| Pinned-source AHSS/generalized-cohomology/exact-couple/strong-convergence scan | 1 | Expected no-match; no terminal proof candidate found. |
| Prohibited-device scan over owned Lean sources | 1 | Expected no-match; no `sorry`, `admit`, `axiom`, `sorryAx`, bodyless `constant`/`opaque`, unsafe/oracle, or equivalent device found. |
| JSON parse plus fail-closed packet assertions | 0 | The packet and all top-level owned JSON parsed; identity, base, blocked state, false completion flags, and the exact four-node root cut were confirmed. |
| `git diff --check` and root self-test absence check | 0 | No whitespace errors; `.stage1-worker-selftest.json` is absent as required for an incomplete proof phase. |

The direct Lean replay is warm, nonrelease diagnostic evidence only. It does
not replace the required `lake env lean` gate and validates only the existing
conditional bodies and bidegree diagnostic, not the AHSS theorem.

## Retry condition

First publish and master-accept a source-faithful statement whose assumptions
carry evidence and whose E2, filtration, convergence, and naturality predicates
are tied to the constructed spectral sequence. Reconcile the instance and task
authorities, and issue registry v2 with exact elaborated branch fingerprints.
Then implement and compose the four root-cut packages without placeholders.
An alternative is an immutable compatible external Lean 4 AHSS proof passing
exact-type, provenance, trust, and composition checks. The canonical pinned
Lake artifact must also be restored without a worker-side fetch or mutation.

Status boundary: this is durable blocker evidence only. It does not satisfy
`S56-M-0554-PROOF`, close the root, complete the audit or theorem, enter
validation/release, or authorize master acceptance.
