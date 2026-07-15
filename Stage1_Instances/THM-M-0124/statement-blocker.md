# Exact-statement gate: blocked

Item: `S56-M-0124-STATEMENT`

Theorem: `THM-M-0124`

Base revision: `90a1d52c43113012c8aa0e2b110da02e58ce1724`

Verdict: `blocked`; the statement node remains `[ ]`.

## First failed gate

The exact source statement and its concrete formal object model are not both frozen. The intake
correctly identifies the Manin-Drinfeld theorem family: a degree-zero divisor supported on the
cusps of a congruence modular curve has torsion class in its Jacobian, with cusp differences as a
candidate equivalent generator form. It also records that the original theorem/page, exact
generality, arithmetic base, geometric-versus-rational conventions, translation variance, errata,
and independent source review remain open. Selecting those details here would invent mathematics
rather than elaborate an already fixed claim.

The pinned Lean environment has the beginning of the required domain, but not the target geometry.
It exposes congruence subgroups, cusps, cusp orbits, and finiteness of those orbits. A bounded
pinned-mathlib search found no Manin-Drinfeld declaration, compactified modular curve attached to a
congruence subgroup, curve Jacobian or `Pic^0`, cuspidal divisor-class construction, or Abel-Jacobi
map. Mathlib's files named `EllipticCurve.Jacobian` encode Jacobian coordinates for a Weierstrass
curve; they are not the Jacobian variety of an arbitrary compactified modular curve.

The legacy `S1_M_043.lean` cannot fill this gap. Its caller supplies an abstract
`CompactifiedModularCurve`, an abstract additive target, and an arbitrary divisor-class map. The
intake expressly excludes a result over such user-supplied interfaces because it assumes away the
modular curve, Jacobian, and Abel-Jacobi construction. It also excludes the generated metadata
gloss about unspecified Heegner-point properties, cusp-orbit finiteness as a substitute for
torsion, and an `X_0(N)`-only or `X_1(N)`-only specialization presented as the general theorem.

Consequently there is no truthful canonical Lean expression, minimal canonical import set,
expression fingerprint, or checked pairwise/all-divisor and Jacobian/`Pic^0` transport. The required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary mutations are not meaningful
until that target exists. Machine state remains `M4`; no proof evidence was inspected or credited.

## Pinned Lean boundary

`StatementProbe.lean` has one direct import,
`Mathlib.NumberTheory.ModularForms.Cusps`. It checks the concrete congruence-subgroup and cusp-orbit
surface and elaborates that a congruence subgroup has finitely many cusp orbits. This distinguishes
a missing canonical object model from a missing Lean installation, but it is not a weakened
Manin-Drinfeld target and receives no statement or proof credit. The import is minimal for the
probe only; no minimal-import claim is made for the absent canonical target.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The existing canonical `.lake` artifacts were used
read-only. No update, build, dependency clone, or fetch was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-15 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0124` | 0 | Rank 43, planned, legacy slot unaccepted, theorem incomplete |
| `git status --short` (pre-edit) | 0 | Only the automation-provided untracked `Formalizations/Lean/.lake` symlink was present |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean, commit, platform, and Lake versions above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | Pinned mathlib revision and tree above; its status was clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0124/StatementProbe.lean` | 0 | Four concrete APIs and congruence-subgroup cusp-orbit finiteness elaborated; stdout SHA-256 `2d31e6...93547` |
| `rg -n -i 'manin.?drinfeld\|manindrinfeld\|cuspidal[ -]divisor\|cusp[ -]divisor\|abel.?jacobi\|compactified modular curve\|modular curve.*(jacobian\|picard)\|degree.zero picard' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | Expected no-match exit; zero output with SHA-256 `e3b0c4...b855`; no exact or concrete target construction found |
| `python3 -m json.tool Stage1_Instances/THM-M-0124/statement-blocker.json` plus scoped `jq -e` blocker invariants | 0 | Valid JSON; item identity, null target/fingerprints, unchanged `[H1,M4,R4]`, failed statement gate, and false completion flags agree |
| scoped `rg` for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` in owned Lean files | 1 | Expected no-match exit; no prohibited Lean declaration found |
| `git diff --no-index --check /dev/null <each-new-owned-file>` | 1 per file | Expected new-file difference exits with empty diagnostics; all three new files have no whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | No completion manifest exists because the statement gate is blocked |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` and exact pin comparison | 0 | Empty package status; mathlib remains at the recorded pinned revision |

The machine-readable blocker records the full hashes and exact claim boundary. These final checks
were rerun after the artifacts were written.

## Retry condition

Preserve and independently review an immutable primary-source theorem/page that fixes the exact
generality, assumptions, base and cusp/divisor conventions. Then provide or pin concrete Lean
constructions of the associated compactified modular curve, its Jacobian or degree-zero Picard
group, and the cuspidal divisor-class map. A later statement worker can encode only that reviewed
claim, minimize imports, serialize the elaborated expression and environment, compile all credited
transports, and execute the four mutation classes.

This is the first failed gate, not completion of the statement node or any downstream node. The
intake dependency is itself only provisional `[_]`, so master acceptance would remain dependency
ordered even if a target were available. This assigned phase is not genuinely self-tested; no
`.stage1-worker-selftest.json` is emitted. Root debt remains `[H1, M4, R4]`, and both audit and
theorem completion remain false.
