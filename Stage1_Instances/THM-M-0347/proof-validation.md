# THM-M-0347 proof-phase validation

Item: `S56-M-0347-PROOF`. Base revision
`9e1db93a3c4b869cc7c1f8ac99b6c1b12cb4c82c`, tree
`0499e20448fdcec5b57b47cc034570b35aab32a1`.

## Implemented proof route

`AtlasFourierSeries.lean` is an exact immutable snapshot of the complete
Fejer proof in `facebookresearch/atlas-lean`. It constructs the Fejer kernel,
proves its integral mass and positivity, rewrites Cesaro means as convolution,
derives the required off-origin decay and approximate-identity estimate, and
proves uniform convergence for every bundled continuous function.

`Proof.lean` proves pointwise checked adapters for both frozen definitions and
then supplies the premise-free declaration

```text
Stage1Instances.THM_M_0347.fejerTheorem :
  Stage1Instances.THM_M_0347.FejerTheoremTarget
```

The conclusion is the unchanged exact target from `Statement.lean`: arbitrary
positive real period, complex-valued continuous map, symmetric frequencies,
means of `S_0` through `S_n`, and continuous-map topology. No premise, domain,
indexing convention, or convergence mode is weakened or substituted.

## Provenance and license boundary

The proof body is from `facebookresearch/atlas-lean`, commit
`34ffed396f376454c1a9b297f3fd74c5c801fb50`, tree
`c12fe2315fe475d70a4fcee81d6b731f853373ab`, file
`Atlas/IntroductionToFunctionalAnalysis/code/FourierSeries.lean`, blob
`5d399cda446f9bd901902b281bb796123c5ec856`. The exact source SHA-256 is
`f205a16c5146232c7c23e66a018ebd2dd954d70c5c481de5491d3b0cc8752f4f`.
The complete upstream license is retained in `ATLAS-LICENSE`.

ATLAS specifies CC BY-NC 4.0 and adds a rider prohibiting use to train,
fine-tune, distill, evaluate, or otherwise develop ML models. Compatibility
with this repository and this automation context is unreviewed. This is an
explicit proof-acceptance and release blocker, not a passed license gate.

The earlier cutoff-bound `anchor-audit.json` remains valid for the candidate
set it actually searched. This proof was discovered after that audit and does
not retroactively alter its evidence. The current receipt pins the new source
without claiming the earlier audit found it.

## Status boundary

The exact root declaration is locally kernel-closed and is an `M0-P`
candidate. It is not accepted M0 or accepted root closure. The frozen
architecture has planned internal fingerprints rather than independently
checked per-node composition certificates, so
`closed_obligation_ids=[]`, `accepted_closed_obligation_ids=[]`, and
`accepted_root_closed=false` remain mandatory pending master review.

The authoritative vector remains `H1/M3/R4`. Primary-source H0, readable R0,
full transitive provenance and TCB review, license acceptance, E0 hermetic
replay, independent verification, validation, release, audit completion,
theorem completion, and master acceptance remain open.
`theorem_complete=false`.

## Commands and results

Validation ran on 2026-07-15 local time (2026-07-15 UTC). The required
`lake env lean` path is not usable because the shared canonical pinned
`.lake/packages/flt-regular` directory has an invalid Git `HEAD`. The worker
did not repair, fetch, update, build, or otherwise mutate `.lake`. The final
recipe invokes the pinned Lean executable directly inside an isolated,
network-disabled temporary directory with explicit already-compiled paths.
Those transitive artifacts are not fully content-addressed here, so this is
warm provisional proof evidence, not E0 or release evidence.

```text
bash Stage1_Instances/THM-M-0347/check_proof.sh
  exit 0: temporary --trust=0 elaboration passed for Statement.lean,
  the exact ATLAS source, the axiom probe, and Proof.lean; the exact root and
  eight major supporting declarations reported exactly propext,
  Classical.choice, and Quot.sound; all packet bindings passed

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and all 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets at ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-0347
  exit 0: execution rank 840; planned; theorem_complete=false

env PYTHONOPTIMIZE=1 python3 Stage1_Instances/THM-M-0347/check_proof.py
  exit 1 as expected: fail-closed checker rejected disabled assertions

git diff --check -- Stage1_Instances/THM-M-0347 .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics
```

This is self-tested proof-phase evidence pending dependency-ordered master
acceptance. It does not claim validation, release, audit completion, or theorem
completion.
