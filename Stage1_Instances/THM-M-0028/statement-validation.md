# THM-M-0028 statement validation

Base revision: `94f6abf9359f26384e0f68bef694dc5b9aae624c`; base tree:
`e0083f4f402c93febe4419b51498afa8ecf81c06`. Validation date: 2026-07-13
(Asia/Shanghai).

The statement phase freezes the modern unital commutative specialization of the source-matched
one-way theorem. Its exact target is
`Stage1Instances.THM_M_0028.IdealAscendingChainTarget`: finite generation of every ideal implies
tail equality for every `Nat →o Ideal R`. The sole direct import is
`Mathlib.RingTheory.Finiteness.Defs`, and deleting it fails. The statement module does not import
the adjacent `Noetherian.Defs` chain theorem or provide an inhabitant of the canonical target.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`.
- Canonical expression SHA-256:
  `89e7e911ed4a5b75c153d824133091ad74ba20a0ecab19bd609b23a54badbee4`.
- Statement source SHA-256:
  `db7cbc8250aa905f1d8a2686ab14e9b31eeeba3409179d22e7169627df02f3a7`.
- Lean output SHA-256:
  `5907fd942bbcc236601dd57eef9e94a77df02cfbd0fc6a1606b38de078d256ce`.

The automation-provided `.lake` symlink to canonical pinned artifacts was used read-only. No Lake
update/build, dependency fetch/clone, or other `.lake` mutation was performed.

## Checks

Checked alternates expose the definitionally equal regular-submodule carrier and the
function-plus-`Monotone` source spelling. They forward the chain and
conclusion unchanged and are not proofs of stabilization. Four structural mutations
remove the premise, change the domain to fields, move the stabilization index outside the chain
binder, and add `Nontrivial`. Each is rejected as the canonical type and has a distinct explicit
expression. A generic subsingleton theorem and concrete `PUnit` probe cover the zero-ring boundary.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets passed |
| `python3 scripts/stage1_target.py show THM-M-0028` | 0 | rank 1073; planned; L0/rework_required; theorem incomplete |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0028/Statement.lean)` | 0 | exact target, carrier/function transports, mutations, boundary, axiom reports, and explicit expression elaborated |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0028/BoundaryProbe.lean)` | 0 | `PUnit` elaborated as a commutative zero ring whose ideals are finitely generated |
| `(cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0028/check_statement.py)` | 0 | expression/source/output hashes, import deletion, mutations, pins, structured artifacts, receipt, and packet agreed |
| prohibited Lean construct scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-0028 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

## Open Boundary

Master acceptance remains pending. The 1921 source's nonunital domain has not been shown equivalent
to the explicitly bounded modern unital specialization; complete translation, terminology,
premise/direction/proof mapping, errata work, and independent source review remain open. The formal
candidate body, provenance, trust, proof/composition closure, obligation graphs, readable proof,
hermetic replay, and independent validation are later phases. Thus H1/M3/R3 is unchanged, and no
H0, M0, root proof, audit completion, or theorem completion is claimed.
