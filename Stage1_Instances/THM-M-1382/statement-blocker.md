# THM-M-1382 statement-phase blocker

- Item: `S56-M-1382-STATEMENT`
- Base revision: `1fc66febfddf404bb914cec34962d66862b96f2b`
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt or theorem-completion claim

## First failed gate

The exact-statement gate in section 5.1 of `Docs/Stage1_Blueprint_rev-5.6.md` cannot be
truthfully entered from the frozen intake boundary. The repository catalog gives only a principle
of least action label, William Hamilton, the year 1834, and the gloss "a variational principle for
physical systems." It supplies no cited proposition, formula, ordered binders, hypotheses,
conclusion, boundary cases, proof boundary, or correction history. Stage0 likewise leaves the
formal system, definitions, premises, proof route, alternate forms, axioms, and machine artifact
open. The catalog's verified label is explicitly untrusted under rev-5.6.

This omission is mathematically material. An exact proposition must choose all of the following:

- a physical system and its time, configuration, path, and variation domains;
- a modern integral-Lagrangian action, Hamilton's accumulated living force, a fixed-energy
  abbreviated action, or another source-defined functional;
- regularity, integrability, endpoint, time, energy, and constraint hypotheses;
- global or local minimum, general extremum, or stationarity semantics;
- the implication direction and a conclusion such as equations of motion, Euler-Lagrange,
  vanishing first variation, or existence of an extremal; and
- degenerate intervals, constant paths, singular Lagrangians, empty admissible classes, free
  endpoints, constrained variations, and pointwise versus weak conclusions.

These choices produce inequivalent theorems. Selecting one from memory would invent or substitute
mathematics rather than elaborate the exact received target.

Hamilton's 1834 *On a General Method in Dynamics* was already inspected at intake as an
authoritative source-family discriminator. Its Sections 1-3 distinguish a fixed-energy stationary
action principle from Hamilton's separate law of varying action and use a source-specific
accumulated-living-force convention. This does not select the common modern fixed-time
`integral L(t, q(t), q'(t)) dt` theorem. The catalog cites neither an edition nor a clause, and the
historical-to-modern translation, premises, corrections, proof boundary, and independent review
remain open.

The target identity is also unresolved. `THM-M-1381` owns an adjacent Maupertuis-principle label;
`THM-M-1518` repeats the translated least-action title and broad gloss; `THM-P-0748` gives an
extremal integral-Lagrangian physics formulation; and `THM-P-0749` gives an Euler-Lagrange
necessary-condition gloss. No alias, deduplication, root ownership, statement transport, or
evidence sharing among them is accepted.

In particular, the elaborated `THM-M-1518` target cannot be copied here. It selects a modern
fixed-endpoint implication from stationary action to the interior Euler-Lagrange equation, while
its legacy `S1_M_187` material contains the converse direction. That direction mismatch itself
demonstrates why a shared title cannot establish statement identity.

The authoritative intake task is provisional `[_]`, its worker receipt declares `accepted: false`,
and it has no accepted receipt ID. Rev-5.6 section 10.2 permits this dependency-ordered attempt, but
no accepted statement transition can precede master acceptance. Independently, the intake freezes
`canonical_statement`, the formal target, binders, and hypotheses as absent at `[H5, M4, R4]`, so
exact source-statement identity is the first substantive statement gate failure.

Consequently there is no canonical expression to elaborate, no honest minimal-import set, and no
expression or environment fingerprint. Checked transports and the removed-hypothesis,
changed-domain, changed-binder-scope, and boundary mutation classes are not runnable before the
canonical proposition exists. The root vector remains `[H5, M4, R4]`.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated against the pinned environment. Its three direct
imports expose six adjacent interval fundamental-theorem, integration-by-parts, and local-extremum
derivative APIs. All six checks passed. The probe defines no action, physical dynamics,
admissible-variation class, endpoint or energy constraint, implication direction, target
declaration, or proof body. Its imports therefore cannot be certified minimal for an unidentified
target and receive no statement or proof credit.

A bounded search found no exact-topic least-action, stationary-action, Hamilton-principle,
Euler-Lagrange, or first-variation occurrence in pinned mathlib. The repo-local search found the
foreign `THM-M-1518` statement, legacy `S1_M_187`, and related mechanics artifacts. These results
are discovery evidence only, not the downstream anchor audit or a proof of absence.

The environment was Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided `.lake` symlink and canonical
pinned artifacts were used read-only. No `lake update`, `lake build`, dependency clone or fetch, or
other `.lake` mutation was run.

## Commands and exact results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1382` | 0 | rank 992; `planned`; `L0/rework_required`; no legacy slot; theorem incomplete |
| `git status --short --untracked-files=all` (pre-edit) | 0 | only the automation-provided untracked `Formalizations/Lean/.lake` symlink; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `1fc66febfddf404bb914cec34962d66862b96f2b`; tree `49ae48302378d63f3c54b2a43eeca26433c6b7c5` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | `651c8acc...b1d2` and `321626c8...6d81` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `8a178386...eea95`; tree `bdc39a...5e2b` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1382/IntakeProbe.lean` | 0 | all six adjacent APIs elaborated; stdout SHA-256 `9f2242b5...e6b2`; no target declaration or proof body |
| bounded exact-topic `rg` over pinned mathlib Lean sources | 1 | expected no-match result; no exact-topic occurrence |
| the same bounded `rg` over scoped repo-local Lean sources | 0 | found foreign `THM-M-1518`, legacy `S1_M_187`, and related mechanics artifacts; none credited |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1382-pycache python3 -B Stage1_Instances/THM-M-1382/check_intake.py` | 1 | historical replay first fails because its receipt binds an older authoritative-blueprint digest; it also freezes the original intake-only inventory and is not a statement gate |
| `python3 -m json.tool Stage1_Instances/THM-M-1382/statement-blocker.json` | 0 | blocker is valid JSON |
| scoped Python blocker-invariant check | 0 | identity, base, null target fields, unchanged debt vector, false completion fields, four unrunnable mutations, owned paths, and absent self-test agree |
| prohibited declaration scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped `git diff --check` plus per-new-file no-index checks | 0 | no whitespace diagnostics; no-index exit 1 for each new file is only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest is absent as required for a blocked phase |

## Unblocking condition

An accountable source owner must preserve and hash one lawful complete source edition, select and
independently approve one exact proposition and proof boundary as the `THM-M-1382` root, audit its
corrections and historical-to-modern translation, and resolve the neighboring target identities.
Every incorporated definition, ordered binder, hypothesis, conclusion, and boundary case must then
be frozen. A later statement run can encode that same claim, establish minimal pinned imports,
serialize its elaborated expression and environment, check every credited transport, and run all
four mutation classes.

Until those prerequisites hold, no exact statement, proof, audit completion, or theorem completion
is claimed. Because the assigned phase is not genuinely self-tested to its completion gate, no
`.stage1-worker-selftest.json` is emitted.
