# Statement validation

Item: `S56-M-1246-STATEMENT`. Base revision:
`7619d195bd4454d4084e74977cf56d86c396ab3a`.

The check reused the pre-existing canonical pinned `.lake` symlink and did not update or fetch any
dependency. Commands were run from the repository root unless a `cd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1246/check_statement.py` | 0 | Exact target elaborated; explicit expression SHA-256 `07f1c030325dfe8d02e99a0af1a00c5241a312e6195aa4a9e2967822960048f1`; all three structural mutations rejected by `fail_if_success` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| Delete each listed import in a temporary copy and run `cd Formalizations/Lean && lake env lean /tmp/m1246-test.lean` | nonzero for each | Each of the three retained imports is necessary; redundant `PiL2` and `Topology.Algebra.Support` imports were removed |
| `python3 -m json.tool Stage1_Instances/THM-M-1246/statement.json >/dev/null` | 0 | Structured statement record parsed |
| `git diff --check -- Stage1_Instances/THM-M-1246` | 0 | No whitespace errors |

This is warm-cache, nonrelease statement evidence. It establishes exact elaboration but not a proof,
anchor acceptance, source fidelity, full dependency/axiom closure, hermetic replay, independent
verification, or master acceptance.
