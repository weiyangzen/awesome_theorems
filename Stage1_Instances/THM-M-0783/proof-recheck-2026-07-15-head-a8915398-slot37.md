# THM-M-0783 proof recheck at a8915398 (slot37)

Item: `S56-M-0783-PROOF`

Intent: `prove`

Recorded: 2026-07-15 (`Asia/Shanghai`)

Base revision: `a891539807529404c603663972e3ba530ae004ba`

Base tree: `0ef8cb5412fcd35d2cebb1be999cea173ed761eb`

## Verdict

`blocked`. The exact proposition `Stage1Instances.THM_M_0783.MartinsAxiom` has no
placeholder-free proof body in the pinned repository-local dependency closure. Martin's axiom is
an additional set-theoretic axiom, rather than a theorem derivable from the selected Lean
foundation. This attempt does not introduce it with `axiom`, assume it as a premise, weaken its
cardinal or forcing hypotheses, or count a conditional transport as root closure.

The proof item remains `[ ]`, lifecycle remains `planned`, and the root remains
`[H5, M4, R4]`. No receipt acceptance, audit completion, theorem completion, validation, release,
or master acceptance is claimed. Because the requested positive proof phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.

## First failed gate

`M0783-L-DENSE-FAMILY` remains open. Its Lean interface is definitionally
`ExpandedMartinsAxiom`, so it must construct, uniformly for every cardinal below the continuum,
one filter meeting every suitably bounded dense family in every nonempty ccc partial order. The
existing theorem
`Stage1Instances.THM_M_0783.ObligationTree.root_of_denseFamilySolver` consumes exactly that open
proposition and transports it to the canonical target. It is valid composition evidence, not a
proof of the premise.

The proof-relevant root cut remains:

```text
M0783-L-DENSE-FAMILY
```

The complete frozen root cut additionally retains the source, foundation, provenance, readable,
and workflow gates recorded by the obligation-tree receipt. A bounded scan of repository-local
pinned package sources found no Martin's-axiom declaration or dense-family solver. The few
mathlib occurrences of the word "forcing" are unrelated documentation or commentary.

## Smallest real validation

The automation-provided `.lake` symlink was treated as read-only. The required
`lake env lean` route was attempted but timed out while Lake tried to resolve the shared
`flt-regular` checkout, whose `HEAD` is the invalid ref `refs/heads/.invalid`. Lake internally
started a fetch before the process was terminated; this worker did not invoke or authorize that
fetch and did not run update, build, clone, checkout repair, or any deliberate `.lake` mutation.
The checkout's invalid state existed before validation and remained invalid afterward. This
shared-artifact defect is a validation-lane failure, separate from the mathematical proof blocker.

As supplemental narrow kernel evidence, the same pinned Lean 4.29.0 executable was invoked
directly at trust level zero with `LEAN_PATH` assembled from the existing pinned package object
directories. It elaborated the exact statement and conditional composition into a removed
temporary directory. This fallback does not satisfy the requested `lake env lean` lane and does
not prove Martin's axiom.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0783` | 0 | rank 788, planned, legacy artifacts unaccepted, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0783/check_obligation_tree.py` | 0 | 12 obligations and 28 typed edges passed; denominator `0581a4ed...25532c9`; root open M4 |
| `python3 Stage1_Instances/THM-M-0783/check_statement.py` | 1 | Lake stopped before elaboration because shared `flt-regular` could not resolve `HEAD` |
| `timeout 5s env GIT_TERMINAL_PROMPT=0 lake env lean --version` from `Formalizations/Lean` | 124 | Lake did not reach Lean; invalid shared `flt-regular` `HEAD` triggered an attempted dependency fetch, so the command was terminated |
| pinned Lean `--trust=0 -t0` with explicit package-object `LEAN_PATH` on `Statement.lean` | 0 | exact canonical target elaborated to an isolated temporary olean |
| same pinned trust-zero fallback on `ObligationTree.lean`, with the temporary statement olean first on `LEAN_PATH` | 0 | conditional composition elaborated; reported axioms exactly `[propext, Classical.choice, Quot.sound]` |
| scoped prohibited-construct scan of owned Lean source | 1 | expected no-match: no `sorry`, `admit`, bodyless declaration, `sorryAx`, unsafe/oracle escape, or proof placeholder |
| scoped Martin-axiom declaration scan across installed pinned package Lean sources | 1 | expected no-match: no exact declaration, proof body, or dense-family solver was found |
| scoped `forcing` scan in pinned mathlib | 0 | only unrelated model-theory documentation, order-ideal commentary, and incidental prose |
| `git diff --check -- Stage1_Instances/THM-M-0783 .stage1-worker-selftest.json` | 0 | no whitespace errors at the validation point |

The direct fallback used this read-only object path pattern:

```bash
ROOT=$PWD
LEAN_ROOT=$ROOT/Formalizations/Lean
LEAN=$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean
LEAN_PATH=$(find "$LEAN_ROOT/.lake/packages" -type d \
  -path '*/.lake/build/lib/lean' -print | sort | paste -sd: -)
LEAN_PATH="$LEAN_ROOT/.lake/build/lib/lean:$LEAN_PATH"
LEAN_PATH="$LEAN_PATH" LEAN_NUM_THREADS=1 timeout 300 "$LEAN" \
  --trust=0 -t0 -R "$ROOT/Stage1_Instances/THM-M-0783" \
  -o /tmp/thm-m-0783-direct/Statement.olean \
  "$ROOT/Stage1_Instances/THM-M-0783/Statement.lean"
```

For `ObligationTree.lean`, the removed temporary object directory was placed first on
`LEAN_PATH`. No repository object was emitted.

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`; Lake manifest SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Retry condition

Resume positive proof execution only after placing an immutable, license-compatible Lean 4 proof
body for the exact frozen target into the pinned repository-local closure, with acceptable axiom,
placeholder, provenance, and composition reports. Alternatively, the master may correct the
execution policy by moving this additional axiom to a theory-extension or independence target;
that would be a target-policy change, not completion of this proof item. The shared pinned Lake
checkout must also be restored by the owning integration lane before `lake env lean` evidence can
be collected.
