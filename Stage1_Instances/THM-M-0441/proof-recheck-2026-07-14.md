# THM-M-0441 proof-phase recheck

Item: `S56-M-0441-PROOF`

Intent: `prove`

Base revision: `a3c20fd2f4da1879baa00bd5455573c49d4b2fa0`

Base tree: `2ae6946f2b059449025558b6033de33c332412ee`

Recheck date: 2026-07-14 (Asia/Shanghai)

## Verdict

`blocked`. The exact root remains `[H1, M3, R4]`; no newly available local or
pinned proof body closes a frozen root-critical obligation. This recheck does
not satisfy the proof item and proposes no scheduler state transition.

The existing `Proof.lean` still supplies eleven genuine, placeholder-free
partial bodies for algebraic-part laws, bounded-height finiteness, and the
empty-transcendental-part counting branches. They elaborate at trust level
zero, and their printed axiom sets are subsets of `propext`,
`Classical.choice`, and `Quot.sound`. They do not inhabit any of the four open
fields consumed by `ObligationTree.engine_compose` and do not prove the exact
general proposition `Stage1Instances.THM_M_0441.PilaWilkie`.

## Failed Gate

The first failed gate remains `M0441-C-PARAM`: the pinned Lean closure contains
no placeholder-free uniform o-minimal `C^r` parameterization theorem for the
frozen definability encoding. The determinant estimate (`M0441-L-DET`),
semialgebraic block construction (`M0441-C-BLOCKS`), and dimension induction
with exponent bookkeeping (`M0441-B-INDUCT`) are also absent. The prerequisite
immutable anchor audit found no compatible external terminal body.

Using the conditional `CountingEngine.deriveCounting` field as proof
provenance, or substituting any finite, empty, semialgebraic, or otherwise
specialized result from `Proof.lean`, would assume or weaken the missing
mathematics rather than prove the canonical theorem.

Resume only after those frozen packages are implemented locally without
placeholders, or after an immutable exact Lean 4 Pila-Wilkie terminal proof is
available for pinned integration, exact-type transport, and provenance/trust
validation. Source reconstruction and trust/replay review also remain open.

## Validation

All commands ran in this worker clone and reused the automation-provided
canonical `.lake` symlink read-only. No `lake update`, `lake build`, dependency
clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard, 15 assurance groups, and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0441` | 0 | rank 87; planned hard-mathlib lane; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0441/check_obligation_tree.py` | 0 | 21 obligations and 18 proof edges passed; root remains open. |
| concatenate the three Lean modules with local imports removed, then pipe to `cd Formalizations/Lean && LEAN_NUM_THREADS=1 lake env lean --trust=0 /dev/stdin` | 0 | exact statement, conditional composition, and all eleven partial bodies elaborated; output SHA-256 `9d25f50f...53d78d3`; printed axioms were within the accepted classical profile and contained no `sorryAx`. |
| `rg -n --pcre2 '\b(?:sorry|admit|axiom)\b|sorryAx|unsafe' Stage1_Instances/THM-M-0441 --glob '*.lean'` | 1 | expected no-match exit; no prohibited construct occurs in the owned Lean sources. |
| `python3 -m json.tool Stage1_Instances/THM-M-0441/proof-recheck-2026-07-14.json` | 0 | fresh structured blocker record parsed. |
| `git diff --check -- Stage1_Instances/THM-M-0441 .stage1-worker-selftest.json` | 0 | no whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test manifest deliberately absent. |

The narrow Lean recipe was:

```bash
set -o pipefail
{
  sed '/^import Statement$/d' Stage1_Instances/THM-M-0441/Statement.lean
  sed '/^import Statement$/d' Stage1_Instances/THM-M-0441/ObligationTree.lean
  sed '/^import ObligationTree$/d' Stage1_Instances/THM-M-0441/Proof.lean
} | (cd Formalizations/Lean &&
  LEAN_NUM_THREADS=1 lake env lean --trust=0 /dev/stdin)
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; `lake-manifest.json` SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

This is fresh nonrelease blocker evidence, not a proof receipt, proof-phase
self-test, theorem-completion claim, validation/release result, or master
acceptance. Because the assigned proof deliverable remains incomplete,
`.stage1-worker-selftest.json` is deliberately absent.
