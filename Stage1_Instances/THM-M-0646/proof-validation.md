# THM-M-0646 proof-phase validation

Item: `S56-M-0646-PROOF`. Base revision:
`3249eebf1d6d90d75e4ab28fe97dd9f92c906b59`.

`Proof.lean` supplies a repo-local theorem at the exact frozen
`LoewenheimSkolemTarget`. Its terminal body is the pinned mathlib declaration
`FirstOrder.Language.exists_elementarilyEquivalent_card_eq`, which constructs
the required exact-cardinality model through the two cardinal-direction
branches. The frozen source-cardinality premise is deliberately retained and
unused because the pinned theorem proves the same conclusion under weaker
hypotheses. This is strengthening, not a change or broadening of the target.

## Commands and results

Commands ran in the worker clone on 2026-07-12. The proof checker creates an
isolated temporary `Statement.olean`, prepends it to the canonical pinned
`LEAN_PATH`, and removes it on exit.

```text
bash Stage1_Instances/THM-M-0646/check_proof.sh
  exit 0
  Both exact-target wrappers and all seven printed upstream declarations
  elaborated. Every #print axioms result was exactly
  [propext, Classical.choice, Quot.sound]. The forbidden-boundary scan had no
  matches. Final line: PASS THM-M-0646 proof phase: exact pinned wrapper elaborated

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546
  uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0646
  exit 0: execution rank 692; lifecycle planned; theorem_complete=false

git diff --check -- Stage1_Instances/THM-M-0646 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

No update, build, dependency clone, fetch, or mutation of `.lake` was
performed. The existing canonical pinned artifacts were read only. This
proof-phase evidence proposes `M0-W` machine closure for the exact root,
pending master acceptance. It does not claim H0, R0, validation, hermetic
replay, independent verification, release, audit completion, or theorem
completion. The source and trust obligations `M0646-X-SOURCE` and
`M0646-X-TCB` remain outside this phase.
