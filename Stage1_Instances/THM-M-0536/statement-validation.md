# Statement validation

Assigned item: `S56-M-0536-STATEMENT`.

Canonical module: `Stage1_Instances/THM-M-0536/Target.lean`.
Canonical declaration: `Stage1.THM_M_0536.HomotopyInvarianceStatement`.
Base revision: `7ebc835c8cb3bb8d31a59476f3e8815026f161d0`.
Lean toolchain: `leanprover/lean4:v4.29.0`.
Pinned mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.

The import list is narrow and explicit. The homotopy-invariance module supplies the singular
homology API; `Homotopy.Equiv` supplies the packaged premise; the three algebra/category modules
supply modules, coproducts, abelianness, and the resulting homology instance. No umbrella `Mathlib`
import is used.

| Command | Result |
|---|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0536/Target.lean` | exit 0; prints `Stage1.THM_M_0536.HomotopyInvarianceStatement : Prop` |
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0536` | exit 0; rank 593, planned, theorem_complete false |
| `git diff --check -- Stage1_Instances/THM-M-0536` | exit 0; no output |

The elaboration checks only the exact proposition. It gives no proof credit. Human-source pinpoint
review, formal-anchor audit, obligation decomposition, proof, axiom/provenance validation, hermetic
replay, and independent review remain known failures. No audit or theorem completion is claimed.
