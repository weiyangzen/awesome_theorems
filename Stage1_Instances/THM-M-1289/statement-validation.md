# Statement validation record

Item: `S56-M-1289-STATEMENT`  
Base revision: `22755e611bc984d98b9d6525b69d8d6120b1c4dd`

`Stage1Instances.THM_M_1289.AubinTalentiTarget` freezes the intake-selected normalized bubble,
including positivity, smoothness, the critical PDE, homogeneous Sobolev finiteness, and equality at
the least sharp constant. The stronger classification of all optimizers remains excluded.

All commands ran in this worker clone. Lean ran from `Formalizations/Lean` against the existing
pinned Lake artifacts; no dependency update or fetch was performed.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1289/Statement.lean` | 0 | Target and four deliberately distinct structural mutations elaborated; explicit target printed; stderr empty |
| `sed -n '/^def Stage1Instances.THM_M_1289.AubinTalentiTarget/,$p' /tmp/thm1289.out \| sha256sum` | 0 | Elaborated explicit expression hash `f61848575711c421710615fb16d1febe13fb89e9e57266124c83cebff6ba0a68` |
| `sha256sum ../../Stage1_Instances/THM-M-1289/Statement.lean lean-toolchain lake-manifest.json` | 0 | `39e001...46f0`, `651c8a...1d2`, `321626...2d81` |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C .lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |

This is statement elaboration only, pending master acceptance. It does not establish any theorem
proof, source audit, obligation closure, release validation, or theorem-completion claim.
