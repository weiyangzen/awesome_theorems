# THM-M-0388 Anchor Audit Validation

## Result

The frozen target has an exact mathlib candidate at immutable revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`: `Pell.exists_of_not_isSquare` in
`Mathlib.NumberTheory.Pell`. Its conclusion is literally the target's integer equation and
nontriviality condition. Its hypotheses differ only in spelling: mathlib's `not IsSquare D` versus
the frozen `not exists k : Int, k * k = D`. `AnchorAudit.lean` gives the direct iff and an exact
candidate wrapper without adding the legacy generator-classification claim.

The pinned source tree, terminal declaration body, direct module imports, license, aliases, and
special-family exclusions are recorded in `anchor-audit.json`. The legacy local module is a
duplicate wrapper over this same terminal theorem, not independent proof credit. A bounded public
search found no additional candidate through repository metadata; unauthenticated GitHub code
search returned 401 and grep.app returned 429, so the audit makes no exhaustive negative claim.

## Validation and blocker

Commands were run on 2026-07-12 from the worker clone at base revision
`36804d275bde22e8280cb304ab8b40dae4fd5c4e`:

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets passed
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0388
  exit 0: rank 3; planned; L0; rework_required=true; theorem_complete=false
python3 Stage1_Instances/THM-M-0388/check_anchor_audit.py
  exit 0: 3 candidates classified; exact mathlib source anchor and hashes verified; kernel closure blocked
python3 -m json.tool Stage1_Instances/THM-M-0388/anchor-audit.json
  exit 0: valid JSON
cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0388/AnchorAudit.lean
  exit 1: unknown module prefix 'Mathlib'; the pinned cache contains no Mathlib.NumberTheory.Pell.olean
git diff --check -- Stage1_Instances/THM-M-0388
  exit 0: no whitespace errors
```

No dependency update, build, clone, or fetch was run. Under the worker rules the missing pinned
olean is a blocker, not permission to mutate `.lake`. Consequently the exact candidate remains
`E3 / M3`: source and statement mapping are established, but kernel, axiom, transitive provenance,
and trust closure are not. The anchor-audit phase is self-tested pending master acceptance; the
overall audit and theorem are not complete.
