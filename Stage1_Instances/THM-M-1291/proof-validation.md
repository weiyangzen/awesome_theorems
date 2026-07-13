# THM-M-1291 proof-phase validation

Item: `S56-M-1291-PROOF`. Base revision:
`35d23d0193cd7c8fccb1d09f22534c6eba066b02`.

## Implemented proof

`Proof.lean` now gives the exact local declaration
`Stage1Instances.THM_M_1291.brezisLiebTarget_proof : BrezisLiebTarget`.
It preserves the frozen arbitrary measure space, complex codomain, almost-everywhere
convergence, one uniform integral bound, and every real exponent `p > 0`.

The proof first obtains integrability of the limiting `p`-power density by Fatou's
lemma. For `0 < p <= 1`, real-power subadditivity bounds the corrected density by
the integrable limit density, so dominated convergence applies. For `1 < p`, a
weighted convexity inequality bounds a nonnegative truncated error. Dominated
convergence sends that truncation integral to zero, while a uniform bound on the
remainder integrals controls the discarded epsilon term. Integral subtraction
then yields the exact splitting limit. The two exponent branches are exhaustive.

This is a provisional `M0-L` proof-body proposal for the 14 frozen required-machine
obligations. The frozen registry and graph retain their pre-proof open snapshot, as
required; only the integration lane may accept the proposal or update authority
state. Human-source, readability, provenance, trust, validation, and release gates
are not claimed here.

## Commands and results

Commands ran on 2026-07-14 in the worker clone. `check_proof.sh` copied the actual
owned `Statement.lean` into a fresh temporary directory under the worker root,
compiled it to `Statement.olean`, then compiled the actual owned `Proof.lean` to a
fresh `Proof.olean` with the direct pinned Lean executable and `--trust=0`. It used
only the existing pinned `LEAN_PATH`; the temporary directory was removed on exit.
No update, build, dependency clone/fetch, network operation, or `.lake` mutation was
performed.

```text
bash Stage1_Instances/THM-M-1291/check_proof.sh
  exit 0: fresh Statement and Proof elaboration passed with --trust=0; exact root
  axiom report was [propext, Classical.choice, Quot.sound]

python3 -B Stage1_Instances/THM-M-1291/check_proof.py
  exit 0: exact target, frozen hashes and denominator, local proof surfaces,
  provisional receipt, pinned mathlib identity, and prohibited constructs passed

python3 Stage1_Instances/THM-M-1291/check_obligation_tree.py
  exit 0: frozen 17-obligation and 38-edge pre-proof architecture still validates

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and all 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework-required

python3 scripts/stage1_target.py show THM-M-1291
  exit 0: rank 462, planned, L0/rework-required, theorem_complete=false

rg -n -i --glob '*.lean' '\b(sorry|admit|sorryAx)\b|^[[:space:]]*(axiom|constant|opaque|unsafe)[[:space:]]|implemented_by|native_decide|extern[[:space:]]' \
  Stage1_Instances/THM-M-1291/Proof.lean
  exit 1 with empty output: expected pass, no prohibited construct found

python3 -m json.tool Stage1_Instances/THM-M-1291/proof-receipt.json
  exit 0: valid JSON

git diff --check -- Stage1_Instances/THM-M-1291 .stage1-worker-selftest.json
  exit 0: no scoped whitespace errors
```

The proof source SHA-256 is
`a5e3f1e9abd93eb15b124eb7bdd8fd3e860154e7f5bada6326f6d88115ecdbc9`;
the statement source SHA-256 is
`ef19e70e68cd8c9179130141706954825b7de8529ecef6aec1dc6e87c76dd92f`.
An independent fresh temporary replay by a second worker agent also exited 0 under
`--trust=0`, with the same axiom report and source hashes; it is corroboration in
the same workspace, not the separate-runner verification required for release.

Accepted state remains `[H2, M3, R4]` until master acceptance. The next workflow
cut is `S56-M-1291-VALIDATION`, followed by release; H0, R0, complete provenance
and trust, cold hermetic replay, independent verification, `AUDIT-Z`, `THEOREM-Z`,
and theorem completion all remain open.
