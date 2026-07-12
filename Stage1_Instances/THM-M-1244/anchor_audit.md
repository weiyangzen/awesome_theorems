# Anchor audit

This audit is for `S56-M-1244-ANCHOR_AUDIT`. It compares candidates against the frozen
`Stage1Instances.THM_M_1244.GaussianLogSobolevTarget`; it does not broaden the target and does not
claim a theorem proof.

## Pinned mathlib

The dependency manifest pins mathlib at
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. A case-insensitive search of every Lean source in that
package for the recorded log-Sobolev names and Gaussian/entropy combinations found no terminal
logarithmic Sobolev theorem. Mathlib does supply the measure and integration infrastructure used by
the statement, including `gaussianReal`, `Measure.pi`, and `MemLp.integrable_sq`. Those are supporting
APIs, not a proof anchor.

The older repo-local `S1_M_279.lean` is also only a discovery record. It names an external project
but does not import its declarations and therefore supplies no machine credit.

## External Lean 4 candidate

The strongest located candidate is Yuanhe Zhang, Jason D. Lee, and Fanghui Liu's
`lean-stat-learning-theory`, audited at signed Git commit
`7b82b1323c80f0c21ca449fd12e1c24315ae9782` (tree
`cadf7aacaa985a23249e2616a4417372d4542fd2`). In
`SLT/GaussianLSI/TensorizedGLSI.lean` (Git blob
`2681f02ad1af5edb23b82e824263e82d2999c7e0`, SHA-256
`22eefaf07248a28de214b07154ecd953e50ed7c9432931ac9e2fe34ea9c45e29`), theorem
`GaussianLSI.gaussian_logSobolev_W12_pi` proves a dimension-free product-Gaussian inequality with
constant `2`. The terminal declaration has a `by` proof body. No `sorry`, `axiom`, or `admit` token
was observed in that candidate file. Its sources carry Apache-2.0 headers.

This is not an exact candidate for the frozen target. Most importantly, upstream uses
`sum_i (fderiv f x (Pi.single i 1))^2`, whereas the canonical target uses `||fderiv f x||^2` for
Lean's product norm on `Fin n -> Real`. These expressions are not definitionally or mathematically
equal in general; `AnchorAudit.lean` checks that Lean rejects their definitional identification.
For the functional `x ↦ x 0 + x 1` under the product sup norm, the squared operator norm is `4`
while the coordinate-square sum is `2`, giving a concrete mathematical separator. Regularity and
integrability premises also differ, and neither the measure nor entropy encodings have a checked
repo-local bridge.

The upstream project pins Lean `v4.27.0-rc1` and mathlib
`d68c4dc09f5e000d3c968adae8def120a0758729`, while this repository uses Lean `v4.29.0` and mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. It is absent from this Lake manifest. Per the worker
rules it was not fetched or added, so it remains `external_upstream_anchor_only`, not M0 evidence.

## Verdict

The immutable candidate inventory is complete for this phase, but there is no exact repo-local
anchor. The current debt is `formalization_debt`, not repo-local integration debt: the located
external theorem cannot close the frozen operator-norm target through a faithful wrapper. The next
phase must either preserve this mismatch as an explicit proof obligation or send the statement back
for a separately accepted correction to an actual Euclidean squared-gradient encoding. Root state
remains `M4`; theorem completion is false.

## Validation record

Base revision: `c00bc6793b3d4c186b81b80bbaf165b32e125b58`.

The pre-existing untracked canonical `.lake` link was reused read-only. No update, build, clone, or
fetch command was run.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 1546 uniform-L0 Lean 4 targets; assurance standard valid
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546
python3 scripts/stage1_target.py show THM-M-1244
  exit 0: rank 425, planned, L0/rework-required, theorem_complete false
rg -n -i --glob '*.lean' 'logarithmic[ _-]*sobolev|log[ _-]*sobolev|logsobolev|sobolev.*entropy|entropy.*sobolev' Formalizations/Lean/.lake/packages
  exit 1: no match in pinned dependency Lean sources
curl -fsSL https://github.com/YuanheZ/lean-stat-learning-theory/archive/7b82b1323c80f0c21ca449fd12e1c24315ae9782.tar.gz | tar -xz -C "$tmp"; rg -n --glob '*.lean' '\bsorry\b|\baxiom\b|\badmit\b' "$tmp"/*/SLT/GaussianLSI
  exit 1: no forbidden proof token in the immutable external GaussianLSI source tree
cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1244/AnchorAudit.lean
  exit 0: support APIs elaborate and Lean rejects definitional equality of the energy encodings
python3 -m json.tool Stage1_Instances/THM-M-1244/anchor_audit.json
  exit 0
git diff --check -- Stage1_Instances/THM-M-1244 .stage1-worker-selftest.json
  exit 0
```
