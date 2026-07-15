# THM-M-0419 validation-phase result

Item: `S56-M-0419-VALIDATION`

Base revision: `bd65bfeeea414dd3cfe270a499dca2b9fd65e34c`

## Verdict

The validation phase is self-tested but **blocked**. A narrow, network-isolated trust-zero replay
checks the exact statement, the frozen conditional compositions, the proof phase's
`cyclotomicIdentify` transport, and a separately written same-worker reconstruction that imports
neither `Proof` nor `ObligationTree`. Both transports and pinned
`IsCyclotomicExtension.algEquiv` report exactly `propext`, `Classical.choice`, and `Quot.sound`.
The selected transitive closure reports 33,153 declarations, 1,178 modules, no bodyless nonaxioms,
and no unsafe declarations.

This evidence does not prove Kronecker-Weber. The proof predecessor is only worker-provisional,
and the five-node mathematical cut remains open:

```text
M0419-B-INDUCTION
M0419-L-TAME
M0419-L-WILD-ODD
M0419-L-WILD-TWO
M0419-T-GLOBAL
```

The accepted root therefore remains `[H1, M3, R3]`; `audit_complete=false` and
`theorem_complete=false`. The phase-specific recipe covers zero frozen obligations. It only
corroborates partial progress toward `M0419-C-CYCLOTOMIC-IDENTIFY`, whose frozen interface still
has a planned signature fingerprint and requires independent master mapping review.

## Exact validation

The final recipe runs from the repository root:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0419/check_validation.py \
  --worker-packet .stage1-worker-selftest.json
  exit 0
  PASS THM-M-0419 narrow validation
  PASS kernel replay: exact statement, frozen conditional compositions, partial proof transport, and differential transport elaborated at trust zero
  PASS trust observation: checked declarations report exactly propext, Classical.choice, and Quot.sound; closure reports no bodyless nonaxioms or unsafe declarations
  PASS selected provenance: frozen hashes, clean pinned mathlib revision/tree/origin/license, Cyclotomic.Basic source/blob/olean, and tool identities agree
  FAIL CLOSED dependency/root: proof is worker-provisional and five mathematical packages remain the exact-root cut; accepted root stays H1/M3/R3
  FAIL CLOSED assurance: accepted foundation profile, complete transitive provenance/TCB/SBOM closure, H0, and independent R0 review are absent
  FAIL CLOSED hermetic/independent: shared warm .lake and same-worker reconstruction are neither cold offline replay nor distinct signed verification; audit_complete=false; theorem_complete=false
```

The checker copies all four Lean modules into a fresh temporary directory. Each Lean process runs
inside `bubblewrap --unshare-net` with the host root read-only, only that temporary output directory
writable, fixed locale/timezone/thread settings, and `--trust=0`. It reuses the existing canonical
pinned Lake closure without running `lake update`, `lake build`, clone, fetch, or dependency
mutation. This is stronger isolation for the narrow replay, but the shared warm cache still makes it
nonrelease evidence.

## Gate decisions

| Gate | Decision | Boundary |
|---|---|---|
| Exact kernel replay | pass, nonrelease | Statement, conditional composition, partial transport, and differential transport elaborate at trust zero. |
| Placeholder/unsafe/oracle hygiene | pass | Comment-aware scans and Lean `assert_no_sorry` find no prohibited construct in checked local sources. |
| Axiom observation | provisional pass | Reports are exactly the recorded three axioms; no theorem-specific foundation profile is accepted. |
| Selected provenance | pass, nonrelease | Input hashes, clean mathlib pin/tree/origin/license, `Cyclotomic.Basic` source/blob/olean, and tool identities agree. |
| Proof dependency and exact root | fail closed | Proof is not master-accepted and the five mathematical packages have no bodies. |
| Full trust/provenance | fail closed | Complete transitive serialized provenance, imported-artifact inventory, TCB/bootstrap, SBOM, and policy acceptance are absent. |
| Human source/readability | fail closed | The root remains H1/R3; accepted H0 and independently reviewed R0 evidence are absent. |
| Hermetic release | fail closed | No clean checkout, empty caches, cold build, offline restoration, or deterministic release archive exists. |
| Independent verification | fail closed | Same worker, checkout, Lean binary, and shared cache; no distinct signed runner or independent minimal verifier exists. |

The structured receipt proposes only worker state `[_]` for this validation execution. It grants no
accepted obligation closure, `M0`, `E0/E1`, `AUDIT-Z`, `THEOREM-Z`, release, theorem completion, or
master acceptance.
