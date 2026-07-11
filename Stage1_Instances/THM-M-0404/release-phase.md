# THM-M-0404 release reconciliation

Item `S56-M-0404-RELEASE` reconciles the dossier's current provisional
evidence. The exact verdict is `blocked`: lifecycle remains `planned`, the
root remains `[H3, M3, R4]`, and both `audit_complete` and
`theorem_complete` are false. This is a self-tested negative release
decision, not theorem completion or master acceptance.

## Evidence reconciliation

The validation receipt establishes narrow Lean replay for the exact
statement, conditional composition, and the local predicate-level
combinatorial proof. It does not establish Skolem-Mahler-Lech. The declaration
`root_of_eventuallyPeriodicZeroSets` takes
`EventuallyPeriodicZeroSets` as an explicit premise, leaving
`M0404-T-EVENTUAL` as the minimal mathematical open root cut. The frozen graph
also retains a stale open entry for `M0404-L-COMBINATORIAL`; release does not
rewrite that authoritative pre-proof snapshot.

The same evidence fails the cold empty-cache hermetic replay and independent
verification gates. There is no accepted H0/R0 review, complete TCB/SBOM and
license archive, offline restoration, immutable clean release input,
deterministic bundle, second clean runner, independently implemented verifier,
second signed attestation, or master receipt. The prerequisite validation item
is provisional `[_]`, not master-accepted `[x]`.

## Exact command and result

Run from repository root with no dependency update, build, fetch, or clone:

```text
python3 Stage1_Instances/THM-M-0404/validate_release.py
  exit 0
  ok: upstream node-scoped validation replayed against pinned Lean/mathlib
  open: exact root M3; conditional composition is not root closure
  open: audit H3/R4; AUDIT-Z is not established
  blocked: hermetic, supply-chain, independent-verifier, and master-acceptance gates
  verdict: blocked; lifecycle planned; theorem_complete=false; cut M0404-T-EVENTUAL
```

The validator reruns the recorded narrow validation recipe, including
`lake env lean` elaboration in a fresh temporary module directory, and checks
the content hashes and negative gate fields in the validation, registry,
graph, instance, and release records. The first failed theorem-completion gate
is exact root kernel closure. Retry requires a proof of the open
eventual-periodicity package and exact composition; subsequent release also
requires accepted audit evidence, hermetic supply-chain replay, independent
verification, a deterministic bundle, and master acceptance.
