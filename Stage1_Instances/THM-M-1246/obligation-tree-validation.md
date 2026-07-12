# Obligation-tree validation

Item: `S56-M-1246-OBLIGATION_TREE`. Base revision:
`58cde546113e54bfa95299c69db6ee1508316872`.

The validation reused the existing canonical pinned `.lake` symlink. It performed no update, build,
clone, fetch, or network operation. The validator copies the two scoped Lean sources into a
temporary directory under `Formalizations/Lean`, compiles `Statement.olean` there, elaborates the
conditional composition with `lake env lean`, and deletes the temporary directory.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1246/build_obligation_artifacts.py` | 0 | Deterministically generated the registry, seven typed graphs, and validation recipes |
| `python3 Stage1_Instances/THM-M-1246/check_obligation_tree.py` | 0 | PASS: 15 unique obligations, 61 typed reciprocal/support edges, acyclic root proof reachability, denominator SHA-256 `dd6e6ca1fc734ea8f477095e77a99601a3387cd914de7e599c9343b874ae2d6d`, and kernel-elaborated exact conditional composition |
| `python3 Stage1_Instances/THM-M-1246/check_statement.py` | 0 | Exact statement fingerprint remained `07f1c030325dfe8d02e99a0af1a00c5241a312e6195aa4a9e2967822960048f1`; all three structural mutations were rejected |
| `python3 Stage1_Instances/THM-M-1246/check_anchor_audit.py` | 0 | Pinned mathlib, content hashes, four analogue classifications, forbidden tokens, and Lean resolution checks passed |
| `python3 -m json.tool Stage1_Instances/THM-M-1246/obligation-registry.json >/dev/null` | 0 | Registry JSON parsed |
| `python3 -m json.tool Stage1_Instances/THM-M-1246/typed-graphs.json >/dev/null` | 0 | Typed graph JSON parsed |
| `python3 -m json.tool Stage1_Instances/THM-M-1246/validation-specs.json >/dev/null` | 0 | Validation recipe JSON parsed |
| `git diff --check -- Stage1_Instances/THM-M-1246 .stage1-worker-selftest.json` | 0 | No whitespace errors |

This is warm-cache, node-scoped, nonrelease evidence. It freezes the eligibility denominator and
proof architecture and checks only an identity composition from the still-open exact terminal
premise. The remaining minimal root cut is `M1246-T-ANALYTIC`; the root remains M3. No analytic
proof, primary-source acceptance, transitive trust closure, readable reconstruction, hermetic
replay, independent verification, master acceptance, audit completion, or theorem completion is
claimed.
