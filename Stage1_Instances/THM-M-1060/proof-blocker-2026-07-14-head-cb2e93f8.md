# THM-M-1060 proof-phase execution at cb2e93f8

Item: `S56-M-1060-PROOF`

Execution date: `2026-07-14` (`Asia/Shanghai`)

Base revision: `cb2e93f820239a49e31c5521ea88c2b7d2a32674`

Base tree: `cd4790bb5a0ddff8b2d2475416295f0112551e20`

## Verdict

`blocked`. This execution adds five placeholder-free local proof bodies in
`Proof.lean`, but they cover only probability, measurability, continuity, and
the zero-time finite-dimensional-law boundary. They do not establish the full
Wiener normalization package or any large-deviation bound. No proof body for
the exact target `Stage1Instances.THM_M_1060.SchilderTarget` exists in the
owned source or pinned dependency closure.

The lifecycle remains `planned`, the root vector remains
`[H2, M3, R4] -> [H2, M3, R4]`, and no frozen obligation is closed. The `M3`
classification records that exact definitions and checked interfaces exist;
it does not claim analytic proof closure. The older graph's `root_machine_debt`
field says `M4`, but the instance manifest and rev-5.6 definition classify the
exact elaborated statement plus conditional interfaces as `M3`. This evidence
does not mutate the prerequisite graph merely to reconcile that historical
field.

## Implemented Bodies

| Declaration | Checked contribution | Open boundary |
|---|---|---|
| `isProbabilityMeasure_of_isWienerMeasure` | extracts the probability component of the frozen Wiener predicate | no increment, covariance, or path-law normalization |
| `measurableEvaluationLinear` | proves measurability of every finite linear combination of path evaluations | no dyadic projection construction or LDP |
| `continuousScale` | proves continuity of scalar multiplication on based paths | no exponential approximation or law bound |
| `zeroTimeVarianceAndLaw` | specializes the frozen law at time zero and derives variance zero | only the degenerate time boundary |
| `zeroTimeLaw` | identifies that boundary law as `gaussianReal 0 0` | no positive-time Gaussian or Brownian increment package |

All five declarations elaborate at trust level zero and report exactly
`propext`, `Classical.choice`, and `Quot.sound`. Four are genuine partial
`M1060-N-WIENER` substrate, while `continuousScale` belongs to
`M1060-S-DEFINITIONS`/map-side substrate. The zero-time result is a boundary
sanity check only: it does not discharge `M1060-S-BOUNDARY`, whose epsilon
filter, empty-set, and extended-real pieces remain open. No body meets a frozen
obligation's full output, so no closed obligation ID or proof receipt is issued.

## Failed Gate And Cut Sets

The first failed implementation gate is `M1060-N-WIENER`: the finite-law
predicate has not been developed into the full increment, covariance, and
path-law interface consumed by the selected polygonal proof. Beyond it, the
pinned closure has no finite Gaussian LDP, dyadic projected-law LDP, Brownian
exponential modulus estimate, exponential-equivalence transfer, exact rate
identification, lower-semicontinuity proof, or compact-sublevel proof.

Two useful frontiers must not be conflated:

- The frozen graph's implementation cut is `M1060-L-GAUSSIAN`,
  `M1060-L-MODULUS`, `M1060-L-EXP-EQUIV`, `M1060-L-RATE-ID`,
  `M1060-L-RATE-LSC`, and `M1060-L-SUBLEVEL-BOUND`.
- The immediate semantic terminal frontier is `M1060-T-LOWER`,
  `M1060-T-UPPER`, and `M1060-T-GOOD`.

`ObligationTree.lean` merely conjoins those three terminal packages when they
are supplied as hypotheses. It does not construct them. Pinned mathlib search
found only an unrelated AddCircle documentation use of "exponential
equivalence" and no probabilistic Schilder, LDP, Cameron-Martin, or Laplace
principle terminal body. Repo-local results are interfaces and scaffolds, not
an exact proof candidate.

## Definition Sanity Probe

A temporary, deleted Lean probe ruled out a cheap inconsistent-premise or
definition-collapse proof. It checked that the time-zero law is consistently
the constant-zero Gaussian, the zero path has a genuine `g = 0` rate
candidate, the empty-open LDP case reduces to the correct bottom boundary, and
the universal probability expression reduces to zero. Thus neither
`IsWienerMeasure` nor `SmallNoiseLDP` trivializes the exact root.

## Validation

All checks used the automation-provided, pre-existing `.lake` symlink to the
canonical pinned artifacts. No `lake update`, `lake build`, dependency
clone/fetch, network access, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1060` | 0 | rank 503; planned; L0/rework-required; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1060/check_obligation_tree.py` | 0 | 21 obligations and 83 typed edges passed; denominator `32d2df11...b2a3f74`; recorded graph root open |
| `tmp=$(mktemp -d); cp .../{Statement,Proof}.lean "$tmp"; cd Formalizations/Lean; lake env lean --trust=0 --root "$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean"; LEAN_PATH="$tmp:$(lake env printenv LEAN_PATH)" lake env lean --trust=0 --root "$tmp" "$tmp/Proof.lean"` (temporary files removed) | 0 | `statement_exit=0 proof_exit=0`; exact statement and all five partial bodies elaborated; each body reports only `propext`, `Classical.choice`, and `Quot.sound` |
| `cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-1060/Statement.lean` | 0 | exact canonical target elaborated and printed |
| `cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-1060/ObligationTree.lean` | 0 | both conditional composers elaborated at their frozen signatures |
| token-anchored prohibited-device scan over owned `*.lean` | 1 | expected no-match exit; no `sorry`, `admit`, axiom declaration, unsafe/oracle, or equivalent prohibited construct |
| pinned-mathlib topical scan for Schilder/LDP/Cameron-Martin/exponential equivalence/Laplace principle | 0 | one unrelated AddCircle documentation hit; no probabilistic terminal declaration |
| `cd Formalizations/Lean && lake env lean ../../.m1060_probe.lean`, followed by deletion and `test ! -e .m1060_probe.lean` | 0 | all sanity lemmas elaborated; scratch file removed |

## Retry And Status Boundary

Resume after implementing the frozen analytic packages without placeholders,
or after identifying an immutable compatible Lean 4 Schilder proof that can be
pinned, exact-type checked, and provenance-audited without changing the
dependency lock.

This is partial proof work plus fresh nonrelease blocker evidence. It does not
satisfy `S56-M-1060-PROOF`, change scheduler/DAG state, close the root, or claim
audit completion, theorem completion, validation, release, receipt acceptance,
or master acceptance. Because the assigned proof phase remains incomplete,
`.stage1-worker-selftest.json` is deliberately absent.
