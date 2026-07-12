# THM-M-0525 obligation-tree validation

Item: `S56-M-0525-OBLIGATION_TREE`. Base revision:
`b86b7c60888b8506233bd2a07adc4f7c277ad675`.

Validation ran in the worker clone on 2026-07-12. The existing pinned Lake dependency closure was
used read-only; no update, build, clone, or fetch was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-0525/build_obligation_artifacts.py` | 0 | Wrote 10 obligations and 38 typed edges; denominator `34b82aed4bf90c1dfd7925851b063f488fadda0971cba4d0b0b5a55a22eac41f`. |
| `python3 Stage1_Instances/THM-M-0525/check_obligation_tree.py` | 0 | Checked source hashes, denominator projection, node schemas, typed adjacency, proof reciprocity, open-root boundary, and Lean hygiene. |
| `LEAN_BIN=$(cd Formalizations/Lean && lake env which lean); LEAN_DEPS=$(cd Formalizations/Lean && lake env printenv LEAN_PATH); cd Stage1_Instances/THM-M-0525; LEAN_PATH="$LEAN_DEPS" "$LEAN_BIN" -o Statement.olean Statement.lean; LEAN_PATH=".:$LEAN_DEPS" "$LEAN_BIN" ObligationTree.lean; rm -f Statement.olean` | 0 | Conditional group construction and exact root packaging elaborated. Both declarations report `[propext, Classical.choice, Quot.sound]`; no `sorryAx`. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0525` | 0 | Rank 582, planned lifecycle, theorem incomplete. |
| `python3 -m json.tool` on both generated JSON artifacts | 0 | Both parse as JSON. |
| prohibited-token scan of `ObligationTree.lean` | 0 | No `sorry`, `admit`, `sorryAx`, or axiom declaration. |
| `git diff --check -- Stage1_Instances/THM-M-0525` | 0 | No whitespace errors. |

The checks establish a reproducible obligation/graph freeze and a kernel-checked conditional
composition interface. They do not accept the pinned laws as proof-phase root evidence, establish
primary-source H0, close trust/provenance/readability, or satisfy release gates. The root remains
`[H1, M2, R3]`; audit completion and theorem completion are false. Master acceptance is required.
