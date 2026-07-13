# THM-M-1148 proof-phase validation

Item: `S56-M-1148-PROOF`. Base revision
`0afbf514f9bd5f339943542106f6b811869fe572`, tree
`adbd9c80e360931a3e7c51cae73dda809b5bed65`.

## Implemented proof route

`PoissonUnitDisk.lean` proves the Poisson extension theorem on the unit disk.
It identifies the Poisson integral with the real part of a Herglotz integral,
proves interior harmonicity, rewrites the integral through a Mobius
transformation of the circle, obtains boundary convergence by dominated
convergence, and joins the interior and boundary pieces continuously. It then
pulls the construction back along `w |-> (w - c) / R` for an arbitrary center
and positive radius.

`Proof.lean` packages that construction as `dirichletExtension`, uses the
pinned mathlib Poisson representation theorem for the formula, and proves

```text
Stage1Instances.THM_M_1148.Proof.poissonIntegralFormula :
  Stage1Instances.THM_M_1148.PoissonIntegralFormula
```

The declaration is the unchanged elaborated target from `Statement.lean`.
It has no additional premise, substituted domain, or weakened conclusion.

## Provenance and boundary

The Herglotz and Mobius boundary-convergence developments are adapted from
`facebookresearch/atlas-lean`, commit
`34ffed396f376454c1a9b297f3fd74c5c801fb50`, file
`Atlas/ComplexVariables/code/Lecture16.lean`, regions 38-194, 196-768, and
770-789. The immutable source SHA-256 is
`e6eee1fa36081cf1a83c1394541fdefe5714d8b42d86bcb88210e1dbd94628da`.
The exact adapted declaration list and local additions are recorded in
`proof-receipt.json`; the complete upstream license is retained in
`ATLAS-LICENSE`.

ATLAS permits adapted material only for noncommercial use and adds a rider
prohibiting use to train, fine-tune, distill, evaluate, or otherwise develop
ML models. Compatibility with this repository and automation context has not
been reviewed. This is an explicit proof-acceptance and release blocker, not
a passed supply-chain gate.

## Status boundary

The exact root kernel declaration is closed locally and is an `M0-L`
candidate. It is not accepted `M0-L` or accepted root closure: this warm,
dirty worker receipt is not E0, is not content-addressed, and receives no
individual frozen-obligation credit. The frozen internal targets mostly have
only planned prose fingerprints, and the checked proof replaces the planned
near/far-arc route with a Mobius-transform route. Therefore
`closed_obligation_ids=[]`, `accepted_root_closed=false`, and internal
composition credit remains false pending master review or an architecture
supersession.

The authoritative accepted vector remains `H2/M4/R4`. H0, R0, complete
provenance/trust review, validation, hermetic replay, independent verification,
license acceptance, release, and master acceptance remain open.
`theorem_complete=false`.

## Commands and results

Validation ran on 2026-07-14 local time (2026-07-13 UTC). An earlier
Lake-based checker invocation unexpectedly attempted to materialize the
missing pinned `flt-regular` package through the shared canonical `.lake`
symlink. It left an incomplete Git directory and violated this worker lane's
no-fetch/no-mutation rule. The worker did not repair or delete that shared
state. The final proof recipe invokes the pinned Lean executable directly
with explicit paths to already present compiled mathlib and transitive
dependency artifacts, and does not invoke Lake or perform network/dependency
operations. Those transitive artifact revisions are not fully bound here, so
this remains warm provisional evidence rather than E0 or release evidence.

```text
bash Stage1_Instances/THM-M-1148/check_proof.sh
  exit 0: temporary --trust=0 elaboration passed for Statement.lean,
  PoissonUnitDisk.lean, and Proof.lean; all 28 recorded declarations reported
  exactly propext, Classical.choice, and Quot.sound; packet bindings passed

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and all 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets at ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-1148
  exit 0: execution rank 353; planned; theorem_complete=false

python3 Stage1_Instances/THM-M-1148/check_statement.py
  exit 0: expression fingerprint and five structural mutations passed; this
  ancillary checker completed after the shared environment became usable
  again, but the final proof recipe remains the direct-Lean recipe above

python3 Stage1_Instances/THM-M-1148/check_anchor_audit.py
  exit 0: pinned mathlib anchor audit passed

python3 Stage1_Instances/THM-M-1148/check_obligation_tree.py
  exit 0: frozen 26-obligation, 51-edge architecture passed structurally;
  its accepted root remained open at M4

env PYTHONOPTIMIZE=1 python3 Stage1_Instances/THM-M-1148/check_proof.py
  exit 1 as expected: fail-closed checker rejected disabled assertions

git diff --check -- Stage1_Instances/THM-M-1148 .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics
```

This is self-tested proof-phase evidence pending dependency-ordered master
acceptance. It does not claim validation, release, audit completion, or
theorem completion.
