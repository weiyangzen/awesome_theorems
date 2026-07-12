# THM-M-0030 statement validation

Item: `S56-M-0030-STATEMENT`; base revision:
`94f6abf9359f26384e0f68bef694dc5b9aae624c`; base tree:
`e0083f4f402c93febe4419b51498afa8ecf81c06`.

## Frozen target

`Stage1Instances.THM_M_0030.KrullIntersectionTarget` quantifies over an implicit
`R : Type u`, its `CommRing R`, `IsNoetherianRing R`, and `IsLocalRing R` instances, and an
arbitrary `I : Ideal R`. Given the propositional properness premise `I ≠ ⊤`, it concludes that
the infimum of `I ^ n` over every `n : Nat` equals the bottom ideal. No domain, reducedness,
completeness, dimension, characteristic, principal-ideal, or maximal-ideal restriction is added.

The checked `krullIntersectionTarget_iff_membershipTarget` transport expands ideal equality to the
elementwise statement that an element in every natural power is zero. Separate kernel witnesses
show that top is the excluded counter-boundary and bottom is included. The three direct imports are
minimal statement-supporting modules. In particular, this artifact does not import the proof-
bearing `Mathlib.RingTheory.Filtration` module or invoke its Krull intersection declarations.

## Commands and results

All commands ran at the repository root unless the table gives a different working directory. The
automation-provided canonical `.lake` symlink was reused read-only; no update, build, clone, fetch,
or dependency mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard projection and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0030` | 0 | rank 1075; planned; intake provisional; theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0030/Statement.lean` | 0 | exact target, checked membership iff, four expected type rejections, top/bottom boundaries, axiom reports, and explicit expression elaborated |
| `cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0030/check_statement.py` | 0 | expression SHA-256 `53389852...861e`, source SHA-256 `737a2cf8...978e`, output SHA-256 `26a2d4c8...ef3a`; all mutations distinguished; imports, pins, metadata, receipt, and worker packet agree |
| deletion probe without `Mathlib.RingTheory.Ideal.Operations` | 1 expected | ideal natural-power interface is unavailable |
| deletion probe without `Mathlib.RingTheory.LocalRing.Defs` | 1 expected | `IsLocalRing` is unavailable |
| deletion probe without `Mathlib.RingTheory.Noetherian.Defs` | 1 expected | `IsNoetherianRing` is unavailable |
| `python3 -m json.tool` over all owned JSON and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON |
| prohibited Lean construct scan over owned `.lean` sources | 1 expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration occurs in source |
| `git diff --check -- Stage1_Instances/THM-M-0030 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

## Boundary and status

The validator serializes each mutation under the same explicit/universe options and rejects any
mutation whose expression fingerprint equals the root. Lean also rejects each mutation as a term
of the root using `#check_failure`: removal of properness, specialization to fields, moving the
arbitrary ideal into an existential, and adding `I ≠ ⊥` to exclude the bottom-ideal boundary.
These are statement-identity tests, not claims that every mutation is mathematically false.

This is statement-only evidence pending master acceptance. Historical primary-source fidelity and
independent review remain open at H1. The packet does not inspect or credit the pinned mathlib proof
body, establish an anchor audit, or advance obligation-tree, proof, validation, release, audit-
completion, or theorem-completion state.
