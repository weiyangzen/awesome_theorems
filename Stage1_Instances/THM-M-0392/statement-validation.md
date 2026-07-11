# THM-M-0392 Statement Validation

## Frozen target

`Statement.lean` freezes the Mordell finiteness target: for every nonzero `k : Int`, the integer
pairs satisfying `y ^ 2 = x ^ 3 + k` form a finite type. Finiteness is dependency-minimally encoded
as an injection into `Fin n` for some `n`; the solutions are a subtype of `Int × Int`. This is the
same mathematical notion of finite solution set without importing a mathlib proof surface.

The repository source says only `y²=x³+k的整数解`. It fixes the equation and integer
coordinates but does not say whether `k` is fixed or quantified, or whether the requested result is
finiteness or effective enumeration. This node freezes the legacy-guided Mordell finiteness
interpretation for execution. It excludes `k = 0`, where `(x,y) = (t^2,t^3)` supplies an infinite
family. Primary-source fidelity and H0 remain open for the later audit.

The sole direct import is Lean's `Init`. The checked theorem
`mordellFinitenessStatement_iff_inlineEquationStatement` transports between the named-predicate and
inline-equation encodings without proving finiteness. Four separately elaborated mutations cover a
removed hypothesis, changed coordinate domain, changed binder scope, and the excluded boundary.

## Environment

- Base revision: `6646f3026454e24525976ebd54841f85a50d3ba5`
- Lean toolchain: `leanprover/lean4:v4.29.0`
- mathlib revision pinned by the environment: `8a178386ffc0f5fef0b77738bb5449d50efeea95`
- `lake-manifest.json` SHA-256: `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`
- Elaborated expression SHA-256: `4b5dfc8bf3fbd262e5553eb6e4641dc2517dd73b49cb45d90aaa1ea0ff4c7dfb`

## Commands and results

Run on 2026-07-12 from the worker clone unless an explicit directory is shown:

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0392
  exit 0: rank 2; planned; L0; rework_required=true; theorem_complete=false
cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0392/Statement.lean
  exit 0: canonical Prop printed with pp.explicit; no Lean diagnostics
python3 Stage1_Instances/THM-M-0392/check_statement.py
  exit 0: expression SHA-256 4b5dfc8bf3fbd262e5553eb6e4641dc2517dd73b49cb45d90aaa1ea0ff4c7dfb;
  4/4 mutation fixtures killed
python3 -m json.tool Stage1_Instances/THM-M-0392/statement.json
  exit 0: valid JSON
git diff --check -- Stage1_Instances/THM-M-0392
  exit 0: no whitespace errors
```

The clone reused the already materialized pinned `.lake` artifacts and did not update or fetch
dependencies. This establishes statement elaboration only. Master acceptance remains pending, and
the theorem remains incomplete.
