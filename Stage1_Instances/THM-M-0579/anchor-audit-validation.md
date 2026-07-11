# Anchor-audit validation record

Item: `S56-M-0579-ANCHOR_AUDIT`  
Base revision: `70b2a7ed5befb7d04e66a3a6907b5cd496a3b701`

## Result

The exact local target remains `M3`. Pinned mathlib at
`8a178386ffc0f5fef0b77738bb5449d50efeea95` contains the exact signature as
`proof_wanted SimplyConnectedSpace.nonempty_homeomorph_sphere_three`, but Batteries elaborates that
command under `withoutModifyingEnv`; the name is absent after import and has no retained proof body.
The checked sphere and simply-connectedness declarations are supporting object-model APIs only.

The immutable `lean-dojo/LeanMillenniumPrizeProblems` candidate defines a near-match with an extra
`SecondCountableTopology` assumption and proves only the generalized dimension-zero case. The
immutable `google-deepmind/formal-conjectures` candidate states a stronger homotopy-equivalence
formulation, but its terminal body is explicitly `by sorry`, so it is `M5` and rejected. The legacy
slot is statement/audit material and receives no inherited rev-5.6 credit. Thus no external body can
be integrated, and neither `M0` nor `M1` is justified.

## Commands and results

Commands ran on 2026-07-12 in this worker clone. Lean used only existing pinned `.lake` artifacts;
no update, build, dependency clone, or fetch was performed.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0579/Statement.lean` | 0 | Frozen target and checked alternate encoding re-elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0579/AnchorAudit.lean` | 0 | Seven supporting mathlib/object-model probes elaborated |
| `cd Formalizations/Lean && lake env lean /tmp/thm0579_probe.lean` where the probe imports the Poincare module and runs `#print axioms` and `#print` on `SimplyConnectedSpace.nonempty_homeomorph_sphere_three` | 1 | Both commands reported `Unknown constant`, confirming the source marker is not retained; expected negative probe |
| `python3 Stage1_Instances/THM-M-0579/check_anchor_audit.py` | 0 | Frozen target hash, five candidates, source hashes, dependency pins, `proof_wanted` semantics, and noncompletion boundary agreed |
| `rg -n -i 'Poincar[eé].{0,40}(conjecture\|sphere)\|nonempty_homeomorph_sphere_three\|homeomorph.{0,40}sphere.{0,40}three' Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages --glob '*.lean'` | 0 | Located the pinned statement marker, legacy statement/audit artifacts, and no retained terminal 3D proof body |
| Sourcegraph public Lean query for `PoincareConjecture3`, `nonempty_homeomorph_sphere_three`, or `Poincare conjecture` | 0 | `matchCount=0`; response SHA-256 `e24f6e40609cfb3a1f96ce20855477cc0108ebe1e11b1d8a111c8b07ed1f61db` |
| GitHub REST repository search for quoted `Poincare conjecture` plus `Lean 4` | 0 | `total_count=0`, `incomplete_results=false`; response SHA-256 `08c082fdf7ca87ba911a2aabb0f0cf2d3e482a6feeaac9713e4578c20b2600b2` |
| GitHub recursive tree query for `google-deepmind/formal-conjectures@b2e608...` | 0 | Complete 1204-entry tree, one Poincare file at blob `75c16ec...`; response SHA-256 `76fa3f96fc2ff7fc85addfd1e85852dae3fcb5022fc1ef35b030a3dc1e3efc61` |
| GitHub contents query for the Formal Conjectures Poincare file at `b2e608...` | 0 | Source SHA-256 `8c9e44bb2b7fc0a89a7a9198e87e0ca9c4dc35fefd10d3686fa201e28cb6ffe2`; terminal declaration contains `by sorry` |
| GitHub contents query for `LeanMillenniumPrizeProblems@540da9.../Problems/Poincare/Millennium.lean` | 0 | Source SHA-256 `045a97bb2dea46544ca57da7e9e5669c6b160721b1882bc53a8426369352deba`; no terminal 3D proof body |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 structural standard passed for all 1546 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique uniform-L0 targets and ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0579` | 0 | Rank 114, planned, rework required, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0579` | 0 | No whitespace errors |

## Open integration gate

Reopen only for a retained, placeholder-free Lean 4 terminal body at an immutable revision with a
compatible dependency closure and license. It must receive an exact checked transport to
`Stage1Instances.THMM0579.Statement`, kernel elaboration, axiom/trust inspection, and a repo-local
wrapper receipt. This bounded negative audit is not a claim of global nonexistence and is not
theorem completion.
