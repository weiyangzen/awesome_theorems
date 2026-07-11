# Anchor-audit validation record

Item: `S56-M-0010-ANCHOR_AUDIT`  
Base revision: `9c8fbcb508ef94b14b4cc94df3d576550867591d`

## Immutable search and candidate assessment

The dependency manifest pins mathlib to
`8a178386ffc0f5fef0b77738bb5449d50efeea95` and `flt-regular` to
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`. A case-insensitive search for
`Artin-Rees`, `Artin Rees`, `exists_pow_inf_eq_pow_smul`, and
`pow_inf_eq_pow_smul` covered the repository's Lean sources and every package
already materialized at the manifest revisions. It found the historical
repo-local wrapper `AwesomeTheorems.Stage1.S1_M_103.artinRees_mathlib` and one
terminal defining candidate, `Ideal.exists_pow_inf_eq_pow_smul`, in
`Mathlib/RingTheory/Filtration.lean:388`. The two hits in
`Mathlib/RingTheory/AdicCompletion/Exactness.lean` are downstream invocations,
not independent candidates. No hit occurred in `flt-regular` or another pinned
external package.

The historical wrapper is tracked at base revision
`9c8fbcb508ef94b14b4cc94df3d576550867591d`. It delegates immediately to the
mathlib theorem, so it is an alias of the same terminal proof body, not a second
independent proof. Under the uniform L0 rule it is discovery input only and
inherits no rev-5.6 proof or acceptance credit.

The declaration has exactly the Artin-Rees equality, assumptions, and lower
bound frozen by the statement node. Its source body calls the stable-filtration
route directly. Git blame at the pinned tree attributes lines 388-390 to
immutable mathlib commit `c639b48cbbee`. The local wrapper in `AnchorAudit.lean`
repeats the frozen target expression exactly (the dossier's hyphenated path is
not an importable Lean module name) and checks that the candidate inhabits it
without transport by an unproved premise. Lean reports only `propext`, `Classical.choice`, and
`Quot.sound` for both the upstream declaration and wrapper.

## Commands and results

All commands ran in this automation clone. No update, fetch, build, or other
mutation of `.lake` was performed.

| Command | Exit | Result |
|---|---:|---|
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | exact manifest revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -ni 'artin.?rees|exists_pow_inf_eq_pow_smul|pow_inf_eq_pow_smul' Formalizations/Lean/.lake/packages Stage1_Instances Formalizations/Lean -g '*.lean' -g '*.md'` | 0 | historical repo wrapper, one mathlib definition, two downstream mathlib uses, and no distinct external candidate |
| `git -C Formalizations/Lean/.lake/packages/mathlib blame -L 388,390 -- Mathlib/RingTheory/Filtration.lean` | 0 | all declaration lines originate at `c639b48cbbee` |
| `lake env lean AwesomeTheorems/Stage1/S1_M_103.lean` | 0 | tracked historical wrapper and its declared supporting anchors elaborated from source without building the library |
| `lake env lean ../../Stage1_Instances/THM-M-0010/AnchorAudit.lean` | 0 | exact mathlib wrapper elaborated; upstream and audit-wrapper axiom reports were `[propext, Classical.choice, Quot.sound]` |
| `python3 -m json.tool Stage1_Instances/THM-M-0010/anchor-audit.json` | 0 | structured audit receipt is valid JSON |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard and 1546-target coverage check passed |
| `python3 scripts/stage1_target.py check` | 0 | ordered 1546-target manifest check passed |
| `git diff --check -- Stage1_Instances/THM-M-0010 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

This completes the candidate inventory and the smallest exact-type/trust check
for the assigned audit node, pending master acceptance. The wrapper demonstrates
candidate feasibility but receives no proof-node credit here. Obligation-tree,
proof, validation, release, independent-review, and theorem-completion gates
remain open.
