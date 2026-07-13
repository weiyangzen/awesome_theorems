# THM-M-0045 obligation-tree validation

Item: `S56-M-0045-OBLIGATION_TREE`  
Base revision: `7d0965498598e684e3e3d0a01836c2bf36a02959` (tree
`753e16a89fce09f051af066f8b58d3e6b2722ade`)  
Validation date: 2026-07-13 (`Asia/Shanghai`)

## Result

Registry version 1 freezes 37 semantic obligations against the exact `Statement.lean`, bounded
anchor audit, and immutable historical source revision `0a539f0c`. Its canonical denominator is
`47fc5062b82b1a06eb2ca0ce6379dc5ea7f6ec15481a1144fe24f11724baad1a`. Seven separate typed
graphs contain 153 edges and the nodes contain 105 substantive ledger steps, with each node under
the 100-step
split threshold.

The proof route expands the historical source through the zero/nontrivial dimension split,
eigenvalue and eigenspace construction, orthogonal complement, compressed restriction, strict
finrank descent, recursive basis, internal direct sum, collected orthonormal basis, three coefficient
cases plus one impossible index placement, matrix transport, unitary and upper-triangular witnesses,
and final equation. Only the
exact root composition from a global equation package is a current-pin checked composition
certificate. Twelve internal parent relations remain explicit unverified source-body decomposition
plans and cannot receive closure credit.

`ObligationTree.lean` elaborates the equation package and conditional root adapter. Both axiom
reports contain only `propext`, `Classical.choice`, and `Quot.sound`; the source contains none of
the prohibited proof devices checked by the validator. It constructs no Schur witnesses.
The checker also hashes Lean's fixed-option `#print` output for `SchurEquationPackage`,
`DimensionBoundary`, and `equationWitness_implies_targetAt`, then binds the actual package hash into
the root composition certificate; hand-written type summaries receive no fingerprint credit.

## Commands and exact outcomes

The automation-provided `.lake` symlink, pinned artifacts, and already materialized historical Git
object were used read-only. No Lake update/build, dependency clone/fetch/checkout, or `.lake`
mutation occurred.

| Command | Exit | Outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0045` | 0 | rank 1085, planned, L0/rework-required, theorem incomplete |
| `python3 -B Stage1_Instances/THM-M-0045/build_obligation_artifacts.py` | 0 | wrote 37 obligations, 153 typed edges, 105 substantive ledger steps, and the denominator above |
| `python3 -B Stage1_Instances/THM-M-0045/check_obligation_tree.py` | 0 | structural schemas, denominator, typed endpoints, reciprocity, acyclicity, reachability, source hash/markers, current-pin conditional Lean composition, axioms, receipt, and open closure passed |
| `for f in <six JSON artifacts>; do python3 -m json.tool $f >/dev/null or exit; done` | 0 | registry, typed graphs, validation specs, receipt, instance, and worker packet all parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0045-obligation-pycache python3 -m py_compile Stage1_Instances/THM-M-0045/build_obligation_artifacts.py Stage1_Instances/THM-M-0045/check_obligation_tree.py` | 0 | both Python programs compiled without writing target bytecode |
| prohibited-token scan over `ObligationTree.lean` | 1 | expected no-match result: no prohibited token in uncommented source |
| `git diff --check -- Stage1_Instances/THM-M-0045 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Open gate

The external implementation remains `M5/E3`: it is outside the current dependency closure, fails
against current mathlib, and lacks own-pin kernel, axiom, placeholder/unsafe, and transitive trust
evidence. It must be reproduced at its immutable historical pins, then ported or integrated at the
current pin with exact node composition receipts. The current classified root remains
`[H1, M3, R4]`; no
obligation, H0, R0, audit completion, theorem completion, or master acceptance is claimed.
