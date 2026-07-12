# THM-M-1255 anchor audit

Item: `S56-M-1255-ANCHOR_AUDIT`  
Base revision: `4d48a3c5fbec6d005a64a99338e40c001656264c`

## Decision

The pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` supplies the
distribution, Dirac delta, derivative, Fourier transform, Fourier multiplier, and multivariate
polynomial object layers. It supplies no terminal Malgrange-Ehrenpreis declaration and no arbitrary
nonzero-polynomial division construction. The checked anchors are therefore useful future proof
dependencies, not a proof or wrapper candidate for the frozen root.

The historical `S1_M_160.lean` file is also nonterminal: it constructs interfaces, wrapper lemmas,
and an uninhabited completion-certificate shape, while explicitly leaving the fundamental-solution
construction open. It receives no inherited proof credit.

Public GitHub repository searches for `"Malgrange-Ehrenpreis" Lean` and
`"fundamental solution" PDE Lean theorem` returned zero repositories on 2026-07-11 UTC. Exact-name
and semantic searches over the locally present pinned mathlib `Mathlib/` and `Archive/` trees and
the repository found no other Lean candidate. This is a bounded negative discovery result, not an
assertion that no formalization exists anywhere. Because no exact external candidate was found,
there is no identified upstream proof to pin or an integration blocker to disguise as completion.

The structured candidate inventory, immutable revisions, roles, missing bridges, and state boundary
are in `anchor-audit.json`. `AnchorAudit.lean` independently elaborates the positive mathlib anchors.
The audit classification remains `M3 / not_repo_local_closed`; theorem completion is false.

## Validation

All commands ran in this automation clone. Lean ran from `Formalizations/Lean` using the existing
pinned `.lake` artifacts. No update, build, clone, or fetch was performed.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1255/AnchorAudit.lean` | 0 | three typed wrapper checks and nine object-layer probes elaborated |
| `python3 ../../Stage1_Instances/THM-M-1255/check_anchor_audit.py` | 0 | receipt schema and non-completion boundary valid; installed mathlib HEAD equals the manifest pin; six anchors checked |
| pinned mathlib/repository exact-name and semantic `rg` searches | 0 | no terminal candidate; only unrelated polynomial-division and Pell uses of “fundamental solution” |
| GitHub repository API queries recorded in `anchor-audit.json` | 0 | both searches returned `total_count: 0` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1255` | 0 | rank 160, planned, L0/rework-required, theorem incomplete |
| forbidden-term scan of the executable audit artifacts | 1 | no `sorry`, `admit`, or `axiom` occurrence; exit 1 is ripgrep's no-match result |
| `git diff --check -- Stage1_Instances/THM-M-1255 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This is a self-tested anchor-audit receipt pending master acceptance. It does not close the root,
the source-fidelity question for the tempered strengthening, or any later obligation/proof/release
gate.
