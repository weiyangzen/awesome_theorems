# Anchor audit

Node: `S56-M-1006-ANCHOR_AUDIT`. Audit date: 2026-07-12. Base revision:
`9d84f229ca62f240f8ad5b6e017c0bfef7b05eae`.

The bounded audit found no exact Lean 4 theorem for the frozen finite discrete-time BDG target.
The full structured inventory, immutable revisions, environment differences, and scope decisions are
in `anchor_audit.json`.

## Candidate decision

| Surface | Immutable revision | Result |
|---|---|---|
| Pinned mathlib | `8a178386ffc0f5fef0b77738bb5449d50efeea95` | `MeasureTheory.maximal_ineq` is the nearest maximal inequality, but it compares a crossing probability with an integral and has no quadratic variation or two-sided moment comparison |
| SmaniaD/Burkholder | `afa97ef3c85697fa3b2a67af89af8d6dd09eda69` | `Lp_Burkholder_inequality_martingaleTransform` is a real adjacent proof for `1 < p < infinity`; it is one-sided and about predictable transforms, so it cannot substitute for `StatementShape` |
| Robby955/formal-martingales | `1e49307ce983fe472b35400a79052bb607298123` | Proves Doob/Ville inequalities, not BDG |
| RemyDegenne/demo-martingales | `faff9d466cead73a91c13798023097e17ac21aef` | Tutorial material only; no BDG declaration |

The Smania development was inspected at immutable raw URLs. Its eight project Lean source files
contained no whole-word `sorry`, `admit`, or `axiom` token, but that fact does not make its different
theorem an exact candidate. It also pins Lean `v4.30.0-rc2` and mathlib `aa7b3adc...`, whereas this
repository pins Lean `v4.29.0` and mathlib `8a178386...`. No dependency was fetched or integrated.

## Human-source boundary

Burkholder (1973), DOI `10.1214/aop/1176997023`, pages 19-42, and Davis (1970), DOI
`10.1007/BF02771313`, pages 187-190, are primary bibliographic anchors. The audit did not obtain an
immutable accessible primary-source copy sufficient for a theorem-number, assumptions, and errata
crosswalk. Human status therefore remains `H2`, not `H0`.

## Validation

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1006/AnchorAudit.lean` | 0 | Pinned Lean printed the types of the nearest mathlib anchors |
| `python3 -m json.tool Stage1_Instances/THM-M-1006/anchor_audit.json >/dev/null` | 0 | Structured receipt is valid JSON |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Rev-5.6 structure passed |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 target identities and ranks passed |
| `python3 scripts/stage1_target.py show THM-M-1006` | 0 | Target is rank 286, L0/rework-required, and theorem-incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1006` | 0 | No whitespace errors |

This completes only the bounded anchor-audit deliverable. It creates no theorem proof, no external
integration, no H0 or M0 credit, and no theorem-completion claim. Master acceptance is required.
