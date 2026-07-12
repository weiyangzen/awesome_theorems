# THM-M-1013 validation-phase result

Item `S56-M-1013-VALIDATION` was run against the proof-phase snapshot on 2026-07-12. The
node-scoped kernel, exact-target, placeholder, observed-axiom, dependency-pin, and local provenance
checks pass. The validation phase is self-tested, but the evidence is deliberately nonrelease:
the worker reused the canonical warm `.lake` artifacts and cannot supply a second independent
runner or independently implemented verifier.

## Exact recipe and result

The structured recipe in `validation-spec.json` was run from repository root:

```text
$ python3 Stage1_Instances/THM-M-1013/check_validation.py
PASS: exact StatementShape, composition, and Cramer-Wold proof replayed in a fresh temporary module directory
PASS: axiom reports contain only the accepted observed kernel axioms: propext, Classical.choice, Quot.sound
PASS: placeholder scan, frozen hashes, proof receipt linkage, and clean pinned mathlib provenance checks passed
STALE: frozen obligation graph predates proof execution and still reports the root open
BLOCKED: cold empty-cache hermetic replay, full transitive TCB/SBOM closure, and independent-runner verification are unavailable in this worker
exit 0
```

The checker copies `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` into a fresh temporary
directory under `Formalizations/Lean`, elaborates a temporary statement and composition olean, and
then elaborates the proof with that directory prepended to `LEAN_PATH`. The temporary directory is
removed automatically. It does not update, build, clone, fetch, or write into `.lake`.

Additional checks all exited zero:

```text
python3 Docs/tools/check_stage1_standard.py
python3 scripts/stage1_target.py check
python3 scripts/stage1_target.py show THM-M-1013
python3 Stage1_Instances/THM-M-1013/check_statement.py
python3 Stage1_Instances/THM-M-1013/check_obligation_tree.py
python3 Stage1_Instances/THM-M-1013/check_proof.py
git diff --check -- Stage1_Instances/THM-M-1013 .stage1-worker-selftest.json
```

Lean reports version `4.29.0` at commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
The mathlib checkout is clean at `8a178386ffc0f5fef0b77738bb5449d50efeea95`.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | The frozen statement, abstract composition, exact proof root, and all proof helpers elaborate in a fresh temporary module directory. |
| Exact root and composition | pass, provisional | `Proof.cramerWold : StatementShape`; `forward` and `reverse` are both consumed. This is worker evidence, not master acceptance. |
| Placeholder/unsafe scan | pass | No `sorry`, `admit`, `sorryAx`, local `axiom`, or `unsafe` declaration occurs in the checked modules. |
| Observed axiom closure | pass under recorded profile | All printed declarations report only `propext`, `Classical.choice`, and `Quot.sound`. |
| Local provenance | pass with stale-state finding | Frozen source/registry/proof-receipt hashes agree; the two terminal mathlib source modules are tracked at the clean pin. The frozen graph still records its pre-proof open root. |
| Hermetic release replay | fail closed | The run reused shared writable warm `.lake` artifacts; it is not an empty-cache cold build, offline restoration, or complete transitive TCB/SBOM archive. |
| Independent verification | fail closed | There is no independently provisioned runner, distinct attestor, second signature, or independently implemented minimal verifier. |

## Status boundary

This is truthful provisional validation evidence for the assigned node. It supports local kernel
closure of the exact machine root, but grants no `E0/E1`, accepted `M0-*`, `H0`, `R0`, `AUDIT-Z`,
`THEOREM-Z`, release, or master-acceptance credit. `theorem_complete=false`. The integration lane
must reconcile the stale frozen graph and separately provide the missing hermetic and independent
evidence before any stronger claim.

