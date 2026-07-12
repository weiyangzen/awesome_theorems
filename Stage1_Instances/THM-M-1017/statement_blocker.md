# Statement-phase blocker

Item: `S56-M-1017-STATEMENT`

Base revision: `5c89c7c48434a9831837db81663d8ef0715c05cd`

Verdict: `blocked`. No canonical Lean expression was created or elaborated, and no statement-gate
receipt or theorem-completion credit is claimed.

## First failed gate

The exact-source identification gate fails before Lean elaboration. The complete repository source
wording for this target is only `由特征函数恢复分布` (recover a distribution from its
characteristic function), in `Docs/researches/math_theorems.md`. It gives no formula, hypotheses,
normalization, recovered quantity, or boundary convention.

At least the following inequivalent claims fit that wording:

1. an interval-mass or distribution-function inversion formula, with continuity/atom endpoint
   conditions and a limit of truncated oscillatory integrals;
2. pointwise density recovery by Fourier inversion, requiring density and integrability
   hypotheses;
3. uniqueness of probability measures from equality of their characteristic functions.

Choosing any one would silently narrow or substitute the screened claim. This is prohibited by the
rev-5.6 statement gate and by the assigned task's exact-target requirement. In particular,
`THM-M-1018` is separately named Levy inversion formula and `THM-M-1019` is separately named the
uniqueness theorem in the target manifest; their proximity is useful disambiguation evidence but
does not supply the missing formula for `THM-M-1017`.

## Validation record

Run on 2026-07-12 in the worker automation clone. The canonical `.lake` directory is a read-only
reuse symlink for this run; no dependency update, fetch, clone, or build was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`; 1546 unique targets with ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1017` | 0 | rank 493, lifecycle `planned`, lane `hard_mathlib_anchor_and_wrapper`, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `python3 -m json.tool Stage1_Instances/THM-M-1017/intake.json` | 0 | intake record is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1017` | 0 | no whitespace errors |

There is deliberately no `lake env lean <file>` result: without an exact proposition, a generated
Lean declaration would be a placeholder or substituted theorem rather than validation of the
assigned target. Availability of the pinned executable does not cure the semantic blocker.

## Retry condition

An integration-lane decision or authoritative primary-source pinpoint must identify the exact
formula and freeze all of the following: ordered binders; probability-measure representation;
characteristic-function sign convention; recovered distributional quantity; endpoint ordering,
continuity, and atom behavior; truncation/limit mode; normalization constants; and all
integrability/density hypotheses. The statement phase can then select minimal pinned imports,
elaborate and fingerprint that exact expression, compile checked transports, and run the required
removed-hypothesis, changed-domain, binder-scope, and boundary mutations.

Because those prerequisites are absent, this phase is not genuinely self-tested and no
`.stage1-worker-selftest.json` is emitted.
