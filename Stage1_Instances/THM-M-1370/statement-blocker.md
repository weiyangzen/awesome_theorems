# THM-M-1370 statement-phase blocker

- Item: `S56-M-1370-STATEMENT`
- Base revision: `7a489588a59dbd7cca44de7e3b8c3bafcb7448f5`
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt or theorem-completion claim

## First failed gate

The exact-statement gate in section 5.1 of `Docs/Stage1_Blueprint_rev-5.6.md` cannot be
truthfully entered from the recorded intake boundary. The repository record supplies only the name
"Kolmogorov-Arnold theorem," the date 1954, and the gloss "the original form of KAM theory." It
does not identify one immutable source proposition or provide its ordered binders, hypotheses, and
conclusion. Stage0 explicitly leaves the exact definitions and assumptions open.

This omission is mathematically material. Kolmogorov's 1954 announcement and Arnold's 1963 proof
or later formulations cannot be silently merged. Candidate formulations differ in their phase
space and torus dimension, analytic category and norm, nondegeneracy condition, arithmetic
constants, perturbation threshold, invariant embedding or canonical transformation, preservation
or shift of frequency, quantitative estimates, and one-torus versus positive-measure conclusion.
Selecting one of them without an accepted source decision would invent or substitute mathematics.
The similarly named representation theorem is unrelated and remains excluded.

The integrated intake node is provisional `[_]` and has no master-accepted receipt. Even apart
from that dependency boundary, its own source crosswalk identifies exact source-statement identity
as the first failed gate, so statement elaboration cannot proceed truthfully.

Consequently there is no canonical expression to elaborate, no honest minimal-import claim, and no
expression or environment fingerprint. Checked transports and the removed-hypothesis,
changed-domain, changed-binder-scope, and boundary mutation classes are not runnable before the
canonical binders and premises exist. The machine state remains `M4`; this statement phase is not
self-tested complete.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. Its five declared
imports expose adjacent analytic, finite-torus Fourier, ODE, flow, and symplectic-matrix APIs, and
all eight `#check` commands passed. These imports are not claimed minimal for an unidentified
target, and none of the checked declarations states a KAM persistence theorem.

A scoped search of repo-local Lean and pinned mathlib found only unrelated substring matches,
Hamiltonian graph declarations, Kolmogorov probability results, and the legacy Liouville-Arnold
boundary. No Hamiltonian KAM invariant-torus persistence declaration was identified. This bounded
search is feasibility evidence only; it is neither the downstream anchor audit nor proof of
absence.

The environment was Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake
`5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided `.lake` symlink and pinned
artifacts were used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other
`.lake` mutation was run.

## Commands and exact results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1370` | 0 | rank 980; `planned`; `L0/rework_required`; no legacy slot; theorem incomplete |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `7a489588a59dbd7cca44de7e3b8c3bafcb7448f5`; tree `54d558bf8ed3ea71536ff6a7e6ac7ee67cccfe98` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | `651c8acc...b1d2` and `321626c8...6d81` |
| `cd Formalizations/Lean && git -C .lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `8a178386...eea95`; tree `bdc39a...5e2b` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1370/IntakeProbe.lean` | 0 | all eight adjacent APIs elaborated; no target declaration or proof body |
| `rg -n -i '(\\bKAM\\b\|Kolmogorov[- .]?Arnol.?d\|small[- _]?divisor\|invariant[- _]?(torus\|tori)\|quasi[- _]?periodic.{0,80}Hamilton\|Hamilton.{0,80}quasi[- _]?periodic)' Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean' \| rg -v 'Authors?:\|Hamiltonian\\.lean\|VanKampen\|van.?Kampen\|KolmogorovProcess\|Kolmogorov condition\|Kolmogorov extension\|Kolmogorov quotient\|Kolmogorov-Chentsov\|Chapman-Kolmogorov\|Diophantine\|Bentkamp\|Kaminski\|S1_M_206\\.lean'` | 1 | expected no-match result after documented unrelated categories and the Liouville-Arnold boundary were excluded |
| `rg -n '\\b(sorry\|admit\|sorryAx\|axiom\|constant\|opaque\|unsafe)\\b' Stage1_Instances/THM-M-1370 --glob '*.lean'` | 1 | expected no-match result; no prohibited declaration token |
| `python3 -B Stage1_Instances/THM-M-1370/check_intake.py` | 1 | pre-existing intake validator expects the scheduler's intake state to remain `[ ]`, but current authoritative DAG marks it `[_]`; this stale state assertion is outside the assigned statement phase and was not modified |
| `python3 -m json.tool Stage1_Instances/THM-M-1370/statement-blocker.json` | 0 | blocker is valid JSON |
| `python3 - <<'PY'` (load the blocker JSON; assert item/theorem/base identity, blocked/open state, null canonical target/import/hash/fingerprint, false completion fields, unchanged `H1/M4/R4`, four unrunnable mutations, and absent `.stage1-worker-selftest.json`) `PY` | 0 | all asserted blocker invariants agree |
| `git diff --check -- Stage1_Instances/THM-M-1370` plus per-file `git diff --no-index --check /dev/null` for both blocker files | 0 | no whitespace diagnostics; per-file exit 1 was only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | worker self-test manifest is absent as required for a blocked phase |

## Unblocking condition

An accountable source owner must preserve and hash one lawful complete edition, select and
independently approve its exact result and proof boundary, reconcile the 1954/1963 attribution and
translation record, and freeze every incorporated definition, assumption, conclusion, constant
dependency, and boundary case. A later statement run can then encode that same claim, establish
minimal imports, serialize its elaborated expression and environment, check transports, and run
all four mutation classes.

Until those prerequisites hold, no exact statement, proof, audit completion, or theorem completion
is claimed. Because the assigned phase is not genuinely self-tested to its completion gate, no
`.stage1-worker-selftest.json` is emitted.
