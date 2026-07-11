# THM-M-0388 Statement Validation

## Frozen target

`Statement.lean` freezes the Pell-equation target as nontrivial integer-solution existence: for
every positive nonsquare `D : Int`, there are `x y : Int` satisfying
`x ^ 2 - D * y ^ 2 = 1` with `y != 0`. The `y != 0` condition excludes the universal trivial
solutions `(1, 0)` and `(-1, 0)`. Positivity and nonsquareness are the standard parameter boundary
under which this is the Pell existence theorem.

The terse repository source says only `x²-Dy²=1的整数解`. It fixes the equation and integer
coordinate domain but omits quantifiers, the domain and conditions on `D`, and whether "solutions"
means existence or complete classification. This statement node freezes the conservative
nontrivial-existence interpretation. It does not silently inherit the legacy file's stronger
unique-generator classification. Primary-source fidelity and H0 remain open for the later audit.

The sole direct import is Lean's `Init`. It is sufficient for the integer order, ring operations,
powers, and the literal local nonsquare predicate `not exists k : Int, k * k = D`. No mathlib or
Pell theorem module is imported, so elaborating this file cannot accidentally inspect or credit
proof closure. The later anchor audit must check transport to any mathlib `IsSquare` spelling it
credits.

The checked theorem
`pellEquationStatement_iff_conjunctiveHypothesesStatement` transports between curried and
conjunctive hypotheses without proving a Pell solution. Four separately elaborated mutations cover
a removed hypothesis, changed domains, changed binder scope, and the excluded square boundary. The
validator requires each mutation source to differ from the canonical expression fixture.

## Environment

- Base revision: `cdc74d2233a90bfe43066d639abb923202621260`
- Lean toolchain: `leanprover/lean4:v4.29.0`
- mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`
- `lake-manifest.json` SHA-256: `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`
- Elaborated expression SHA-256: `1c7823359ce2079a4c418429cd6be26e48fdfe6acb4624a0ee9701fdc05a92ad`

## Commands and results

Run on 2026-07-12 from the worker clone unless the command contains an explicit `cd`:

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0388
  exit 0: rank 3; planned; L0; rework_required=true; theorem_complete=false
cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0388/Statement.lean
  exit 0: canonical Prop printed with pp.explicit; no Lean diagnostics
python3 Stage1_Instances/THM-M-0388/check_statement.py
  exit 0: expression SHA-256 1c7823359ce2079a4c418429cd6be26e48fdfe6acb4624a0ee9701fdc05a92ad;
  4/4 mutation fixtures killed
python3 -m json.tool Stage1_Instances/THM-M-0388/statement.json
  exit 0: valid JSON
git diff --check -- Stage1_Instances/THM-M-0388
  exit 0: no whitespace errors
```

The worker clone reused the already materialized pinned `.lake` artifacts; it did not update,
fetch, clone, or otherwise mutate dependencies. This evidence establishes statement elaboration
only. Master acceptance remains pending, and the theorem remains incomplete.
