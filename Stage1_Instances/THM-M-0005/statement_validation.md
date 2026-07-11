# Statement validation record

Item: `S56-M-0005-STATEMENT`  
Base revision: `9e3fd02a2a952da7031bb1dd61387443dd4c1cc7`

## Frozen target

- Source: `KunnethStatement.lean`
- Declaration: `AwesomeTheorems.Stage1.THM_M_0005.KunnethFormula`
- Source SHA-256: `f91fb92e25655c923340755a9b64b5b32e4667a51f48474db1f4f14ac0edea53`
- Explicit printed expression SHA-256:
  `f6396a70702a8bb45dbbb267ebd3ba10aae4f4db28cf25355f8fcd7bb607ddd4`
- Lean: `v4.29.0`
- mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`

The target is a proposition asserting a `Nonempty NaturalKunnethSequence R` for every commutative
PID. `NaturalKunnethSequence` contains an actual `ShortComplex.ShortExact` field in every degree,
componentwise homology-induced maps on the tensor and `Tor₁` sums, and both naturality squares.
It is a specification structure only; this phase constructs no inhabitant and claims no proof.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets and ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0005` | 0 | Rank 100, planned hard-mathlib lane, theorem incomplete. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0005/KunnethStatement.lean` | 0 | Exact target elaborated; only four unused-parameter linter warnings on abstract map fields. |
| remove each declared import in isolation and run the same `lake env lean` command | 0 | Every retained direct import is necessary; the redundant TopCat-products import was removed. |
| append `#print AwesomeTheorems.Stage1.THM_M_0005.KunnethFormula`, then `lake env lean -Dpp.universes=true -Dpp.explicit=true <temporary-file>` | 0 | Explicit expression printed; the declaration block alone was extracted and hashed above. |
| append four `rfl` equality mutations and run `lake env lean` separately | 1 each (expected) | Removed PID hypothesis, field-only domain, outer degree binder, and exclusion of degree zero were all rejected as non-identical. |
| `python3 -m json.tool Stage1_Instances/THM-M-0005/intake.json` | 0 | Updated structured dossier parsed. |
| `git diff --check -- Stage1_Instances/THM-M-0005 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

No `lake update`, build, fetch, clone, or `.lake` mutation was performed. The pre-existing untracked
`Formalizations/Lean/.lake` link/artifact was used read-only as instructed.

## Statement-gate tests

The canonical expression fixes the PID domain, all binders, Nat grading, the `p + q = n` tensor
index, the `p + q + 1 = n` Tor index, short exactness, component maps, and two-space naturality.
The boundary `n = 0` is represented without subtraction: `TorDegrees 0` is empty.

No alternate encoding is credited, so no transport wrapper is required at this node. Four
kernel-elaboration mutations attempted to identify the target by `rfl` with a removed PID
hypothesis, a field-only coefficient domain, an incorrectly outer-scoped degree binder, and a
conjunction excluding degree zero. Each failed with a type mismatch as required. Dropping
`shortExact`, either component equation, or either naturality equation visibly changes the
structure type. These checks occurred before any proof evidence; there is no proof evidence here.

## Status boundary

Worker verdict: statement elaboration is self-tested and provisional (`M3`), subject to master
receipt acceptance. The theorem is not complete. The next gate must audit exact mathlib/external
anchors; proof closure, graph composition, source, trust, provenance, hermetic, readability, and
independent-verification gates all remain open.
