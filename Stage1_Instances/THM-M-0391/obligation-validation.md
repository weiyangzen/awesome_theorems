# Obligation-tree validation receipt

Item: `S56-M-0391-OBLIGATION_TREE`

Base revision: `3eb3bf1bab9ffff7a10bfdd0e5131144e7c71a9b`

Validation date: `2026-07-12` (Asia/Shanghai)

The worker used the existing pinned toolchain and canonical reused Lake
artifacts. It did not update, build, clone, fetch, or otherwise mutate `.lake`.
The pre-existing untracked `Formalizations/Lean/.lake` link/artifact was left
unchanged.

## Commands and exact results

All commands ran from the repository root unless a subshell is shown.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: check_stage1_standard: ok (15 assurance groups, 41 legacy rows,
  300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)

python3 scripts/stage1_target.py check
  exit 0: stage1_target: ok (1546 unique targets, ranks 1..1546, all
  L0/rework_required)

python3 scripts/stage1_target.py show THM-M-0391
  exit 0: execution_rank=5; lifecycle_mode=planned;
  theorem_complete=false

python3 -m json.tool Stage1_Instances/THM-M-0391/{instance,obligation-registry,obligation-nodes,typed-graphs}.json
  exit 0 for every file

python3 <inline structural validator recorded below>
  exit 0: ok: 15 complete node records; digest
  34303df380facae6379de68a228a154d99ccdccd152e38962df41f0e8674e138;
  7 typed graphs; proof graph acyclic and root-reaches every obligation

(cd Formalizations/Lean && lake env lean \
  ../../Stage1_Instances/THM-M-0391/Statement.lean)
  exit 0 with no output: exact target, checked iff transport, and two boundary
  mutation counterexamples elaborate under the pinned environment

git diff --check -- Stage1_Instances/THM-M-0391
  exit 0 with no output

sha256sum Stage1_Instances/THM-M-0391/obligation-registry.json \
  Stage1_Instances/THM-M-0391/obligation-nodes.json \
  Stage1_Instances/THM-M-0391/typed-graphs.json \
  Stage1_Instances/THM-M-0391/obligation-tree.md
  exit 0:
  c340453b27db47a49d59c81af6cfa88037cd3b8a4572f3fdf7df47425db7af1f  obligation-registry.json
  d095791454971080adcfe310d267c6516b351ad8ad269d7f99364692033b305d  obligation-nodes.json
  3f7ae2e9cf98aa7ee05ccd0c8cadcc0f2b9c3aec9eb1ea64500f6bd5252d0b17  typed-graphs.json
  ac0fafc6ac840287704861898981c33b4234d9b7be986606625c214838543afd  obligation-tree.md
```

The inline validator parsed all structured artifacts; required every registry
and node-schema field; checked the 15 one-to-one registry/node identities,
debt enums, and `1..100` node budgets; recomputed the canonical eligibility
projection digest; checked graph names and edge-type enums; rejected duplicate
edges; required proof/refinement endpoints to be obligations; and proved by
depth-first traversal that the proof graph is acyclic and every obligation is
reachable from `M0391-ROOT`.

## Status boundary

These checks self-test the assigned architecture freeze only. They do not prove
the open mathematical nodes, validate terminal proof bodies, establish H0 or
R0, complete `AUDIT-Z`, or complete `THEOREM-Z`. Master acceptance is still
required to promote the scheduler item.
