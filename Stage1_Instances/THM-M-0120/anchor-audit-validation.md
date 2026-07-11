# THM-M-0120 anchor-audit validation

Item: `S56-M-0120-ANCHOR_AUDIT`  
Date: 2026-07-12  
Base revision: `304123cb0513eac404230aea1ab7c608db1cb55e`

## Decision

The frozen exact target is present locally as a proposition but has no proof body. The legacy
`S1_M_039` artifact is only an opaque parameterized statement shape and historical search ledger;
uniform L0 rework gives it no proof or audit credit. At immutable mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, the generic scheme, properness, topology,
finite-dimensional-space, and field APIs used to represent the statement elaborate. A full-source
search finds none of the specific klt-pair, numerical-curve, Mori-cone, cone-theorem, or
extremal-ray interfaces needed to state an upstream candidate, much less prove the root.

Three separate Sourcegraph public Lean searches returned zero matches for Mori-cone,
cone-theorem/extremal-ray, and klt-pair identifiers. Two GitHub repository searches returned zero
repositories. GitHub code search was rate-limited with HTTP 403, so that lane is recorded as
blocked rather than turned into negative evidence. No external candidate repository was therefore
available to audit at a commit, pin, or integrate. The dated discovery responses are content-hashed
in `anchor-audit.json`; absence is not claimed globally.

The machine boundary remains `M3`: exact statement elaborated, required formal vocabulary and all
four root conclusion branches open. This receipt completes only the assigned bounded candidate
inventory pending master acceptance. It does not change H/R status and does not claim proof, full
audit completion, or theorem completion.

## Commands and results

All commands ran in this worker clone. Lean used the existing pinned `.lake` closure. No update,
fetch, clone, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0120` | 0 | rank 39, planned, hard-mathlib-anchor lane, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | exact manifest pin `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty; dependency checkout clean |
| `lake env lean ../../Stage1_Instances/THM-M-0120/Statement.lean` from `Formalizations/Lean` | 0 | frozen target and mutations elaborated; exact target expression printed |
| `lake env lean ../../Stage1_Instances/THM-M-0120/AnchorAudit.lean` from `Formalizations/Lean` | 0 | all eight pinned mathlib support declarations elaborated |
| `python3 Stage1_Instances/THM-M-0120/check_anchor_audit.py` | 0 | local sources and hashes, clean pin, probes, vocabulary absence, and M3 boundary agreed |
| three Sourcegraph stream searches recorded in `anchor-audit.json` | 0 | each completed with `matchCount=0`; response hashes recorded |
| two GitHub repository API searches recorded in `anchor-audit.json` | 0 | both returned `total_count=0`, `incomplete_results=false` |
| GitHub code-search API for `MoriCone language:Lean` | 22 | HTTP 403 rate limit; explicitly retained as a search limitation |
| `python3 -m json.tool Stage1_Instances/THM-M-0120/anchor-audit.json` | 0 | structured ledger valid |
| `git diff --check -- Stage1_Instances/THM-M-0120` | 0 | no whitespace errors |

The remaining root cut set is concrete: formalize or pin klt and numerical-intersection
infrastructure; prove the negative-ray decomposition and bounded rational generators; prove local
finiteness; and construct the universal contraction of each listed ray.
