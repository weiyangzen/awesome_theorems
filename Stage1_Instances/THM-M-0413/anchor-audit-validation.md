# Anchor-audit validation record

Base revision: `1ec654c416270f261b365f46f5f2409b65d3f839`.

All Lean commands ran from `Formalizations/Lean` with the existing pinned toolchain and canonical
`.lake` artifacts. No update, build, fetch, clone, or other dependency mutation was run.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`; 1546 unique ranked targets, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0413` | 0 | rank 68; planned; `hard_mathlib_anchor_and_wrapper`; theorem incomplete |
| `lake env lean ../../Stage1_Instances/THM-M-0413/AnchorAudit.lean` | 0 | Both exact wrappers elaborated; printed the instance and terminal body; all four axiom reports were `[propext, Classical.choice, Quot.sound]` |
| `git -C .lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`, equal to the Lake manifest pin |
| `rg -n 'sorry|admit' .lake/packages/mathlib/Mathlib/NumberTheory/NumberField/Basic.lean .lake/packages/mathlib/Mathlib/RingTheory/DedekindDomain/IntegralClosure.lean` | 1 | No placeholder token found in either audited source file |
| `rg -n 'IsDedekindDomain.*(RingOfIntegers|𝓞)|RingOfIntegers.*IsDedekindDomain' .lake/packages/flt-regular --glob '*.lean'` | 1 | No distinct candidate in pinned `flt-regular` commit `56161b6e...` |
| `python3 -m json.tool Stage1_Instances/THM-M-0413/anchor-audit.json` | 0 | Audit receipt parses |
| `git diff --check -- Stage1_Instances/THM-M-0413` | 0 | No whitespace errors in the owned path |

The `#print` output confirms that the named number-field instance delegates directly to
`IsIntegralClosure.isDedekindDomain`. The latter visibly constructs the result from its
Noetherian, dimension-one, and integrally-closed fields. These imported bodies are upstream
mathlib provenance, not repo-local proof bodies. A later obligation/provenance phase must expand
their transitive closure before any stronger machine status or theorem-completion claim.
