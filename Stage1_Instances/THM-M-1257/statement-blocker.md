# Statement gate blocker

Item: `S56-M-1257-STATEMENT`  
Theorem: `THM-M-1257`  
Verdict: blocked; no exact canonical Lean target is claimed.

## First failed gate

The repository source record gives only "Lewy counterexample," Hans Lewy, 1957, and "some linear
PDEs have no solution." The intake identifies Lewy's paper, *An example of a smooth linear partial
differential equation without solution*, Annals of Mathematics (2) 66 (1957), 155-158, but it does
not contain an accepted immutable copy or a verified transcription of the displayed operator,
forcing term, neighborhood quantifiers, derivative convention, or solution regularity. The
repo-local research record and Stage0 projection add none of those statement-critical data.

Those omissions distinguish inequivalent propositions. In particular, a statement about no
classical solution on one domain, no distributional solution near a point, or only the existential
headline that some PDE is nonsolvable cannot be substituted for Lewy's explicit construction.
Coefficient signs and complex-conjugation conventions also cannot be selected from memory without
a checked coordinate or conjugation transport.

Consequently the ordered binders, exact hypotheses and conclusion, normalized Lean expression,
expression hash, minimal import set, checked alternate transports, and the four required mutations
cannot be truthfully supplied. Under rev-5.6 section 5.1 this is a hard statement blocker. The
machine state remains `M4`. No opaque proxy predicate, caller-supplied nonsolvability assumption,
unproved declaration, or broadened existential wrapper was introduced.

## Pinned-environment inspection

The available pinned environment can be inspected, but it does not repair the missing mathematical
statement. A bounded name/text search found no Lewy or local-PDE-solvability declaration in pinned
mathlib or the repository's historical Lean modules. The sole `nonsolvability` match in mathlib is
for the unrelated Fermat-Catalan equation and supplies no candidate for this target. This is only a
statement-phase feasibility observation, not the later exhaustive anchor audit.

- Repository base revision: `c00bc6793b3d4c186b81b80bbaf165b32e125b58`.
- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Validation evidence

Commands ran in this worker clone. The Lean inspection used only the existing canonical pinned
`.lake` artifacts; no update, build, clone, or fetch command was used.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1257` | 0 | rank 435, lifecycle `planned`, legacy artifacts unaccepted, theorem incomplete |
| `rg -n -i 'Lewy\|local.?solvab\|nonsolvab\|partial differential equation without solution' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | only unrelated Fermat-Catalan `nonsolvability` documentation matched; no Lewy/PDE target declaration |
| `rg -n -i 'Lewy\|local.?solvab\|nonsolvab\|partial differential equation without solution' Formalizations/Lean/AwesomeTheorems --glob '*.lean'` | 0 | only an unrelated string describing the same Fermat-Catalan theorem matched; no historical Lewy module |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | checked mathlib revision recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | hashes match the environment fingerprint above |
| `git diff --check -- Stage1_Instances/THM-M-1257` | 0 | no whitespace errors after adding this record |

The pre-existing untracked `Formalizations/Lean/.lake` link is shared pinned infrastructure and was
read but not modified.

## Retry condition

Provide an immutable primary-source artifact and independently verified page-level transcription
that fixes the explicit operator, forcing term, locality quantifiers, solution space, equality
sense, and applicable errata. The statement phase can then map every source component to ordered
Lean binders, identify genuinely minimal imports, elaborate and serialize the exact proposition,
check any coordinate/conjugation variants by kernel-checked transports, and mutation-test removed
regularity, changed domain, binder scope, and boundary cases.

Until then, statement acceptance and theorem completion are false. Because the assigned phase is
not genuinely self-tested to its completion gate, no `.stage1-worker-selftest.json` is emitted.
