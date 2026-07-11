# THM-M-0405 intake dossier

## Instance

- Item: `S56-M-0405-INTAKE`
- Lifecycle: `planned`
- Baseline: `L0 / rework_required`
- Execution rank: 18
- Lane: `hard_mathlib_anchor_and_wrapper`
- Category: number theory / Diophantine equations
- Historical title: Bilu theorem (比拉斯基定理)
- Historical gloss: prime factors of linear recurrence sequences
- Theorem completion: false
- Intake evidence status: provisional worker evidence, pending master acceptance

The manifest's `已验证` label is untrusted metadata. No historical Lean file, source
label, or mathematical publication receives proof credit at intake.

## Source-statement crosswalk

| Surface | Recorded claim | Intake interpretation |
|---|---|---|
| `Docs/researches/math_theorems.md` | Yuri Bilu; 1995; prime factors of linear recurrence sequences | Discovery metadata only. It is too short to determine a theorem statement. |
| `Docs/Stage1_Blueprint.md` | Bilu theorem; same subject; formalization status `已验证` | Queue metadata only; explicitly not completion evidence. |
| Legacy `S1_M_018.lean` | Selects Bilu-Hanrot-Voutier (BHV), *Existence of primitive divisors of Lucas and Lehmer numbers* | Candidate source and object-model discovery only under rev-5.6. |
| BHV, J. reine angew. Math. 539 (2001), 75-122 | Every Lucas or Lehmer number of index `n > 30` has a primitive divisor; lower defective terms are classified | Preferred canonical human claim, subject to primary-source page/theorem/definition audit in the statement and anchor phases. |
| Voutier, Math. Comp. 64 (1995), 869-888 | Predecessor on primitive divisors of Lucas and Lehmer sequences | Explains the historical year but is not silently substituted for the BHV target. |

The historical row conflates author/year/subject and does not contain enough
assumptions to freeze an exact theorem. The preferred reading is the BHV
primitive-divisor theorem because it matches Bilu and prime factors of linear
recurrences. Exact source theorem number, pages carrying the statement,
definitions, hypotheses, and errata remain deliberately open for the later
source audit. This intake does not claim `H0`.

## Scope map

### Included target

The intended root is the conjunction of the Lucas and Lehmer branches: for
each admissible Lucas pair or Lehmer pair in the source sense and every natural
index `n > 30`, its `n`-th number has a primitive prime divisor in the source
sense. Admissibility, integrality conventions, the Lucas/Lehmer term formulas,
and branch-specific factors excluded by "primitive" must be transcribed from
the primary paper rather than inferred from the legacy recurrence model.

### Boundaries and exclusions

- The finite classification for `n <= 30` is source context, not part of the
  `n > 30` existence root unless the primary statement makes it conjunctive.
- A theorem about an arbitrary integer linear recurrence is broader than BHV
  and is excluded.
- The integer-parameter recurrence in legacy `S1_M_018.lean` is not accepted as
  equivalent to the algebraic-integer Lucas/Lehmer definitions.
- Fibonacci, Mersenne, Lucas primality, elliptic divisibility sequences, and
  arithmetic-dynamics results are examples or search anchors, not substitutes.
- No claim about all prime factors, greatest prime factors, density, or growth
  is imported from the historical gloss.

### Profiles

- Foundation: Lean 4 + pinned mathlib, classical mathematics permitted only
  when exposed by the eventual declaration's axiom report.
- Computation: ordinary kernel reduction; no native/oracle result is accepted.
- TCB: Lean kernel, toolchain, pinned dependencies, and build scripts; exact
  versions are deferred to the statement environment fingerprint.
- Expected debt at intake: `formalization_debt`; public Lean closure has not
  been established by this phase.

## Open task DAG

| Node | Depends on | Required output | State |
|---|---|---|---|
| `S56-M-0405-STATEMENT` | intake acceptance | Exact primary-source scope and elaborated Lean target with minimal pinned imports | open |
| `S56-M-0405-ANCHOR_AUDIT` | statement | Immutable mathlib/external candidate inventory and proof-body provenance | blocked by predecessor |
| `S56-M-0405-OBLIGATION_TREE` | anchor audit | Frozen typed obligation and assurance graphs | blocked by predecessor |
| `S56-M-0405-PROOF` | obligation tree | Exact proof bodies or pinned/imported closure | blocked by predecessor |
| `S56-M-0405-VALIDATION` | proof | Kernel, trust, provenance, hermetic, and independent evidence | blocked by predecessor |
| `S56-M-0405-RELEASE` | validation | Audit and theorem verdicts reconciled independently | blocked by predecessor |

## Intake validation receipt

Base revision: `a8d6489fd935cd71fa4499f2f3f5b051998203f4`.

Preflight and scoped checks were run from the repository root on 2026-07-12:

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard valid: 15 assurance groups and 1546 uniform-L0 targets. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0405` | 0 | Membership, rank 18, planned lifecycle, and incomplete theorem confirmed. |
| `python3 -m json.tool Stage1_Instances/THM-M-0405/instance.json` | 0 | Structured intake parses. |
| `git diff --check -- Stage1_Instances/THM-M-0405 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

Status boundary: the intake dossier, scope map, crosswalk, and open DAG are
self-tested. The canonical Lean expression, source fidelity, proof closure,
and all later rev-5.6 gates remain open. No theorem completion is claimed.
