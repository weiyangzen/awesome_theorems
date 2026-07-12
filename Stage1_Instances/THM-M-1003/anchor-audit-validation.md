# Anchor-audit validation record

Item: `S56-M-1003-ANCHOR_AUDIT`  
Base revision: `2c6761e363b5a57450403b79966a76702e940c3b`

## Result

The exact repo-local artifact remains a proposition definition, so it is `M3` and supplies no
proof body. The historical `S1_M_283` file is useful discovery input but only wraps a.e.
convergence, `MemLp` of `Filtration.limitProcess`, and the `p = 1` uniformly-integrable endpoint.
It neither matches nor proves the frozen root.

Pinned mathlib at `8a178386ffc0f5fef0b77738bb5449d50efeea95` provides the same partial
martingale anchors. Its generic Vitali theorems yield `L^p` convergence from a.e./in-measure
convergence plus `UnifIntegrable` at the same exponent. The frozen target supplies only a uniform
bound on the `L^p` norms; that is not the missing same-exponent uniform-integrability premise.
No terminal declaration composes these surfaces into the root. The audit therefore classifies the
exact root as `M4`, while retaining the checked mathlib declarations as partial/support anchors.

The bounded external search found two relevant Lean 4 repositories. At
`Robby955/formal-martingales@1e49307ce983fe472b35400a79052bb607298123`, the complete 31-entry
tree contains finite-horizon Doob and Ville inequalities but no convergence theorem. At
`SmaniaD/Burkholder@afa97ef3c85697fa3b2a67af89af8d6dd09eda69`, the related terminal theorem is
the pointwise-in-time `Lp_Burkholder_inequality_martingaleTransform`, not martingale convergence.
Both use Lean `v4.30.0-rc2` and different mathlib revisions. Their immutable source snapshots were
inspected without installing dependencies or mutating `.lake`; neither is an integration
candidate. Authenticated GitHub code search was unavailable, so no global-absence claim is made.

## Commands and results

Commands ran on 2026-07-12 in this worker clone. Lean used only the existing pinned `.lake`
artifacts. No update, build, dependency clone, fetch, or installation was performed.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1003/AnchorAudit.lean` | 0 | Ten pinned declarations elaborated; four selected axiom sets printed |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1003/Statement.lean` | 0 | Frozen exact target and statement transport re-elaborated |
| `python3 Stage1_Instances/THM-M-1003/check_anchor_audit.py` | 0 | Audit boundary, inventory probes, legacy names, manifest pin, and installed mathlib HEAD agreed |
| `rg -n -i 'martingale convergence|Lp martingale|L\\^p.*martingale|martingale.*L\\^p' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | Only the L1 convergence module/documentation matched; no terminal full-Lp declaration matched |
| `rg -n 'tendsto_Lp_finite_of_tendsto_ae|tendstoInMeasure_iff_tendsto_Lp_finite|memLp_limitProcess' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | Located and cross-read the partial martingale and generic Vitali support declarations |
| Sourcegraph stream queries for exact Lp-martingale phrases and declaration names | 0 | No terminal candidate returned by the bounded public-index queries |
| GitHub REST repository queries for martingale Lean 4 projects | 0 | Located the two relevant repositories audited above; exact quoted convergence queries returned zero repositories |
| immutable GitHub tree/source inspection of the two named commits | 0 | Complete formal-martingales tree and both source archives inspected; no exact target declaration; no `sorry`, `admit`, or declared `axiom` in project Lean sources |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and 1546-target projection passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets, all uniform L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1003` | 0 | rank 283, planned, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1003/anchor-audit.json >/dev/null` | 0 | Audit JSON valid |
| `git diff --check -- Stage1_Instances/THM-M-1003` | 0 | No whitespace errors |

## Open integration gate

Reopen only for a concrete immutable Lean 4 theorem with an exact-type transport and audited
terminal body, or for a local construction of the missing same-exponent bridge and its composition
with the pinned a.e./Vitali surfaces. This audit does not advance proof, validation, or release.
