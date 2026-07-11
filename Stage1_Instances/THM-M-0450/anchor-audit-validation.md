# Anchor-audit validation

Item: `S56-M-0450-ANCHOR_AUDIT`  
Base revision: `8909a35bce35ee5c42b643282ec175114622659d`

The audit searched the repository, the locally available pinned mathlib checkout, and public
formal repositories. External source inspection used immutable commit URLs and an immutable
archive; it did not clone, fetch, update, build, or modify any dependency. The archive was placed
under `/tmp` only and is not part of the repository or machine-proof closure.

## Results

Pinned mathlib at `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains the exact Jacobian
point-group instance and `AddCommGroup.fg_of_descent'`. The latter proves finite generation only
after finite-index doubling, a nonnegative Northcott height, and an approximate parallelogram law
are supplied. `AnchorAudit.lean` type-checks this specialization against the frozen point model.
The pinned source has no terminal Mordell-Weil declaration.

`MichaelStollBayreuth/Heights@688bdb63259556fab4b0f699ce0d10bd2dce23f6` is the strongest Lean 4
candidate found. Its `WeierstrassCurve.Affine.weakMW_implies_MW` has an active proof body, but
assumes weak Mordell-Weil and uses a different affine short-Weierstrass model. It therefore cannot
close the exact root. It also targets Lean `v4.30.0-rc2` and mathlib
`6f66e004f0a46a57a8b0d78b28c45e8e74c6d940`, is absent from the local lock, and was not built.
The older Lean 3 repositories either admit the terminal theorem or do not state it.

## Commands

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard valid: 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | manifest valid: 1546 unique ordered targets |
| `python3 scripts/stage1_target.py show THM-M-0450` | 0 | rank 92, planned, rework-required, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a178386...`, tree `bdc39a3...` |
| `git -C Formalizations/Lean/.lake/packages/mathlib grep -n -i -E 'mordell.?weil\|weakMW_implies_MW' HEAD -- '*.lean'` | 0 | only explanatory Mordell-Weil references in `GroupTheory/Descent.lean`; no terminal theorem |
| `sha256sum` on the three audited mathlib files | 0 | hashes recorded in `anchor-audit.json` |
| `curl -L --fail https://github.com/MichaelStollBayreuth/Heights/archive/688bdb63259556fab4b0f699ce0d10bd2dce23f6.tar.gz` then `sha256sum` | 0 | immutable archive SHA-256 `09e8bd85fe5e30f9a9ae5d1fe30bc11f27da05fd75123e770ab0954754333d27` |
| `rg -n -g '*.lean' '\b(sorry\|admit\|axiom\|unsafe)\b' /tmp/thm-m-0450-heights-audit` | 0 | two `sorry` tokens, both inside one block comment in `Heights/NumberField.lean`; none in the candidate terminal path |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0450/AnchorAudit.lean` | 0 | exact object-model, generic descent, and frozen-model specialized descent probes elaborated |
| `python3 -m json.tool Stage1_Instances/THM-M-0450/anchor-audit.json` | 0 | structured receipt valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0450` | 0 | no whitespace errors |

## Verdict

The anchor-audit node is self-tested pending master acceptance. The root remains `[H1, M3, R3]`.
The strongest formal evidence is partial `E3/M3` infrastructure, not an independently reproduced
external proof (`E2/M1`) and not pinned exact closure (`E1/M0-P`). The theorem remains incomplete.
