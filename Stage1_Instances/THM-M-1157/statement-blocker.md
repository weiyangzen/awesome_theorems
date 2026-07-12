# THM-M-1157 exact-statement gate: blocked

Item: `S56-M-1157-STATEMENT`  
Base revision: `b24e74e26136fe318a124a7754cc67fdb2a2f24c`

## Decision

No exact Lean 4 target can be truthfully selected or elaborated from the repository record. The
entire theorem-specific mathematical wording is the title `Newton位势` (Newton potential) and the
gloss `引力位势` (gravitational potential). The record supplies no truth-valued claim, primary-source
edition or proposition/page locator, exact transcription, assumptions, or errata disposition. The
accepted intake therefore correctly leaves the canonical statement null and the machine state at
`M4`.

A Newtonian potential is an object or construction, not a unique theorem. At least the following
materially different propositions remain compatible with the metadata:

- the point-mass inverse-distance potential formula away from its singularity;
- an integral potential of a density or measure, whose statement depends on dimension,
  integrability, support, and kernel normalization;
- classical or distributional satisfaction of Poisson's equation, with convention-dependent sign
  and constant and different regularity hypotheses;
- harmonicity away from the source/support, decay, regularity, or uniqueness;
- Newton's shell theorem for a spherically symmetric source.

Selecting any one would invent a conclusion and its hypotheses. Even the sign of the potential and
the Poisson equation, the dimension, the gravitational constant, the source model, the treatment of
the singular set, and classical versus weak/distributional equality are unfrozen. The date 1687 and
attribution to Isaac Newton do not identify a modern potential-theory proposition and cannot replace
a pinpoint source crosswalk.

Consequently there is no honest canonical declaration/expression, minimal import set, serialized
expression fingerprint, checked alternate transport, or removed-hypothesis/domain/binder/boundary
mutation to validate. A definition, an assumed `Prop`, or a convenient theorem about inverse
distance would be a broadened or substituted target. No Lean source, proof placeholder, unproved
primitive, or proxy statement was introduced.

First failed gate: exact source-statement identification. Statement acceptance, audit completion,
and theorem completion remain false. The assigned phase is blocked rather than genuinely
self-tested, so no `.stage1-worker-selftest.json` is emitted.

## Pinned environment and checks

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai). The canonical `.lake` directory was
used read-only; no update, build, clone, or fetch command was run.

- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1157` | 0 | Rank 360, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| repository search for the Chinese and English target wording | 0 | Found only inventory metadata, the intake dossier, and neighboring scope notes; no source-frozen proposition or target-specific Lean module |
| pinned-mathlib source search for Newtonian/gravitational potential wording | 1 | No matching declaration source (`rg` exit 1 means no match) |

There is no applicable `lake env lean <target>.lean` command: the missing exact proposition is the
blocker, and compiling a nearby statement would not validate this node.

## Retry condition

An accountable source review must supply an immutable primary edition and exact proposition/page,
an exact claim transcription, translation and errata notes, and a convention ledger freezing the
dimension, source domain, kernel and constants, sign, ordered quantifiers, hypotheses, conclusion,
singular/degenerate cases, and the intended notion of equality or differentiability. It must also
distinguish the selected result from the shell theorem, Poisson equation, and harmonicity/regularity
claims. A later statement run can then encode that proposition, minimize pinned imports,
fingerprint elaboration, compile checked transports, and execute the required mutation classes.
