# Anchor audit validation record

Item: `S56-M-0986-ANCHOR_AUDIT`  
Base revision: `1d8a539081efa179b9394093ae54c756f3e17ea4`  
Cutoff: `2026-07-12T00:00:00+08:00`

## Result

The pinned mathlib revision contains no separately named weak-law theorem, but it contains the
stronger `ProbabilityTheory.strong_law_ae`. Together with
`MeasureTheory.tendstoInMeasure_of_tendsto_ae`, it proves the exact frozen real-valued conclusion.
`AnchorAuditCheck.lean` is the narrow checked adapter, rather than a theorem-completion claim.

The older `S1_M_266.lean` independently contains the same route in a Banach-valued wrapper. It is
recorded as immutable discovery input at the worker base revision, not inherited acceptance. The
terminal proof body is in pinned mathlib, so the exact Real specialization is an `M0-W` candidate,
not a repo-local `M0-L` body. `#print axioms` reports only `propext`, `Classical.choice`, and
`Quot.sound`; it reports no undeclared theorem assumption.

## Commands and results

Commands using Lake ran from `Formalizations/Lean`; all others ran from the repository root.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and 1546-target projection pass |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered uniform-L0 targets pass |
| `python3 scripts/stage1_target.py show THM-M-0986` | 0 | rank 266; planned; theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned mathlib tree clean |
| `rg -n -i 'weak[_ -]?law\|khin(ch\|t)in\|khintchine\|law[_ ]of[_ ]large[_ ]numbers' Formalizations/Lean/.lake/packages --glob '*.lean'` | 0 | mathlib strong-law module and convergence-in-measure documentation only; no separately named weak-law terminal |
| `lake env lean ../../Stage1_Instances/THM-M-0986/AnchorAuditCheck.lean` | 0 | exact adapter elaborates; axioms are `propext`, `Classical.choice`, `Quot.sound` |
| `lake env lean AwesomeTheorems/Stage1/S1_M_266.lean` | 0 | immutable historical wrapper elaborates in the pinned environment |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| anonymous GitHub repository search for the three recorded queries | 0 | each returned `total_count: 0`; response SHA-256 `08c082fdf7ca87ba911a2aabb0f0cf2d3e482a6feeaac9713e4578c20b2600b2` |
| anonymous grep.app code search for four aliases | 22 | HTTP 429 for every request; recorded as access failure, not as absence evidence |
| `python3 -m json.tool Stage1_Instances/THM-M-0986/anchor-audit.json >/dev/null` | 0 | structured audit is valid JSON |
| `rg -n '\bsorry\b\|\baxiom\b\|\badmit\b' Stage1_Instances/THM-M-0986 --glob '*.lean'` | 1 | no forbidden Lean declarations or placeholders |
| `git diff --check -- Stage1_Instances/THM-M-0986 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Limits

Anonymous GitHub code search was not available, and grep.app rate-limited all requests. Thus this
is a classified audit of the frozen local and pinned dependency inventory plus documented public
index attempts, not an exhaustive-discovery claim. The human source remains `H1`; no immutable scan,
translation, assumption crosswalk, or errata review was added. Obligation-tree, proof acceptance,
full transitive provenance, hermetic validation, independent replay, and release remain downstream.
