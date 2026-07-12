# Anchor audit: THM-M-0330

Item: `S56-M-0330-ANCHOR_AUDIT`  
Audit cutoff: 2026-07-12 12:00 +08:00  
Base revision: `106084d7f6343f3046dfb9e108503edbcdc86191`

## Exact target and search boundary

The audited root is the frozen real contraction variant
`Stage1Instances.THM_M_0330.HilleYosidaContractionTarget`, expression SHA-256
`5696285042abd39e340c7e72b2c2855d17e2e335106b1aa6a724056fd68bd75e`. It is an equivalence
between existence of a strongly continuous contraction semigroup with generator `A` and
closedness, density, and a bounded two-sided resolvent for every positive real parameter.

Search order was repository-local Lean, pinned mathlib, then public Lean 4 repositories. Queries
covered the standard Hille-Yosida aliases, strongly continuous and C0 semigroups, infinitesimal
generators, and semigroup generators. Public negative discovery is bounded rather than exhaustive.
The discovered external project was inspected at a commit-qualified URL and through git metadata;
it was not cloned, fetched into `.lake`, or built.

## Candidate decisions

| Candidate | Immutable revision | Exact role | Decision |
|---|---|---|---|
| repository legacy `S1_M_234.lean` | `106084d7...6191` | abstract statement shape and projection wrappers | `M3`; reject because substantive facts are unconstrained `Prop` fields |
| pinned mathlib | `8a178386...a95` | `LinearPMap` and continuous-linear-map substrate | no terminal match; exact root remains `M4` |
| `mrdouglasny/hille-yosida` | `680e9499...d667` | forward resolvent range/right inverse/norm bound | `E3/M3` partial anchor only; no root integration credit |

The external project uses Lean 4.29.0 and the same mathlib commit. Its
`StronglyContinuousSemigroup.lean` defines `ContractingSemigroup.resolventMapsToDomain`,
`ContractingSemigroup.resolventRightInv`, and `hilleYosidaResolventBound`. These start from a
bundled semigroup and cover only pieces of the forward direction. They do not establish generator
closedness/density, the left inverse over the entire operator domain, or the converse construction.
`Future/GenerationTheorem.lean` retains dissipativity scaffolding, a trivial placeholder example,
and commented former axioms, but no converse theorem. Thus it cannot match the frozen `Iff`.

The external source was not imported or independently checked with `#print axioms`. A
commit-qualified source anchor without a local build is `E3`, not `E2`; its partial scope also
prevents `M1`. Content hashes in `anchor-audit.json` bind the two inspected source files.

## Validation

All commands ran in this worker clone. Lean reused existing pinned `.lake` artifacts; no dependency
update, clone, fetch, or build occurred.

| Command | Exit | Result |
|---|---:|---|
| `rg -n -i 'Hille.?Yosida\|HilleYosida\|Yosida\|strongly continuous semigroup\|C.?0 semigroup\|infinitesimal generator' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no matching terminal API/theorem in pinned mathlib source |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git ls-remote https://github.com/mrdouglasny/hille-yosida.git refs/heads/main` | 0 | `680e9499ee866763e737c8d888c1248684ced667` |
| commit-qualified `curl` plus `rg`/`sha256sum` for the two external files | 0 | declarations/boundaries inspected; hashes `2f7d2149...abe` and `ff3b87ae...308` |
| `lake env lean ../../Stage1_Instances/THM-M-0330/AnchorAudit.lean` | 0 | pinned substrate declarations and closed/dense expression elaborate |
| `python3 ../../Stage1_Instances/THM-M-0330/check_anchor_audit.py` | 0 | schema, revisions, exact fingerprint, classifications, and fail-closed root pass |
| `python3 ../../Stage1_Instances/THM-M-0330/check_statement.py` | 0 | frozen expression unchanged; three mutations distinguished |

## Verdict

The bounded phase audit is self-tested and may be offered to the master as `[_]`; the theorem is
not proved. Root machine status remains `M4`. The obligation-tree phase should separate generator
closedness/density, the missing forward inverse, and the Yosida-approximation converse. Any reuse
of the external partial source requires a pinned local build, exact adapters, axiom inspection, and
terminal-body provenance.
