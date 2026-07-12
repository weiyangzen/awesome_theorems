# THM-M-1041 proof-phase blocker

Item: `S56-M-1041-PROOF`  
Attempt date: 2026-07-12  
Base revision: `76c08cb569093ff0ea02564e80dced5284ebd59d`

## Result

The proof phase is blocked and is not self-tested as complete. No worker
self-test manifest is emitted. The exact frozen root remains `H2/M4/R4`, and
neither `ForwardPackage` nor `ConversePackage` has been inhabited.

The smallest root cut is still:

```text
M1041-F-ASSEMBLE
M1041-C-ASSEMBLE
```

The forward package requires new formal analysis for generator closedness and
density, construction of the Laplace/Bochner resolvent, both inverse laws, and
the contraction estimate. The converse package requires the Yosida
approximants, their exponential semigroups, convergence, strong continuity,
contraction, and identification of the generator graph. These results are not
present in the pinned mathlib source.

The only audited external Lean candidate is
`mrdouglasny/hille-yosida` at
`680e9499ee866763e737c8d888c1248684ced667`. Its inspected scope is partial:
it supplies prospective forward resolvent children but not generator density,
closedness, the complete two-sided resolvent package, or the converse
generation theorem. It is not in the pinned Lake dependency closure and was
therefore neither fetched nor credited. The worker rules prohibit mutating
`.lake` to acquire it. Consequently there is no exact theorem body that can be
truthfully pinned or imported in this phase.

`ObligationTree.lean` contains only a checked implication from the two open
direction packages to the root. It is not a proof of either package and is not
counted as root closure. Adding constants for those packages, weakening the
equivalence, or replacing the analytic definitions with abstract fields would
be an axiom or substituted theorem and was rejected.

## Commands and exact results

All commands ran in the worker clone. Existing pinned artifacts were reused;
no Lake update, build, clone, or fetch ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets pass |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1041` | 0 | rank 234, `planned`, `theorem_complete: false` |
| `python3 Stage1_Instances/THM-M-1041/check_statement.py` | 0 | exact expression SHA-256 `e6e5f0cbc4d61e4b3ac869fe7b01d4e0d28e3c558c1dea897c29871891f7768d`; three mutations killed |
| `python3 Stage1_Instances/THM-M-1041/check_obligation_tree.py` | 0 | 21 obligations and 56 typed edges pass; root open at M4; both packages remain M4 |
| `rg -n -i 'Hille.?Yosida\|HilleYosida\|Yosida\|strongly continuous semigroup\|C.?0 semigroup\|infinitesimal generator' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no matching Hille-Yosida terminal theorem in pinned mathlib source |

The recorded narrow Lean recipe is:

```text
cd Stage1_Instances/THM-M-1041
LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
  $(cd ../../Formalizations/Lean && lake env which lean) \
    -o Statement.olean Statement.lean
LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
  $(cd ../../Formalizations/Lean && lake env which lean) ObligationTree.lean
rm -f Statement.olean
```

It elaborates the frozen statement and the conditional composition, but it
cannot supply kernel evidence for either open direction package.

## First failed gate

`M1041-F-CLOSED` is the first unresolved forward leaf and
`M1041-C-YOSIDA-APPROX` is the first unresolved converse leaf. There is no
repo-local or pinned exact proof body for either. Proof-phase completion and a
`[_]` worker receipt would therefore be false.
