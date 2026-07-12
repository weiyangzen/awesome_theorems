# Anchor-audit validation record

Item: `S56-M-1045-ANCHOR_AUDIT`  
Base revision: `0ef9fcf1c0a7fb2521adb0cd3bbce55a6285c80d`  
Audit date: 2026-07-12

## Decision

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` supplies the exact low-level
absolute-continuity, Radon-Nikodym, mutual-singularity, measure-map, `L2`, and real-Gaussian APIs
used by the frozen statement. It also has the strict finite-dimensional subcase
`gaussianReal_map_add_const`. The pinned source has no Wiener-measure construction, Paley-Wiener
integral, Cameron-Martin-space characterization, Gaussian quasi-invariance theorem, or
non-admissible singularity theorem. `AnchorAudit.lean` directly elaborates ten retained interfaces;
none is presented as a terminal result.

The legacy `S1_M_238.lean` file is not the root proof. Its general wrapper projects the desired
facts from fields of `CameronMartinModel`, and its concrete theorem covers only a one-dimensional
standard Gaussian shift. Those checked bodies are useful discovery inputs but do not match the
frozen continuous-path iff/density/singularity target.

The strongest external substrate is `RemyDegenne/brownian-motion` at immutable commit
`bdf5ea0c34f9e6d75bce5f0609a968d6e9e99e8e`. Its complete content-addressed archive constructs
Brownian motion and `wienerMeasure`. A whole-archive semantic-name scan found no Cameron-Martin,
Girsanov, quasi-invariance, RN-derivative, mutual-singularity, or Paley-Wiener declaration. It uses
Lean 4.31 and mathlib `fabf563...`, and is absent from the local manifest. The second Brownian
repository returned by the public repository query, `banr1/tailored-brownian-motion` at
`5f7e474...`, likewise has no terminal candidate and uses Lean 4.28-rc1. Neither creates an
integration obligation because neither contains an exact closure.

The root therefore remains `M3 / formalization_debt`. This bounded candidate audit is self-tested,
but `audit_complete` remains false because later obligation, provenance, trust, and human-source
nodes are not part of this phase. It is not theorem completion or a claim of globally exhaustive
search: authenticated GitHub code search was unavailable.

## Commands and results

Commands ran inside this worker clone. Lean used the existing canonical `.lake` artifacts. No Lake
update/build, dependency fetch/clone, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1045/AnchorAudit.lean` | 0 | ten pinned support interfaces elaborated and printed |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1045/Statement.lean` | 0 | frozen exact statement and checked transport re-elaborated |
| `python3 Stage1_Instances/THM-M-1045/check_anchor_audit.py` | 0 | structured classification, target fingerprint, probes, manifest pin, and installed mathlib HEAD agree |
| pinned mathlib semantic `rg` search over all Lean sources | 0 | only supporting RN/Gaussian APIs and legacy metadata hits; no exact terminal theorem |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | commit `8a1783...a95`, tree `bdc39a...2b` |
| GitHub repository API queries for five alias families | 0 | counts `0, 0, 0, 2, 0`, each with `incomplete_results=false` |
| `git ls-remote` plus content archives for both Brownian repositories | 0 | immutable commits confirmed; archive hashes `de1fad...2cd` and `e8eeb6...88a` |
| whole-archive semantic search of `RemyDegenne/brownian-motion@bdf5ea...` | 1 | expected no-match exit for all terminal target aliases; Brownian/Wiener declarations separately inventoried |
| whole-archive semantic search of `banr1/tailored-brownian-motion@5f7e47...` | 0 | only blueprint prose about Wiener measure; no terminal Lean declaration |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and 1546-target projection passed |
| `python3 scripts/stage1_target.py check` | 0 | all 1546 targets and uniform L0 baseline passed |
| `python3 scripts/stage1_target.py show THM-M-1045` | 0 | rank 238, planned, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1045/anchor-audit.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1045 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Open cut set

Future proof work must construct or integrate a concrete `WienerData`, construct its Paley-Wiener
pairing, prove the exact positive-sign density and both absolute-continuity directions, prove
singularity outside the Cameron-Martin space, and compose and trust-audit those bodies. Human-source
status remains `H1`, readability remains `R3`, and no proof or theorem-completion credit is granted.
