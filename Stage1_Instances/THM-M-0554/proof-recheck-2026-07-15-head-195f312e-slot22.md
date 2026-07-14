# THM-M-0554 proof-phase recheck: blocked

Item: `S56-M-0554-PROOF`

Attempt: `2026-07-15T06:44:34+08:00`

Base revision: `195f312e0164390d672a8e6642dd1242dd7bbe8d`

Base tree: `f12d8c8e0368a8142da0ceeb2c931a087157f49c`

## Verdict

`blocked`. No genuine Atiyah-Hirzebruch spectral-sequence proof body was
implemented or found in the pinned dependency closure. The exact root remains
`M4`; this attempt adds no proof receipt, composition certificate, debt-vector
change, or state transition.

The proof-relevant inputs are byte-for-byte unchanged from the preceding
recheck at revision `ed919316`: `Statement.lean`, `statement.json`, the anchor
audit, registry, typed graphs, validation specs, instance, and local task DAG
have no diff. Revision `195f312e` only integrates that preceding recheck and
its uncredited differential diagnostic into this target path.

The immediate root cut remains:

- `M0554-X-GENCOH`: generalized-cohomology pair, excision, and wedge infrastructure;
- `M0554-C-EXACT-COUPLE`: the skeletal-filtration exact-couple construction;
- `M0554-C-E2-MODEL`: the cellular-cohomology `E2` identification;
- `M0554-L-STRONG`: strong convergence for the finite skeletal filtration.

Pinned mathlib supplies generic spectral-sequence, CW-complex, and singular-
homology substrate only. A current-base search of every pinned package found no
AHSS, generalized-cohomology, exact-couple, or strong-convergence proof body.
Mathlib's spectral-object file still documents the intended
`spectralSequence`, `homologyData`, and `spectralSequenceHomologyData`
constructions as `TODO`.

## First Failed Gate

Exact-statement fidelity fails before a proof can be credited. The canonical
claim requires a reduced generalized cohomology theory and a genuine finite-CW
structure, but reducedness is absent from the frozen interface. In
`Statement.lean`, the theory facts `pointIsPoint`, `exactnessAxiom`, and
`wedgeAxiomOrRepresentability`, and the CW facts `finiteCW`, `exhaustive`, and
`cellAttachments`, are proposition-valued data rather than required proofs.
The output chooses the meanings of `coefficientConvention`,
`strongConvergence`, and `naturalityInSpace`, while
`filtrationIsInducedBy` is only `K.skeleton = K.skeleton`.

Consequently the literal proposition admits a zero spectral-sequence
inhabitant using zero objects, reflexive isomorphisms, and output-selected
`True` propositions. Independent proof search reconfirmed that this diagnostic
term elaborates at trust level zero, but it was not retained or credited: it
constructs no AHSS, closes none of the four root-cut packages, and supplies no
checked child-to-parent composition certificate. Retaining it would be a fake
result and violate exact-statement fidelity and the no-substitution rule.

The only apparent small positive body is already recorded in
`DifferentialProbe.lean`: the literal `pageDifferentialBidegree` formula is
definitionally provable by `rfl`. Registry v1 nevertheless makes
`M0554-B-DIFFERENTIAL` a nonleaf marked `split-required` and gives it a
`proof_requires` edge to open node `M0554-C-SPECTRAL`. The diagnostic consumes
neither that child nor its conclusion, so it cannot legally close the frozen
branch. Correcting the mismatched decomposition requires registry version 2.

Predecessor authority is also unresolved. The global obligation-tree item is
only provisional (`[_]`). In the dossier, `instance.json` still records a null
canonical module, expression, expression hash, and environment fingerprint
with status `open_statement_phase`. `task-dag.json` remains unfrozen, leaves
statement/source/tree open, and marks proof blocked by predecessors. In
addition, `statement.json` attributes convergence fields to the legacy
`AtiyahHirzebruchConvergenceData` declaration instead of the canonical owned
source's `Stage1.THM_M_0554.AtiyahHirzebruchData`. A proof-only worker cannot
silently replace or reconcile those predecessor artifacts.

## Validation

All Lean commands reused the automation-provided symlink to the canonical
pinned `.lake` artifacts. No update, build, dependency clone/fetch, network
action, or `.lake` mutation was performed. Generated Lean output was placed in
a temporary directory and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0554` | 0 | Rank 106; lifecycle `planned`; baseline `L0/rework_required`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0554/check_obligation_tree.py` | 0 | 32 obligations and 91 typed edges passed; denominator `3c72072a...8048b`; root remains M4 without a composition certificate. |
| Isolated resolved `lean --trust=0 -t0 -R "$target" -o "$tmp/Statement.olean" Statement.lean` | 0 | The frozen target elaborated with Lean 4.29.0; temporary output was removed. |
| Isolated pinned `lean --trust=0 -t0 -R "$target" -o "$tmp/DifferentialProbe.olean" DifferentialProbe.lean` | 0 | The minimally imported, uncomposed bidegree diagnostic elaborated; `#print axioms` reported `propext`, `Classical.choice`, and `Quot.sound`; temporary output was removed. |
| `rg -n -i --glob '*.lean' 'Atiyah[-_ ]?Hirzebruch\|AtiyahHirzebruch\|\bAHSS\b\|generalized[ _-]*(co)?homology\|exact[ _-]*couple\|strong[ _-]*convergence' Formalizations/Lean/.lake/packages` | 1 | Expected no-match result: no pinned terminal proof candidate was found. |
| The same query over repo-local Lean outside the dossier and pinned cache | 0 | Target-specific hits were the legacy `S1_M_106.lean` interfaces and blocker gates, not a terminal proof body. |
| `rg -n --pcre2 '^\s*(?:sorry\|admit\|axiom)(?:\s\|$)\|\bsorryAx\b\|^\s*unsafe(?:\s\|$)' Stage1_Instances/THM-M-0554 --glob '*.lean'` | 1 | Expected no-match result: no prohibited declaration token occurs. |
| Pinned Lean/Lake and mathlib revision/tree checks | 0 | Lean `4.29.0` commit `98dc76e...16740`; Lake `5.0.0-src+98dc76e`; mathlib `8a178386...ea95`, tree `bdc39a31...1c2b`; mathlib source tree clean. |
| Spectral-object source hash and `TODO` scan | 0 | SHA-256 `2ce62b9d...740aa`; intended spectral-sequence and homology-data constructors remain documented as `TODO`. |
| Proof-relevant `git diff --quiet ed919316..HEAD` | 0 | The eight canonical target inputs listed above are unchanged. |
| `python3 -m json.tool` plus scoped `jq -e` assertions on the companion JSON | 0 | The packet parsed and its identity, current base, blocked state, empty closure arrays, four-node root cut, and false completion flags agreed. |
| `git diff --no-index --check /dev/null` for each new owned artifact | 1 each | Expected content-difference status; both commands emitted no whitespace diagnostic. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The self-test manifest is absent because the proof phase is blocked. |

## Retry Condition

First publish and master-accept a source-faithful corrected statement,
reconcile the instance, task, and statement projections, and issue obligation-
registry version 2 with corrected branch dependencies. Then implement and
compose all four root-cut packages without placeholders. An alternative is an
immutable exact compatible Lean 4 AHSS proof that can be pinned, exact-type
transported, and checked with complete provenance, trust, and composition
closure.

These artifacts are durable blocker evidence only. They do not satisfy
`S56-M-0554-PROOF`, close an obligation, complete the audit or theorem, or
authorize master acceptance. Because the assigned phase is not genuinely
self-tested as complete, `.stage1-worker-selftest.json` remains absent.
