# THM-M-0122 proof-phase attempt

Item: `S56-M-0122-PROOF`

Intent: `prove`

Base: `307c34d30fc3763c82a944a142ae922b48ff18aa`

## Verdict

`blocked`. The exact target remains open.

The authoritative theorem-DAG parent closure, reuse hints, and shared groups
are all empty. The prescribed `parent_inspection_order` was therefore
traversed exactly once as the empty sequence before proof work. The refreshed
`dependency-reuse-ledger.json` binds graph SHA-256
`8be71ef1e4fa1c3de5aa420550ff915dbe0b9f165ac0d98518adf2d1fe25fd47`
and context SHA-256
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.
No provider bytes, receipt, or checkbox acceptance are consumed.

`Proof.lean` adds three genuine target-owned, sorry-free bodies. Two implement
the final set-theoretic injection transports. The third concludes the exact
canonical `FaltingsTarget`, but only from the three package propositions
already frozen by `ObligationTree.lean`. It is conditional composition, not a
premise-free proof of Faltings' theorem.

The first mathematical failure is `P04-KERNEL.M0122-N-FINITE-EXTENSION`.
The remaining machine root cut is:

- `M0122-N-FINITE-EXTENSION`
- `M0122-C-ABEL-JACOBI`
- `M0122-L-MORDELL-WEIL`
- `M0122-L-MORDELL-LANG`
- `M0122-L-NO-POSITIVE-COSET`
- `M0122-L-FINITE-INTERSECTION`

A bounded scan of all 9,676 installed pinned Lean sources found no terminal
Faltings, Mordell-Lang, Abel-Jacobi, or Mordell-Weil package. The only exact
Mordell-Weil spelling is explanatory prose in `Mathlib.GroupTheory.Descent`.
The already audited external Faltings candidate is Q-only, materially
mismatched, and directly `by sorry`.

The proof phase contract does not allow partial bodies or a negative finding
to satisfy the complete assigned phase predicate. In addition, neither
`check_proof.py` nor `check_proof.sh` existed at this worker base. Because the
HEAD contract requires the sole validator candidate to have existed at the
base with unchanged bytes, a worker-created validator cannot make this claim
review-eligible. This is a target-scoped handoff, not a state transition.

## Validation

The following checks ran in this worker clone using the existing pinned
`.lake` artifacts read-only. No update, build, clone, fetch, checkout, or
network operation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 1 expected | Target-owned proof artifacts make the checked-in theorem-DAG evidence inventory stale; only the integration lane may regenerate that read-only authority projection. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 1 expected | Fresh deterministic generation sees the new proof artifacts, so the checked-in read-only projection differs until integration. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1..1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0122` | 0 | Rank 41, planned lifecycle, theorem incomplete. |
| Isolated `lake env lean --trust=0 -t0` replay of `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` | 0 | All three proof declarations are sorry-free and report exactly `propext`, `Classical.choice`, and `Quot.sound`. Proof stdout SHA-256: `fb39843cb284e2a02ec84fb3449f4759358ff524799a36b5f654d3e21b967a55`. |
| Prohibited-construct scan over target-owned Lean sources | expected no match | No executable `sorry`, `admit`, `sorryAx`, bodyless axiom/constant, unsafe/opaque/extern declaration, `implemented_by`, or `native_decide`. |
| Exact-name scan across installed pinned Lean sources | expected one prose-only match | Only the Mordell-Weil prose line in `Mathlib.GroupTheory.Descent`; no terminal package. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0122/check_proof.py` | 0 | Emitted exactly one `stage1-validator-semantic-result/1.0` JSON object with `status=blocked`, `phase_predicate_proven=false`, and `phase_accepted=false`. |
| `git diff --check -- Stage1_Instances/THM-M-0122 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

`audit_complete=false` and `theorem_complete=false`. The lifecycle and root
debt remain unchanged. Resume only after the exact missing package bodies or a
compatible immutable proof source becomes available, and after integration
provides a HEAD-tracked proof validator for a fresh claim.
