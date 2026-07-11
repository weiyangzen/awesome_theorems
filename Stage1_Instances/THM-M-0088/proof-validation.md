# THM-M-0088 proof-phase validation

## Implemented bodies

`Proof.lean` implements the frozen preimage by evaluating a transformation at `op X` on `𝟙 X`.
It proves the component equation from `Yoneda.naturality`, proves both inverse laws, and feeds those
bodies to the already checked `yonedaEmbedding_of_inverseLaws` constructor. The resulting
`yonedaEmbedding` inhabits the exact data-valued `YonedaEmbeddingTarget C`; it does not weaken the
root to fullness, faithfulness, or mere nonemptiness. No imported `Yoneda.fullyFaithful` proof body
is used to close the local proof graph.

This provisionally closes the six machine-required frozen obligations `M0088-ROOT`,
`M0088-T-CONSTRUCT`, `M0088-C-PREIMAGE`, `M0088-L-RIGHT`, `M0088-L-LEFT`, and
`M0088-B-NATURALITY`. The source and provenance overlays are not machine-proof obligations and are
not claimed here.

## Commands and results

Commands ran from base revision `1f93d74fbfd640b2ed20c70526609c84eb603b35` on 2026-07-12
(receipt timestamp `2026-07-11T23:47:49Z` UTC).

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0088
  exit 0: execution rank 137; planned; theorem_complete=false

Stage1_Instances/THM-M-0088/check_proof.sh
  exit 0: Statement, ObligationTree, and Proof elaborated in a temporary directory
  #print axioms for the four local proof declarations reported only
  [propext, Classical.choice, Quot.sound]

python3 Stage1_Instances/THM-M-0088/check_proof.py
  exit 0: PASS THM-M-0088 proof: 6 frozen machine obligations locally closed

rg -n '\b(sorry|admit|sorryAx)\b|^[[:space:]]*(axiom|unsafe)\b' \
  Stage1_Instances/THM-M-0088/Proof.lean
  exit 1 with empty output: pass, no prohibited declaration or placeholder

git diff --check -- Stage1_Instances/THM-M-0088
  exit 0: no whitespace errors
```

No update, build, clone, fetch, or mutation of `.lake` was performed. This is provisional proof-node
evidence pending master acceptance. It does not claim H0, R0, validation/release gates, independent
verification, hermetic replay, or theorem completion.
