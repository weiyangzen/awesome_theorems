# Statement-phase blocker

Item: `S56-M-0340-STATEMENT`  
Theorem: `THM-M-0340`  
Validation date: `2026-07-12` (`Asia/Shanghai`)  
Worker base revision: `230f719da7724afb27c761dcb8c62a327557fe63`

## Verdict

`blocked`: the repository sources do not identify one exact mathematical proposition, so an exact
Lean target cannot truthfully be selected or elaborated. The only source wording is
`选择公理下的分球定理` ("the ball-splitting theorem under the axiom of choice"), together with
the Banach/Tarski attribution and year 1924. It supplies no edition, theorem/page locator, quoted
statement, or decisions for the distinctions below.

This is the first failed gate in Phase 2 (Freeze The Target) of
`skills/execute-stage1-rev56/SKILL.md`: "source statement cannot be identified without inventing
missing mathematics." Consequently this phase does not create `Statement.lean`, does not fill the
null canonical target in `instance.json`, and does not claim statement completion. The intake API
probe remains encoding-feasibility evidence only.

## Unresolved statement identity

An accepted source passage and crosswalk must determine all of the following before retry:

1. whether the object is an open ball, closed ball, solid ball in another encoding, boundary
   sphere, or all of Euclidean three-space;
2. whether the conclusion is one ball equidecomposable with two balls, one sphere with two
   spheres, or a stronger equidecomposability result;
3. how the two copies are represented (disjoint translated subsets in one ambient space or a
   tagged disjoint union);
4. which transformations witness congruence (rotations, orientation-preserving rigid motions, or
   arbitrary Euclidean isometries), including whether translations and reflections are allowed;
5. whether a fixed piece count, such as five, is part of the claim;
6. the radius and center binders and the treatment of zero or negative radius; and
7. whether choice is merely part of the foundation profile or an explicit premise in the selected
   proposition.

Choosing any one of these common variants from general mathematical knowledge would broaden or
substitute for the repository's under-specified claim. Elaborating a generic proposition that
assumes the desired `Equidecomp` would also hide the theorem rather than state it.

## Validation evidence

The existing canonical `.lake` link and pinned artifacts were used read-only. No update, build,
fetch, or clone was run.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0340` | 0 | rank 833; lifecycle `planned`; `legacy_artifacts_accepted=false`; `theorem_complete=false` |
| `rg -n -C 12 '巴拿赫-塔斯基分球悖论\|Banach.Tarski\|Banach-Tarski\|选择公理下的分球定理' Docs Stage1_Instances Formalizations --glob '!Formalizations/Lean/.lake/**' --glob '!Docs/Stage1_Blueprint_rev-5.6.md' --glob '!Docs/Stage1_Execution_DAG_rev-5.6.json' --glob '!Docs/Stage1_Targets_rev-5.6.json'` | 0 | The only repository mathematical wording found is the topic-level gloss above; other matches are generated inventory/intake records, not an exact source statement. |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0340/IntakeProbe.lean)` | 0 | The pinned `Equidecomp`, Euclidean-space, ball/sphere, and isometry APIs elaborate; this does not resolve which target is intended. |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0340 -g '*.lean'` | 1 | Expected no-match exit: no prohibited placeholder or declared axiom in the owned Lean source. |
| `git diff --check -- Stage1_Instances/THM-M-0340` | 0 | No whitespace errors. |

Retry condition: provide and independently inspect an immutable primary or otherwise authoritative
source passage that fixes the seven choices above. Then the statement phase can encode that exact
claim, freeze ordered binders and foundation/TCB profiles, elaborate it with minimal pinned imports,
record its expression fingerprint, and run transport and mutation checks.

No `.stage1-worker-selftest.json` is emitted because the assigned statement phase did not pass its
hard gate.
