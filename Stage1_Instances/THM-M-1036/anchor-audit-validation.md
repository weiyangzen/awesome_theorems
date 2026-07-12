# Anchor-audit validation record

Item: `S56-M-1036-ANCHOR_AUDIT`  
Base revision: `bbb17fe085a3545a76988417fdad024a9e9e136a`

## Verdict

The immutable-revision audit found no exact Lean 4 theorem for the frozen
finite-dimensional global-Lipschitz SDE existence-and-uniqueness target.
Pinned mathlib supplies Gaussian-process, adaptedness, and
independent-increments substrate but no Brownian-motion object, general Ito
integral, SDE solution theory, or terminal theorem. The historical
`S1_M_229.lean` artifact is an abstract statement/package boundary and does not
prove its `StatementShape`.

The external `RemyDegenne/brownian-motion` candidate was inspected from the
content-addressed archive of commit
`91885e6172648ea7f9c6a16b3a7069f92c88e023` (archive SHA-256
`74e42a88acbe271a34cba8668ea8bcba8afe38c0818c1de28e42bcd6d53cf20e`).
It has genuine Brownian-motion and early stochastic-integral anchors, but no
SDE existence/uniqueness declaration. Its README calls stochastic integration
and Ito's lemma in progress, and the relevant tree contains 12 `sorry`
occurrences. It also pins Lean `v4.30.0-rc1` and mathlib `f2330612...`, not this
repository's Lean `v4.29.0` and mathlib `8a178386...`.

Therefore no external anchor can be treated as M0 or integrated as a wrapper.
The truthful root remains `[H2, M4, R3]`; theorem completion is false.

## Commands and results

All repository commands ran in this worker clone. The external archive was
expanded only under `/tmp`; no dependency was cloned/fetched and `.lake` was
not modified.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and 1546-target projection passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered L0/rework-required targets passed |
| `python3 scripts/stage1_target.py show THM-M-1036` | 0 | rank 229, planned, theorem incomplete |
| pinned-mathlib `rg` search over `Mathlib/**/*.lean` for the terms serialized in `anchor-audit.json` | 0 | only unrelated phrase matches plus Gaussian/adapted/independent-increment substrate; no terminal SDE/Ito declaration |
| repo-local `rg` search for SDE existence/uniqueness terms | 0 | only the frozen target and historical abstract SDE packages; no proof of the exact target |
| `curl -L --fail https://codeload.github.com/RemyDegenne/brownian-motion/tar.gz/91885e...` | 0 | immutable archive downloaded; SHA-256 `74e42a88...cf20e` |
| external-tree terminal-term `rg` search serialized in `anchor-audit.json` | 1 | no match (ripgrep no-match exit) |
| external stochastic-integral `rg` scan for `sorry`, `admit`, or `axiom` | 0 | 12 `sorry` occurrences; no terminal candidate eligible for proof credit |
| `lake env lean ../../Stage1_Instances/THM-M-1036/AnchorAudit.lean` | 0 | pinned mathlib substrate declarations elaborated; the historical source was audited textually because its `.olean` is absent from the reused build closure |
| `python3 -m json.tool ../../Stage1_Instances/THM-M-1036/anchor-audit.json` | 0 | structured audit is valid JSON |
| scoped forbidden-declaration scan of new owned artifacts | 1 | no `axiom`, `admit`, or Lean `sorry` declaration in the deliverable; 1 is ripgrep's no-match exit |
| `git diff --check -- Stage1_Instances/THM-M-1036 .stage1-worker-selftest.json` | 0 | no scoped whitespace errors |

## Boundary

This completes only the bounded anchor-audit phase, pending master acceptance.
It records adjacent APIs and an actionable integration blocker instead of
inventing a proof. The next proof architecture must retain the Ito-integral,
strong-existence, and indistinguishability obligations as open root cuts.
