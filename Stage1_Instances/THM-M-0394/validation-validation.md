# THM-M-0394 validation handoff

## Verdict boundary

Item `S56-M-0394-VALIDATION` is self-tested as a fail-closed partial-validation handoff. The exact
logical genus split and conditional child-to-parent composition kernel-elaborate, and
`Validation.lean` reconstructs both without importing `Proof.lean`. Neither substantive finiteness
branch is proved, so the root remains `[H3, M3, R3]`; `audit_complete=false` and
`theorem_complete=false` are mandatory.

## Commands and results

Commands ran from base revision `c6c14c0add140b98175266dc6421066ea99c79b3` on 2026-07-12
(receipt timestamp `2026-07-11T19:34:12Z` UTC).

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0394
  exit 0: rank 7; planned; theorem_complete=false

python3 Stage1_Instances/THM-M-0394/check_obligation_tree.py
  exit 0: 17 obligations and 47 typed edges pass; root open M3

cd Formalizations/Lean &&
  bash ../../Stage1_Instances/THM-M-0394/check_composition.sh
  exit 0: conditional branch_composition elaborated

cd Formalizations/Lean &&
  bash ../../Stage1_Instances/THM-M-0394/check_proof.sh
  exit 0: both partial proof declarations elaborate; axioms are exactly
  propext, Classical.choice, and Quot.sound

cd Formalizations/Lean &&
  bash ../../Stage1_Instances/THM-M-0394/check_validation_lean.sh
  exit 0: both independent probes elaborate; axioms are exactly propext,
  Classical.choice, and Quot.sound

python3 Stage1_Instances/THM-M-0394/check_validation.py
  exit 0: frozen hashes and 17-node boundary verified; partial proof and
  independent probes elaborated; root remains open

rg -n '\b(sorry|admit)\b|^[[:space:]]*(axiom|unsafe)\b' \
  Stage1_Instances/THM-M-0394/{Statement,ObligationTree,Proof,Validation}.lean
  exit 1 with empty output: pass, no prohibited local construct

git diff --check -- Stage1_Instances/THM-M-0394 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

No `lake update`, `lake build`, dependency clone/fetch, network access, or `.lake` mutation occurred.
The pre-existing canonical pinned `.lake` symlink was reused.

## Failed gates

The first node gate failure is the proof dependency: `M0394-N`, `M0394-N1`, `M0394-B1`,
`M0394-B2`, their arithmetic children, `M0394-T`, and the root are open and unaccepted. Consequently
there is no root trust/provenance closure. The same-workspace independent probe is useful
cross-check evidence, not the distinct signed runner required by section 10.7. Empty-cache hermetic
replay, offline restoration, H0/R0 review, SBOM/licenses, deterministic bundling, and master
acceptance remain open.
