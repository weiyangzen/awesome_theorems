# THM-M-0464 release decision

Item `S56-M-0464-RELEASE` has the exact verdict **blocked**. Lifecycle remains `planned`, the
accepted root vector remains `H1/M4/R3`, and both `AUDIT-Z` and `THEOREM-Z` are blocked.
`theorem_complete` remains false and no receipt is accepted. This is a self-tested negative release
decision, not theorem completion, release-grade evidence, or master acceptance.

## Evidence reconciliation

The provisional validation receipt re-elaborates the exact frozen statement, the conditional root
interface, seven local set-theoretic or degenerate proof bodies, and two separately written boundary
probes. The probes ran in this checkout with the shared warm dependency cache. They do not prove the
general Pila-Wilkie theorem and do not qualify as independent release verification.

The first failed node gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`: the validation prerequisite is a
worker `[_]` receipt with `release_grade=false`, not master-accepted evidence. Even after dependency
acceptance, section 6.7 fails because there is no unconditional declaration of the exact
`PilaWilkieStatement`. The source-equivalence, cell-decomposition, parameterization, determinant,
general algebraic-part, induction, general counting, and representation-transport obligations
remain in the frozen root cut set. The provisional machine root is therefore `M3`.

`AUDIT-Z` is also unavailable: the validation and typed graph explicitly record
`audit_complete=false`, and there are no accepted independent `H0` source or `R0` readability
reviews. Complete root provenance, trust, and TCB closure are impossible while the terminal body is
absent. No immutable clean release input, empty-cache network-denied cold build, offline archive
replay, SBOM/license closure, protected CI/adversarial evidence, two distinct signed runner
attestations, independently implemented minimal verifier, or deterministic release bundle exists.

## Self-test

Commands run from base revision `8a434aa49a78627cb0f9ce260ee33af4d1f2f174`:

```text
python3 Stage1_Instances/THM-M-0464/check_release.py
  exit 0
  release-decision: ok (blocked; validation dependency is unaccepted)
  validation replay: ok (seven partial bodies; exact Pila-Wilkie root remains M3)
  AUDIT-Z=false; THEOREM-Z=false; theorem_complete=false; accepted receipts=[]
```

The release checker binds the reconciled dossier inputs by SHA-256, checks target membership and
accepted `planned` state, compares the validation and frozen-graph cut sets, rejects any terminal
promotion, and reruns the recorded validation recipe with `lake env lean`. No `lake update`,
`lake build`, dependency fetch/clone, network operation, or `.lake` mutation is performed.

Retry requires proof and master acceptance of the eight open root obligations and exact root
composition, accepted `AUDIT-Z` with independent H0/R0 review, and then hermetic, supply-chain,
independent-verifier, CI, deterministic-bundle, and master-acceptance evidence.
