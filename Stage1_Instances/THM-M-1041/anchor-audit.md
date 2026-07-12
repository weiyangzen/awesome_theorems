# Anchor audit: THM-M-1041

Item: `S56-M-1041-ANCHOR_AUDIT`  
Audit cutoff: 2026-07-12 10:00 +08:00  
Base revision: `3bb9672e70fb05a3e2a6743d8dcfb6b86161e0cb`

## Exact target and search boundary

The audited root is the frozen real contraction variant
`Stage1Instances.THM_M_1041.HilleYosidaContractionTarget`, expression SHA-256
`e6e5f0cbc4d61e4b3ac869fe7b01d4e0d28e3c558c1dea897c29871891f7768d`. It is an `Iff`
between existence of a strongly continuous contraction semigroup with generator `A` and
closedness, density, and a bounded two-sided resolvent for every positive real parameter.

Search order was repository-local Lean, pinned mathlib, then public Lean 4 repositories. Queries
included `Hille-Yosida`, `HilleYosida`, `Yosida`, `strongly continuous semigroup`, `C0 semigroup`,
`infinitesimal generator`, and `semigroup generator Lean4`. Anonymous GitHub code search became
rate-limited, so the public negative result is bounded rather than exhaustive. The discovered
project was inspected at a commit-qualified URL and through git metadata; it was not cloned,
fetched into `.lake`, or built.

## Candidate decisions

| Candidate | Immutable revision | Exact role | Decision |
|---|---|---|---|
| repository legacy `S1_M_234.lean` | `3bb9672e...e0cb` | abstract statement shape and projection wrappers | `M3`; reject as proof anchor because substantive facts are unconstrained `Prop` fields |
| pinned mathlib | `8a178386...a95` | `LinearPMap` closed graph/domain and continuous-linear-map substrate | no terminal match; exact root remains `M4`, so no `M0-W` |
| `mrdouglasny/hille-yosida` | `680e9499...d667` | forward resolvent construction, right inverse, and norm bound | `E3/M3` partial anchor only; no root integration credit |

The external project uses Lean 4.29.0 and the same mathlib commit as this repository. At the
audited revision, `StronglyContinuousSemigroup.lean` exposes
`ContractingSemigroup.resolventMapsToDomain`, `ContractingSemigroup.resolventRightInv`, and
`hilleYosidaResolventBound`. Those results start from a bundled semigroup and cover useful pieces
of the forward direction. They do not prove generator density or closedness, the left inverse on
the whole operator domain, or the converse construction. `Future/GenerationTheorem.lean` keeps
only dissipativity scaffolding: the former generation and density axioms are commented out, and
there is no converse theorem body. Consequently the candidate does not match the frozen `Iff`.

The external README and axiom audit report standard Lean axioms for headline forward results, but
this worker did not import or build that repository, run `#print axioms`, or inspect a transitive
terminal dependency closure locally. Under the evidence hierarchy, a commit-qualified source
anchor without an independent build is `E3`, not `E2`; partial statement scope also prevents `M1`.

## Validation

All commands ran in this worker clone. Lean used the existing pinned `.lake` artifacts; no Lake
update, dependency fetch, clone, or build occurred.

| Command | Exit | Result |
|---|---:|---|
| `rg -n -i 'Hille.?Yosida|HilleYosida|Yosida|strongly continuous semigroup|C.?0 semigroup|infinitesimal generator' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no matching terminal API or theorem in pinned mathlib source |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git ls-remote https://github.com/mrdouglasny/hille-yosida.git refs/heads/main` | 0 | immutable candidate revision observed as `680e9499ee866763e737c8d888c1248684ced667` |
| `lake env lean ../../Stage1_Instances/THM-M-1041/AnchorAudit.lean` | 0 | pinned substrate declarations and the closed/dense `LinearPMap` expression elaborate |
| `python3 ../../Stage1_Instances/THM-M-1041/check_anchor_audit.py` | 0 | schema, immutable revisions, candidate classifications, exact target fingerprint, and fail-closed root decision pass |
| `python3 ../../Stage1_Instances/THM-M-1041/check_statement.py` | 0 | frozen expression fingerprint unchanged; all three statement mutations distinguished |

## Verdict

The phase audit is self-tested and may be offered to the master as `[_]`, but the theorem is not
proved. Root machine status remains `M4`: no usable exact formal artifact was located. The external
partial anchor should be revisited only at child-obligation granularity with a pinned local build,
exact adapters, machine-derived axioms, and terminal-body provenance. The next phase must expose
generator closedness/density, the missing forward inverse, and the Yosida-approximation converse as
separate obligations.

