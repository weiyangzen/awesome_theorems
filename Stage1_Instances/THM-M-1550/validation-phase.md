# THM-M-1550 validation-phase result

Item: `S56-M-1550-VALIDATION`  
Base revision: `fa403ca1dcee36895541a38891b372faf4113aab`

The frozen statement, conditional composition certificate, proof-phase module,
and a separately written reconstruction all elaborate with the pinned toolchain.
`Validation.lean` does not import `Proof.lean` or `ObligationTree.lean`; it repeats
the proposition and directly applies the pinned spectrum theorem. This is useful
same-worker corroboration, but not rev-5.6 independent verification.

## Exact validation

Commands ran from the repository root on 2026-07-12. The validator used
`lake env lean` narrowly, directed local `.olean` output to a fresh temporary
directory, and removed it. It did not update, build, clone, fetch, or modify
`.lake`.

```text
python3 Stage1_Instances/THM-M-1550/check_validation.py
  exit 0
  PASS narrow kernel replay: statement, composition, proof, and separate reconstruction elaborated
  PASS trust observation: checked declarations report only the allowed classical kernel axioms
  PASS local provenance: frozen hashes, clean pinned mathlib, toolchain, and manifest agree
  STALE authoritative graph: root remains M3 with zero accepted closure pending master reconciliation
  BLOCKED release gates: shared warm .lake, incomplete TCB/SBOM archive, and no distinct runner

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-1550
  exit 0: rank 209, planned, theorem_complete false
python3 Stage1_Instances/THM-M-1550/check_statement.py
  exit 0: canonical expression hash matched and all four mutations differed
python3 Stage1_Instances/THM-M-1550/check_obligation_tree.py
  exit 0: 10 obligations and 19 reciprocal typed edges passed; frozen root remains M3
python3 Stage1_Instances/THM-M-1550/check_proof.py
  exit 0: exact frozen root and spectrum leaf source checks passed
```

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | provisional pass | Exact statement, conditional composition, proof, and separate reconstruction elaborate. |
| Placeholder/unsafe scan | pass | Four Lean modules contain no `sorry`, `admit`, `sorryAx`, local `axiom`, or `unsafe` declaration. |
| Trust observation | provisional pass | Checked proof declarations report `propext`, `Classical.choice`, and `Quot.sound`; full release TCB closure is absent. |
| Local provenance | pass | Frozen source hashes, clean mathlib revision `8a178386`, toolchain pin, manifest pin, and terminal source hash agree. |
| Root kernel closure | provisional pass | Both `laxPairIsospectrality` implementations prove the frozen conditional proposition via `spectrum.units_conjugate`. |
| Structured state freshness | fail closed | The frozen graph predates proof closure and reports `root_machine_debt=M3` with zero accepted obligations. |
| Hermetic release replay | fail closed | Shared warm `.lake`; no cold empty-cache replay, offline restore, complete TCB inventory, SBOM/license archive, or deterministic bundle. |
| Independent verification | fail closed | Separate implementation, but no distinct identity, independently provisioned runner, second signature, or independent minimal verifier. |

This is genuinely self-tested validation-phase work, but grants no `E0/E1`,
accepted `M0-*`, `AUDIT-Z`, `THEOREM-Z`, release, or theorem-completion credit.
`audit_complete=false` and `theorem_complete=false`.
