# THM-M-0387 release decision handoff

## Exact verdict

`S56-M-0387-RELEASE` is `blocked`. Lifecycle remains `planned`, the root vector remains
`H1/M2/R4`, and both `audit_complete` and `theorem_complete` are false. There are no accepted
receipt IDs and no theorem-completion promotion.

The first failed gate is dependency acceptance. `S56-M-0387-VALIDATION` is worker-self-tested
evidence pending master acceptance, not an accepted prerequisite. Even after acceptance, the next
theorem gate fails: the exact root is conditional on `M0387-WTW`, the universal nonregular
odd-prime branch, for which no eligible proof body exists in the pinned closure.

## Reconciliation

The exact natural-number statement re-elaborates, and Lean checks the statement transport,
exponents three and four, regular primes, and the conditional composition from all odd-prime
exponents. Those declarations report only `propext`, `Classical.choice`, and `Quot.sound`. They do
not provide the missing premise or an unconditional proof of Fermat's Last Theorem. The frozen graph
therefore retains `M0387-WTW` as its minimal open root cut and the root remains `M2`.

The source classification remains `H1`, and the readable classification remains `R4`; neither has
an independently accepted H0 or R0 review. Release evidence is also absent for a clean immutable
snapshot, cold empty-cache network-denied build, offline replay, SBOM/licenses, protected CI,
independent signed runners, an independently implemented minimal verifier, and a deterministic
content-addressed bundle. The warm canonical `.lake` symlink is nonrelease evidence only.

## Self-test

Commands run from base revision `4dabab14860067cbb1220d76c5a1bd9abd87d624` on 2026-07-12:

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets validated

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0387
  exit 0: rank 1; lifecycle planned; theorem_complete=false

cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0387/Statement.lean
  exit 0: exact target elaborated

cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0387/Proof.lean
  exit 0: five admitted partial or conditional declarations elaborated

python3 Stage1_Instances/THM-M-0387/check_validation.py
  exit 0: pinned evidence reconciled; exact root remains M2/open

python3 Stage1_Instances/THM-M-0387/check_release.py
  exit 0: blocked decision, unaccepted dependency, open M2 root, unchanged vector, and release cut set agree

python3 -m json.tool Stage1_Instances/THM-M-0387/release-decision.json
  exit 0: valid JSON

git diff --check -- Stage1_Instances/THM-M-0387
  exit 0: no whitespace errors
```

No dependency update, build, fetch, clone, or `.lake` mutation was performed. This self-tests the
negative release reconciliation only. Retry requires exact closure of `M0387-WTW` and root
composition, accepted H0/R0 and trust evidence, master acceptance of the dependency chain, and a
separately provisioned hermetic and independent release run.
