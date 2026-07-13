# THM-M-0405 release decision

Item `S56-M-0405-RELEASE` has the exact verdict **blocked**. The lifecycle remains `planned`, the
root vector remains `[H1, M4, R3]`, no receipt is accepted, and both `AUDIT-Z` and `THEOREM-Z` are
false. This is a self-tested negative release reconciliation. It is not theorem completion,
release-grade evidence, or master acceptance.

## Evidence reconciliation

The first workflow failure is `S56-10.2-DEPENDENCY-ACCEPTANCE`. The validation prerequisite is only
a `[_]` worker projection. Its receipt is provisional, `accepted=false`, `release_grade=false`, and
has no dependency-ordered master acceptance.

The mathematical root independently remains open at `M0405-X-BHV-BRIDGE`. `Proof.lean` contains
18 genuine algebraic normalization lemmas, and `Validation.lean` separately reconstructs four
small Lucas consequences. Neither file proves a universal primitive-divisor branch. The checked
`statement_of_branches` declaration consumes the Lucas and Lehmer branches as premises; it does
not establish either premise. The frozen registry and both receipts therefore agree on zero closed
obligations, an `M4` root, and `theorem_complete=false`.

The high-level Bilu-Hanrot-Voutier `n > 30` citation is plausible but does not clear `H0`. The
dossier lacks a primary theorem/page/definition/assumption/errata crosswalk and independent source
review for the exact Lean pair predicates. It also has two unresolved inconsistencies:
`obligation-tree.md` reports 12 human-source-required nodes while the registry reports 11, and
twelve typed-graph nodes name a nonexistent `obligation-graphs.json` owned source. No independent
`R0` reconstruction or complete source-boundary reconciliation exists, so `AUDIT-Z` is false.

Release assurance also fails closed. The current narrow replay uses the scheduler-provided shared
warm pinned `.lake` artifacts. It is not immutable clean input, an empty-cache cold build, offline
archive restoration, or complete SBOM/license/TCB closure. There are no two independent signed
runner attestations, independently implemented minimal verifier, protected adversarial CI record,
build-twice deterministic bundle, or master receipt.

## Validation

The validation-phase checker is historical evidence bound to base revision `09a2e94f...` and the
pre-integration validation DAG row. At current HEAD it correctly rejects reuse as stale. The release
checker instead hash-binds that receipt and the current dossier, then performs a fresh narrow replay
of `Statement.lean`, `ObligationTree.lean`, `Proof.lean`, and `Validation.lean` through the existing
`lake env lean --trust=0` toolchain in a temporary directory under bubblewrap with networking
unshared. It checks source hygiene, the pinned mathlib revision/tree/license, all 25 extant proof or
composition declarations, and the four differential `assert_no_sorry` reports while preserving the
open-root boundary.

```text
python3 -I -B Stage1_Instances/THM-M-0405/check_release.py
  exit 0
  PASS release inputs: target, DAG dependency, receipts, registry, graphs, and hashes agree
  PASS current Lean replay: 25 theorem declarations, including 4 differential checks, are trust-zero and sorry-free
  PASS fail-closed state: lifecycle planned; root H1/M4/R3; accepted receipts 0; closed obligations 0
  BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and unaccepted
  BLOCKED M0405-X-BHV-BRIDGE and S56-10.6-HERMETIC-COLD-EMPTY-CACHE
  verdict=blocked audit_complete=false theorem_complete=false
```

No dependency update, build, clone, fetch, or `.lake` mutation is part of this check. Retry requires
the exact bridge and both primitive-divisor branches, reconciled source and graph records, accepted
H0/R0/provenance/trust evidence, and every independent release gate recorded in
`release-decision.json`.
