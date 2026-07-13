# THM-M-0041 proof-phase validation

Item: `S56-M-0041-PROOF`

Base revision: `c5f6fb269f6eb84efa935ee66c4e9bab92495e61`

Validation date: `2026-07-13` (`Asia/Shanghai`)

## Implemented proof

`Proof.lean` imports the exact statement and obligation interfaces through `ObligationTree.lean`.
It implements the four visible stages of the pinned proof body: the adjugate identity, transport
through `matPolyEquiv`, evaluation of the right factor `X - C A`, and conversion back to algebra
evaluation. Their checked composition proves the exact matrix engine and then the frozen expanded-
determinant root. A second root uses the exact pinned terminal theorem
`Matrix.aeval_self_charpoly` from mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The wrappers do not receive separate terminal-body
credit.

The proof retains arbitrary commutative rings, finite decidable index types, empty dimensions, and
zero rings. All eight local declarations and the pinned terminal theorem report only `propext`,
`Classical.choice`, and `Quot.sound`. There is no `sorry`, `admit`, `sorryAx`, axiom declaration,
opaque declaration, or unsafe declaration in `Proof.lean`.

This supplies provisional proof-node evidence for `M0-W`; it is not authoritative acceptance.
The root vector remains `[H1, M3, R3]` until the integration lane accepts dependency-ordered
receipts. Validation, source, readability, trust, release, audit completion, and theorem completion
remain separate.

## Commands and results

All commands ran inside this worker clone. The pre-existing automation-provided canonical `.lake`
symlink was reused read-only. No `lake update`, `lake build`, dependency clone/fetch, network access,
or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, execution skill, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0041` | 0 | rank 1081, planned, L0/rework-required, theorem incomplete |
| `(cd Formalizations/Lean && bash ../../Stage1_Instances/THM-M-0041/check_proof.sh)` | 0 | isolated statement/tree compilation and proof elaboration passed; all local declarations and `Matrix.aeval_self_charpoly` reported only the allowed three axioms; output SHA-256 `725a5f76...8011c` |
| `python3 -B Stage1_Instances/THM-M-0041/check_proof.py` | 0 | exact task identity, prerequisite/source hashes, mathlib pin, proof markers, isolated Lean replay, axiom closure, receipt, and worker packet agreed |
| `python3 -m json.tool Stage1_Instances/THM-M-0041/proof-receipt.json` and `python3 -m json.tool .stage1-worker-selftest.json` | 0 each | both structured artifacts parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0041-proof-pycache python3 -m py_compile Stage1_Instances/THM-M-0041/check_proof.py` | 0 | validator compiled outside the repository tree |
| `rg -n '<prohibited construct pattern>' Stage1_Instances/THM-M-0041/Proof.lean` | 1 (expected) | no prohibited proof gap, axiom, opaque, or unsafe construct matched |
| `git diff --check -- Stage1_Instances/THM-M-0041 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

The statement compilation intentionally prints diagnostics from its successful `#check_failure`
mutation and negative-availability probes. Those messages are expected and the command exits zero.
The proof validator requires zero exit status, every expected axiom report, the exact allowed axiom
set, and absence of `error:` and `sorryAx` in the combined replay output.

## Open gates

Master acceptance of all provisional prerequisites and this node is pending. Release-grade E1,
full provenance and trust closure, a cold hermetic replay, deterministic evidence, independent
verification, H0, R0, validation, release, `AUDIT-Z`, and `THEOREM-Z` are outside this proof phase.
