# THM-M-1278 proof-phase validation

Item: `S56-M-1278-PROOF`. Base revision:
`35d23d0193cd7c8fccb1d09f22534c6eba066b02`.

## Implemented Bodies

`exists_subtract_mean` closes the exact frozen construction interface by selecting the smooth
ambient extension `u.extension - mean u`. `dirichletEnergy_subtractMean` proves energy invariance
for that selected witness: subtracting a constant leaves the ambient gradient, tangential
projection, integrand, and integral unchanged.

Lean checked both bodies without placeholders or added axioms. Each declaration reports exactly
`propext`, `Classical.choice`, and `Quot.sound`. These are two local obligation bodies, not the
sharp analytic estimate or a terminal root proof.

The frozen obligation module uses a separate nominal copy of the statement structures and has no
checked bridge to the canonical `OnofriInequality`. Validation therefore credits only the two
frozen obligation-tree nodes, not a direct canonical-namespace closure.

## Validation Record

Commands ran from the worker clone on 2026-07-14. Lean output was written only to a disposable
directory under `/tmp`, removed on exit. The proof replay used direct pinned Lean with explicit
existing compiled-package paths and did not invoke Lake or perform dependency operations.

| Command | Exit | Result |
|---|---:|---|
| `bash Stage1_Instances/THM-M-1278/check_proof.sh` | 0 | Frozen obligation module and partial proof elaborated at trust zero; both credited declarations reported exactly `[propext, Classical.choice, Quot.sound]` |
| `python3 Stage1_Instances/THM-M-1278/check_proof.py` | 0 | Receipt hashes, frozen fingerprints and denominator, partial-closure boundary, and prohibited devices passed |
| `python3 Stage1_Instances/THM-M-1278/check_obligation_tree.py` | 0 | Frozen 15-obligation, 54-edge architecture and M3 root cut passed |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-1278` | 0 | Rank 449; planned L0/rework-required target; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1278/check_anchor_audit.py` | 0 | Pinned negative anchor disposition and 11 Lean probes passed |
| `python3 -m json.tool` on the three new proof JSON files | 0 | All structured proof artifacts parsed |

`check_statement.py` was not rerun: it invokes Lake, while concurrent activity left the shared
`flt-regular` dependency checkout in flux during this proof-phase run. The frozen statement source
hash was checked by `check_proof.py`, and the direct trust-zero replay elaborated the identical
obligation encoding needed by the two credited bodies. This proof receipt does not upgrade or
reissue statement-phase evidence.

First failed gate: `M1278-L-SHARP-ONOFRI`. The remaining root cut is
`M1278-L-SHARP-ONOFRI`, `M1278-S-AREA`, and `M1278-S-FINITE`. The root remains M3;
master acceptance, validation, release, audit completion, and theorem completion remain open.
