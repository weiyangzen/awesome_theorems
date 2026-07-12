# THM-M-0772 release decision

Item: `S56-M-0772-RELEASE`

The exact verdict is `blocked`. The lifecycle remains `planned`, the accepted root vector remains
`[H1, M4, R4]`, and both `audit_complete=false` and `theorem_complete=false`. No receipt is accepted
and no authoritative state is promoted.

The proof and validation receipts contain useful provisional evidence: the exact maximal-chain root
and its expanded form elaborate through pinned mathlib `maxChain_spec`, and a second same-worker
implementation uses `IsChain.exists_maxChain`. The observed axioms are `propext`,
`Classical.choice`, and `Quot.sound`, and the local placeholder/unsafe scan passes. This supports a
candidate `M0-W` classification for later master reconciliation, but it is not release-grade `E1`
evidence and cannot overwrite the planned instance, open task DAG, or stale pre-proof typed graph.

The first failed gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`: `S56-M-0772-VALIDATION` remains open and
its receipt is only `provisional_worker_selftest` with `release_grade=false`. The next release gate
also fails: the run reused a shared warm `.lake` cache rather than performing an empty-cache,
network-denied cold build and offline restoration. H0 and R0 independent reviews, complete
transitive TCB and supply-chain closure, two separately provisioned signed runners, an independently
implemented minimal verifier, adversarial fixtures, deterministic bundling, protected CI evidence,
and master acceptance are absent.

## Self-test

Commands run from base revision `ed3ed0f054485ec0127b6322b75cd061be59d105`:

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0772
  exit 0: rank 580; lifecycle planned; theorem_complete=false

python3 Stage1_Instances/THM-M-0772/check_validation.py
  exit 0: exact statement, composition, proof roots, and independent direct root elaborated;
  release hermetic and distinct-runner gates remained blocked

python3 Stage1_Instances/THM-M-0772/check_release.py
  exit 0: blocked decision agrees with the current instance, DAG, graph, and receipts

cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0772/Proof.lean
  exit 0: exact and expanded maximal-chain proof declarations elaborated

git diff --check -- Stage1_Instances/THM-M-0772 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

No dependency update, build, clone, fetch, or `.lake` mutation was performed. The pre-existing
untracked `.lake` symlink is not a changed path and is not release evidence. Only the integration
lane may accept the dependency chain or reconcile authoritative root state.
