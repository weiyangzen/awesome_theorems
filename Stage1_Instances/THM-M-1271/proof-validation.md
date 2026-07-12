# THM-M-1271 proof-phase validation

Item: `S56-M-1271-PROOF`

Date: 2026-07-12 (Asia/Shanghai)  
Base revision: `a1b16ca3ed65db2ec65e3d478d1680d9c1f5489d`

## Implemented proof bodies

`Proof.lean` kernel-checks these substantive nodes without `sorry`, `axiom`,
or an assumed theorem root:

- `M1271-L-SPHERE-CROSSING`: intermediate-value proof that an admissible path
  meets the sphere of radius `rho`.
- `M1271-C-PATH-MAX` / `M1271-T-BARRIER`: compact-image boundedness, `sSup`
  membership, and `sInf` order yield the complete
  `MountainPassBarrierPackage`.
- `M1271-L-PS-COMPACT` / `M1271-L-LIMIT-PASSAGE`: a canonical
  Palais-Smale sequence has a convergent subsequence; continuity of `Phi` and
  `fderiv` gives an exact critical point at its limiting value.
- `M1271-T-CRITICAL`: checked composition from the still-explicit sequence
  construction premise to `MountainPassCriticalPackage`.

The only remaining mathematical cut is `M1271-C-PS-SEQUENCE`: construct a
sequence at `MountainPassLevel Phi e` whose functional values converge to that
level and whose derivative norms converge to zero. The pinned dependency audit
found no deformation lemma or Ekeland variational principle providing this.
Consequently the exact canonical root remains open and this proof phase is
**blocked**, not self-tested complete. No `.stage1-worker-selftest.json` is
written.

## Exact validation

Run from `Formalizations/Lean` (the temporary local modules are removed after
the check):

```bash
lake env lean -R ../.. -o ../../Stage1_Instances/THM-M-1271/Statement.olean ../../Stage1_Instances/THM-M-1271/Statement.lean
LEAN_PATH=../../Stage1_Instances/THM-M-1271 lake env lean -R ../.. -o ../../Stage1_Instances/THM-M-1271/ObligationTree.olean ../../Stage1_Instances/THM-M-1271/ObligationTree.lean
LEAN_PATH=../../Stage1_Instances/THM-M-1271 lake env lean -R ../.. ../../Stage1_Instances/THM-M-1271/Proof.lean
rm -f ../../Stage1_Instances/THM-M-1271/Statement.olean ../../Stage1_Instances/THM-M-1271/ObligationTree.olean
```

Result: exit 0. All five `#print axioms` probes report only `propext`,
`Classical.choice`, and `Quot.sound`; none reports `sorryAx`. Lean emits two
non-fatal unused-section-variable linter warnings.

Additional checks:

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 1546 uniform-L0 targets and assurance structure valid |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1271` | exit 0; rank 164, planned, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1271` | exit 0; no output |
| `rg -n "sorry\|admit\|placeholder" Stage1_Instances/THM-M-1271/Proof.lean` | exit 1; no matches (the `#print axioms` commands intentionally contain the word `axioms`) |

`Proof.lean` SHA-256 at validation:
`f96bc82f3a7e8fbb4d9d4b3aa8ec27db6505a5a9dd0b9fc5dfb40698cf955869`.

Status boundary: this artifact is genuine partial proof progress. It supplies
no theorem-completion, validation-phase, release, or master-acceptance claim.
