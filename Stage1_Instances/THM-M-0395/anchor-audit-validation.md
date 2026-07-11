# THM-M-0395 anchor-audit validation

Item: `S56-M-0395-ANCHOR_AUDIT`  
Audit date: `2026-07-12` (`Asia/Shanghai`)  
Base revision: `f87604acb61507f0c9c8d5de4ba3085b97a1de69`

## Result

The pinned mathlib revision has checked, locally elaborated support for number
fields, schemes, smooth and proper morphisms, scheme integrality, Northcott
finiteness, and abstract descent. These are nonterminal infrastructure. The
mathlib documentation row titled "Faltings's theorem" has no declaration, and
the pinned source tree contains no Faltings/Mordell terminal theorem.

Immutable external candidates were classified at the revisions recorded in
`anchor-audit.json`. Heights and adele projects provide only adjacent
infrastructure; Formal Conjectures has no matching path. GitHub repository
searches returned counts `0, 0, 0, 1`; the sole result is a perfect-cuboid
project and is a name/query false positive. This protocol is deliberately not
claimed to exhaust the public web.

No exact external proof exists among the identified candidates, so there is no
proof-bearing dependency to pin. The root remains `M4`, kernel closure is
false, and the remaining debt is formalization debt rather than unremediated
anchor-only integration debt. This completes only the assigned candidate audit.
It does not complete the theorem or any downstream phase.

## Commands and results

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0395` | 0 | rank 8, planned, L0, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| pinned mathlib `rg` for `Faltings`, `Mordell`, genus/rational-point terms | 0 | only the declaration-free docs row and Mordell-Weil commentary; no terminal theorem |
| GitHub repository API searches for the four recorded queries | 0 | totals `0, 0, 0, 1`, all complete; the one result is unrelated |
| immutable GitHub recursive-tree probes for the three external revisions | 0 | no path containing `Faltings` or `Mordell` |
| from `Formalizations/Lean`, `lake env lean ../../Stage1_Instances/THM-M-0395/Statement.lean` | 0 | canonical target elaborated as `Stage1Rev56.THMM0395.Statement.{u} : Prop` |
| from `Formalizations/Lean`, `lake env lean ../../Stage1_Instances/THM-M-0395/AnchorAudit.lean` | 0 | all seven partial mathlib declaration probes elaborated |
| `python3 Stage1_Instances/THM-M-0395/check_anchor_audit.py` | 0 | pin, statement hash, source witnesses, and seven non-closing rows verified |
| `python3 -m json.tool Stage1_Instances/THM-M-0395/anchor-audit.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0395 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The clone's pre-existing untracked `.lake` link reuses the canonical pinned
artifacts. No `lake update`, build, clone, fetch, or `.lake` mutation occurred.
