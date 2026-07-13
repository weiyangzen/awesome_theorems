# THM-M-0626 proof-phase validation

Item: `S56-M-0626-PROOF`. Base revision:
`72e9e8092182121a6794921f61fcc9cae22f726d` (tree
`0d6c1fdf06d1573c256af331c6b198e5a787af43`).

## Implemented proof routes

`Proof.lean` installs pinned mathlib's exact `IsConnected.image` theorem at the frozen
`LocalConnectedImagePackage` interface, consumes `globalToLocalContinuity`, and produces the
unchanged `ConnectedImageTarget` through both registered terminal-assembly interfaces. It also
implements the visible proof body independently: construct two relative source opens, pull back
the image cover and endpoint witnesses, apply source preconnectedness, push the intersection
witness forward, restore image nonemptiness, and reassemble image connectedness.

The pinned and expanded routes are deduplicated. The terminal upstream bodies remain
`IsPreconnected.image` and `IsConnected.image` in
`Mathlib/Topology/Connected/Basic.lean:273-297` at mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The proof is a provisional `M0-W` candidate. The
accepted vector remains `[H1, M3, R4]`, and this worker evidence does not claim theorem completion.

## Commands and exact results

Validation ran on 2026-07-13 (`Asia/Shanghai`). The automation-provided canonical `.lake` symlink
was reused read-only. No `lake update`, `lake build`, dependency clone/fetch, checkout, or `.lake`
mutation ran.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0626
  exit 0: rank 1320, planned, L0/rework_required, theorem_complete=false

bash Stage1_Instances/THM-M-0626/check_proof.sh
  exit 0: isolated Statement, ObligationTree, and Proof elaboration passed; all fifteen audited or
  implemented declarations were sorry-free, and axiom closure was a subset of propext,
  Classical.choice, and Quot.sound

python3 -B Stage1_Instances/THM-M-0626/check_proof.py
  exit 0: exact source, target, graph, denominator, terminal body, pin, receipt, worker packet, and
  truthful status boundary passed

python3 -B Stage1_Instances/THM-M-0626/check_obligation_tree.py
  exit 1: the predecessor's frozen workflow snapshots still record pre-integration authoritative
  item states; the integration lane later promoted predecessor proposals to [_]

rg -n -i --glob '*.lean' '\b(sorry|admit|sorryAx)\b|^[[:space:]]*(axiom|constant|opaque|unsafe)[[:space:]]|implemented_by|native_decide|extern[[:space:]]' Stage1_Instances/THM-M-0626/Proof.lean
  exit 1 with empty output: expected pass; no prohibited construct found

python3 -m json.tool Stage1_Instances/THM-M-0626/proof-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0: both structured artifacts parsed

PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0626-proof-pycache python3 -m py_compile Stage1_Instances/THM-M-0626/check_proof.py
  exit 0: validator compiled outside the repository tree

git diff --check -- Stage1_Instances/THM-M-0626 .stage1-worker-selftest.json
  exit 0: no tracked whitespace diagnostics
```

The proof node remains provisional until dependency-ordered predecessor and node-specific master
acceptance. `M0626-S-FOUNDATION`, H0, R0, full transitive provenance/trust, hermetic replay,
independent verification, validation, release, `AUDIT-Z`, and `THEOREM-Z` remain downstream.
