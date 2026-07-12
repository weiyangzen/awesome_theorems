# THM-M-1083 obligation-tree validation

Item: `S56-M-1083-OBLIGATION_TREE`  
Validation date: `2026-07-12`  
Base revision: `8875e7e449ea94d832c4e6dfa20c9d4e240bca79`

## Frozen architecture

Registry version 1 contains 20 unique semantic obligations. Eighteen are machine-required;
`M1083-X-SOURCE` is a human-source overlay; `M1083-X-EXTERNAL` and `M1083-X-PROVENANCE` are
informational candidate/provenance overlays. None can earn proof credit. Eligibility was assigned from the multiscale
Kolmogorov-Chentsov architecture before closure status was recorded.

The route explicitly contains statement boundaries, the dimension-one covering estimate,
multiscale branches and finite-net construction, Markov and Borel-Cantelli estimates, pathwise
Cauchy limits, construction of one fixed-time modification, dense-net Holder control, extension to
all times, and exact root composition. The known external `exists_modification_holder` theorem is a
separate version/provenance bridge rather than a hidden terminal proof.

The frozen denominator digest is
`06ca47d90b0a7af9d99c935d0c7766cea3df5e722f08b563d226d7736baf6a50`. Seven typed graphs contain
76 reciprocal-indexed edges, with proof, refinement, provenance, evidence, trust, documentation,
and workflow roles kept separate. Per-node validation recipes are frozen in
`validation-specs.json`.

`ObligationTree.lean` checks only the final conditional composition interface. Its `engine`
argument is the complete open proof package; it is not a proof body and closes no obligation.

## Commands and results

Commands ran in this worker clone. Lean reused the existing pinned Lake environment; no dependency
update, build, clone, or fetch was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1083/build_obligation_artifacts.py` | 0 | built 20 obligations; printed the denominator digest above |
| `python3 Stage1_Instances/THM-M-1083/check_obligation_tree.py` | 0 | PASS; 20 obligations, 76 typed edges, open M3 root |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1083/ObligationTree.lean` | 0 | exact conditional root-composition declaration elaborated |
| `python3 -m json.tool` on all three generated JSON artifacts | 0 | obligation registry, typed graphs, and validation recipes are valid JSON |
| `rg -n '\b(sorry\|admit\|sorryAx\|axiom)\b' Stage1_Instances/THM-M-1083/{Statement,AnchorAudit,ObligationTree}.lean` | 1 | expected no-match exit; executable Lean artifacts contain no prohibited declaration |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1,546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546 |
| `python3 scripts/stage1_target.py show THM-M-1083` | 0 | rank 525; planned; L0/rework-required; theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1083 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Open-root boundary

No semantic obligation has an accepted terminal proof body. The external candidate remains absent
from the pinned local dependency closure and was not fetched. Root machine debt is `M3`; source
pinpoint review remains open and readable reconstruction remains `R4`. This packet self-tests only
the obligation registry and typed architecture pending master acceptance. It does not claim `H0`,
`M0`, `R0`, `AUDIT-Z`, root closure, or theorem completion.
