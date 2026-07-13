# S56-M-1009-PROOF worker evidence

Date: `2026-07-13`. Base revision:
`bb6fb28ac1c55ecb52f3f1c84e7fbb35c26b47ad`.

## Implemented proof

`Proof.lean` imports the definitions and exact `ErdosRenyiLowerBoundTarget`
frozen in `Statement.lean`. It proves the finite counting-variable moment
identities, a support-sensitive Cauchy-Schwarz estimate, the finite ratio
bound, the shifted-window tail estimate, and the initial-segment limsup
comparison. It then identifies the decreasing tail intersection with the set
limsup and applies continuity from above. The final theorem has exactly the
frozen target type, including the zero-denominator convention and without an
independence premise. A second wrapper inhabits the independently frozen
`ObligationTree.Root` and passes it through `ObligationTree.root_compose`,
checking the terminal composition path selected by the obligation registry.

There is no `sorry`, `admit`, `sorryAx`, added axiom, unsafe declaration, or
substituted target. Lean reports exactly `[propext, Classical.choice,
Quot.sound]` for the root. This is provisional proof-phase evidence only. The
accepted root remains `H1/M3/R3`; master acceptance may promote the proof node
and machine root proposal, while validation, release, and theorem completion
remain downstream decisions.

## Commands and exact results

No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was
performed. The proof check built only temporary `Statement.olean` and
`ObligationTree.olean` files under `/tmp`, reused the canonical pinned
dependency artifacts, and removed its temporary directory.

```text
$ python3 Docs/tools/check_stage1_standard.py
check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)
exit 0

$ python3 scripts/stage1_target.py check
stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)
exit 0

$ python3 scripts/stage1_target.py show THM-M-1009
exit 0: execution rank 289; planned; L0/rework_required; theorem_complete=false

$ timeout 360s Stage1_Instances/THM-M-1009/check_proof.sh
exit 0: the exact imported root and frozen composition elaborated; both axiom reports were
[propext, Classical.choice, Quot.sound]

$ python3 Stage1_Instances/THM-M-1009/check_proof.py
PASS THM-M-1009 proof phase: exact frozen root is provisionally kernel-closed
exit 0

$ timeout 360s python3 Stage1_Instances/THM-M-1009/check_statement.py
exit 0: all four structural mutations were elaborated and distinguished

$ python3 Stage1_Instances/THM-M-1009/check_obligation_tree.py
PASS THM-M-1009 obligation tree: 15 obligations, 28 typed edges
exit 0: the frozen architecture truthfully retains its pre-proof M3 boundary

$ rg -n '\b(sorry|admit|sorryAx|axiom|constant|opaque|unsafe|extern|implemented_by|native_decide)\b' \
    Stage1_Instances/THM-M-1009/Proof.lean
no output; exit 1 (expected clean scan; `check_proof.py` repeats this after removing comments)

$ python3 -m json.tool Stage1_Instances/THM-M-1009/proof-status.json >/dev/null
$ python3 -m json.tool Stage1_Instances/THM-M-1009/proof-receipt.json >/dev/null
$ python3 -m json.tool .stage1-worker-selftest.json >/dev/null
exit 0 for each JSON document

$ git diff --check -- Stage1_Instances/THM-M-1009 .stage1-worker-selftest.json
no output; exit 0
```

Validated SHA-256 values:

```text
0e498dbd2d3c0f4d8def2a305388605fe571d3d77aa2033bb4e3edd633ef4fde  Proof.lean
9906d8bf53b69bff68246b938627f5f117611fbdf95e2e54f01758c28ce5d831  Statement.lean
9481f4c7c973a04eab69c35c7e27de90f6fef79ad2de6615994993c6e312cdae  ObligationTree.lean
0baaf6dd25fc4222d849fdfaa2240a537c6bd4ca81f9e18ecb8bab8f112e3fb0  obligation-registry.json
9fcd990adf7edf38e8cf2465b54d3c2ece7b82cc6638396679a34a8781e99f2a  typed-graphs.json
2e1f8eb08b6cf34ce5fc93d5354dd707faedc74dc465f81544ead90f4d8c9fd9  validation-specs.json
4182164ae4b6951d635fd90f70c85add5bbd26b66c4756bccafe7d8a798447f9  anchor-audit.json
```

Only the integration lane can accept the node-specific receipt. H0/R0,
transitive trust and provenance closure, cold/offline replay, independent
verification, validation, release, and `THEOREM-Z` remain open.
