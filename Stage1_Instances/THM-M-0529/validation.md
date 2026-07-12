# Statement validation

Base revision: `8cd5bc5a3f94397a9ec5148db97a8631552f37ec` (tree
`817620977e18dadd98c499fd1e9cc69a5022b0d3`). Validation ran in the worker clone on
2026-07-12 using the pre-existing read-only link `Formalizations/Lean/.lake` to canonical pinned
artifacts. No Lake update, build, fetch, clone, or `.lake` mutation was performed.

## Exact target

`Statement.lean` has only two direct imports: singular-homology definitions and the bundled
abelian-group AB instances needed to instantiate coproducts and homology. Lean printed:

```text
def AwesomeTheorems.THM_M_0529.CanonicalTarget : Prop :=
∀ (n : ℕ) (X Y : TopCat) (e : ↑X ≃ₜ ↑Y),
  IsIso (((singularHomologyFunctor AddCommGrpCat n).obj (AddCommGrpCat.of ℤ)).map (TopCat.isoOfHomeo e).hom)
```

The SHA-256 of this exact stdout (including newlines) is
`346202448f85225bd2460d494524132adb745ad2711c1c4c587a816499c30aea`.

## Commands and results

Commands below use cwd `Formalizations/Lean` unless noted.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0529` | exit 0; rank 586, planned, theorem_complete false |
| `lake env lean --version` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `lake env lean ../../Stage1_Instances/THM-M-0529/Statement.lean` | exit 0; printed the exact target above |
| `lake env lean ../../Stage1_Instances/THM-M-0529/StatementBoundary.lean` | exit 0; degree zero on the empty space elaborates |
| `lake env lean ../../Stage1_Instances/THM-M-0529/MutationRemovedHomeomorphism.lean` | expected exit 1; no `Nonempty` iso instance can be synthesized for arbitrary homology objects |
| `lake env lean ../../Stage1_Instances/THM-M-0529/MutationChangedDomain.lean` | expected exit 1; `n : ℤ` mismatches required `n : ℕ` |
| `lake env lean ../../Stage1_Instances/THM-M-0529/MutationChangedBinderScope.lean` | expected exit 1; `X` and `Y` are unknown before their binders |
| `python3 -m json.tool` on the three target JSON files | exit 0 for all |
| scoped placeholder scan and dossier assertions | exit 0; no forbidden declaration or proof placeholder; frozen hashes/paths agree |
| `git diff --check -- Stage1_Instances/THM-M-0529 .stage1-worker-selftest.json` | exit 0; no output |

The failed mutation files are intentionally invalid negative fixtures and are never imports of the
canonical target. Their expected nonzero status is part of the statement gate, not a known failure.

## Boundary

This receipt proposes only worker-self-tested statement elaboration. The primary-source pinpoint,
formal anchor and terminal proof-body provenance, obligation registry, proof closure, trust and
axiom audit, readable reconstruction, hermetic replay, independent verification, audit completion,
and theorem completion remain open. The historical `已验证` label supplies no credit.
