# Obligation-tree validation record

Item: `S56-M-1067-OBLIGATION_TREE`  
Validation date: `2026-07-12`  
Base revision: `ceb0a98b07364cde2a40a2bae3b24317916319ef`

## Frozen architecture

Registry version 1 contains 17 unique obligations. Fifteen are machine-required;
`M1067-X-SOURCE` and `M1067-X-PROVENANCE` are informational overlays and cannot earn proof
credit. The frozen route constructs mollified occupation densities, proves uniform moment and
Cauchy estimates, selects one limit field, obtains a jointly continuous version, and extends a
countable determining-class identity to every measurable `ENNReal` test and every nonnegative
time on one common full-measure event.

The denominator digest is
`7a96f4bf13db4217fbfb692216234f150f00b54bd7b0017662acb6895595d5c1`. The root
fingerprint is the SHA-256 of the exact printed elaboration from `Statement.lean`:
`3a760f8d4cb9898c637755e90fc9ca8402c9427103006981081a7378ec46d2e1`.
`typed-graphs.json` separately binds the statement source hash.

Seven typed graphs contain 71 reciprocal edges. Proof, refinement, provenance, evidence, trust,
documentation, and workflow relations remain separate. The structural checker verifies unique
IDs, denominator derivation, source binding, reciprocal edges, acyclic root reachability, local
step budgets of at most 100, composition records, and the fail-closed completion boundary.

`ObligationTree.lean` kernel-checks only two child-to-parent composition interfaces. Every
mathematical child is an explicit hypothesis, so these declarations are not a proof of Brownian
local-time existence and earn no terminal-body credit.

## Commands and results

All Lean commands reused the existing pinned closure. No dependency update, build, clone, fetch,
or `.lake` mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1067/build_obligation_artifacts.py` | 0 | built 17 obligations; printed the denominator digest above |
| `python3 Stage1_Instances/THM-M-1067/check_obligation_tree.py` | 0 | PASS; 17 obligations, 71 typed edges, open M4 root |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1067/ObligationTree.lean` | 0 | both exact composition-interface declarations elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1067/Statement.lean \| sha256sum` | 0 | `3a760f...d7c1  -` |
| `python3 -m json.tool Stage1_Instances/THM-M-1067/obligation-registry.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1067/typed-graphs.json` | 0 | valid JSON |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1,546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546 |
| `python3 scripts/stage1_target.py show THM-M-1067` | 0 | rank 509; planned; theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1067 .stage1-worker-selftest.json` | 0 | no output |

## Open root boundary

No obligation has a terminal proof-body ID or accepted closure evidence. The current implementation
cut includes the Wiener-law interface, moment estimates, compact-field convergence, joint
continuity, determining-class occupation identity, and simultaneous extension. Root debt remains
`M4`; source pinpoint review remains `H2`; readability remains `R4`.

This packet self-tests only the obligation-tree phase pending master acceptance. It does not claim
`H0`, `M0`, `R0`, `AUDIT-Z`, proof completion, validation, release, or theorem completion.
