# THM-M-0590 proof phase blocked at `b946eecc`

Item: `S56-M-0590-PROOF`

Recorded: `2026-07-15T09:06:30+08:00`

Base revision: `b946eecc7cde20700ed2dae9454ed0da0efeba76`

Base tree: `313de7829d81965f35bf136d1fb878cbadca331d`

## Verdict

`blocked`. No eligible proof body closes the exact frozen Lean target. The
target is the full Brown-Douglas-Fillmore classification of essentially normal
bounded operators on separable infinite-dimensional complex Hilbert spaces by
essential spectrum and the off-spectrum Fredholm-index function.

`THMM0590.root_of_directional_packages` is placeholder-free and checks under
`--trust=0`, but it consumes `ForwardInvariantPackage` and
`BackwardClassificationPackage`. Those parameters are exactly the two missing
directional BDF proofs. The declaration checks final biconditional composition;
it does not inhabit `brownDouglasFillmoreTarget` unconditionally.

Pinned mathlib supplies compact-operator, adjoint, ordinary-spectrum, and
compact-operator Fredholm-alternative support. The pinned source search found no
Calkin-algebra, general Fredholm-index, essential-spectrum, Busby-extension, or
BDF-classification implementation. A scoped repo-local Lean search likewise
found no unconditional body outside this dossier. Fresh bounded Sourcegraph
searches, including indexed archived and forked repositories, found no relevant
Lean body for the target or missing infrastructure. The grep.app lane was HTTP
429 rate-limited. These are bounded discovery results, not a global
nonexistence claim.

No premise, axiom, placeholder, weaker target, changed convention, or moving
dependency was added. The proof item remains `[ ]`; the root remains
`[H1, M4, R3]`. No proof, validation, release, theorem-completion, receipt, or
master-acceptance claim is made. Because the proof phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.

## Split Required

Eight integrated unresolved proof-recheck pairs existed before this run, so
this is the ninth root-sized recheck. The authoritative DAG still records
`attempts=0` and `children=[]`. Rev-5.6 section 10.2 requires a split after five
unresolved execution ticks rather than another root-sized assignment. This
worker cannot edit scheduler authority or the generated checklist, so the
master must reconcile the cursor and create dependency-legal child tasks before
another proof retry.

The frozen architecture identifies suitable child boundaries:
`M0590-S-BOUNDARY`, `M0590-S-FOUNDATION`, `M0590-N-CALKIN`,
`M0590-N-FREDHOLM`, `M0590-L-FWD-SPECTRUM`, `M0590-L-FWD-INDEX`,
`M0590-B-FORWARD`, `M0590-C-BUSBY`, `M0590-L-EXT-CLASS`,
`M0590-L-INDEX-COMPLETE`, and `M0590-T-BACKWARD`.

## Failed Gate And Retry

The first failed gate is terminal proof-body availability for
`M0590-B-FORWARD` and `M0590-T-BACKWARD`; these obligations are the remaining
root cut set. Closing them still requires Calkin and Atkinson bridges, forward
invariance of essential spectrum and Fredholm index, Busby extensions, BDF
extension classification, and completeness of the index invariant.

Do not schedule the same root-sized proof item unchanged. Resume a split child
only when its exact placeholder-free Lean body can be implemented, or when a
licensed immutable compatible Lean 4 dependency supplies it and passes
exact-type, provenance, axiom, placeholder, composition, and pinned-replay
checks. A citation or conditional composer does not satisfy this condition.

## Validation

Commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` link to canonical pinned artifacts was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, or `.lake`
mutation was performed. Temporary Lean objects were created under `/tmp` and
removed. Network use was limited to bounded public source discovery; the Lean
replay and dependency checks used the existing pinned closure.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0590` | 0 | Rank 630; lifecycle `planned`; hard-statement-first lane; legacy artifacts unaccepted; theorem incomplete. |
| `git status --short` | 0 | At start, only the automation-provided untracked `Formalizations/Lean/.lake` link was present. |
| `python3 Stage1_Instances/THM-M-0590/check_obligation_tree.py` | 0 | 17 obligations and 37 typed edges passed; denominator `2d5b17d162ed0ef7a445673a25243da41d3aeb4a2be8f39eab68511e1809a9e8`; root and both directional packages remain open M4. |
| Isolated `lake env lean --trust=0 -t0` replay of `Statement.lean` and `ObligationTree.lean` | 0 | Exact target and conditional composition elaborated; target stdout SHA-256 `0d233828...f14b`, composer stdout SHA-256 `05a0a820...03a`, and composer axioms `[propext, Classical.choice, Quot.sound]`; stderr was empty. |
| Owned Lean prohibited-construct scan | 1 (expected) | No `sorry`, `admit`, `sorryAx`, axiom/bodyless declaration, unsafe/oracle, implementation override, or native-decision shortcut was found. |
| Repo-local exact-name Lean search outside this dossier | 1 (expected) | No unconditional root or directional-package body was found. |
| Pinned-mathlib target/API search | 1 (expected) | No BDF target or missing Calkin, Fredholm-index, essential-spectrum, or Busby API was found. |
| Bounded Sourcegraph searches, including `archived:yes fork:yes` | 0 | No relevant BDF or required operator-algebra Lean body was found; broader `IsFredholm` and `Calkin` hits were unrelated false positives. |
| Bounded grep.app Lean searches | 22 | HTTP 429 rate limiter; recorded as an unavailable lane, not negative evidence. |
| Frozen-registry terminal-body assertion | 0 | Fifteen obligations are machine-required: 14 have no terminal body, and `M0590-T-ASSEMBLE` alone records the conditional composer. |
| Mathlib revision/tree/status check | 0 | Revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`, clean dependency worktree. |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake `5.0.0-src+98dc76e`. |
| Prior-recheck count plus authoritative DAG inspection | 0 | Eight prior integrated rechecks; scheduler still says `attempts=0`, `children=[]`, state `[ ]`; split threshold exceeded. |
| JSON parse, blocker invariant assertions, and self-test absence check | 0 | Base/tree, open state, empty proof bodies/receipts, cut set, ninth-recheck split trigger, changed paths, and deliberate self-test absence agreed. |
| Scoped `git diff --check` plus no-index checks for both added files | 0 | No whitespace errors; normal added-file exit 1 was accepted only with empty diagnostic output. |

The exact narrow Lean replay recipe was:

```bash
TMP=$(mktemp -d /tmp/thm-m-0590-proof-b946eecc-slot70.XXXXXX)
LEAN=$(cd Formalizations/Lean && lake env which lean)
LP=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
(cd Stage1_Instances/THM-M-0590 &&
  LEAN_NUM_THREADS=1 LEAN_PATH="$LP" timeout 600 "$LEAN" --trust=0 -t0 \
    -o "$TMP/Statement.olean" Statement.lean)
(cd Stage1_Instances/THM-M-0590 &&
  LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$LP" timeout 600 "$LEAN" --trust=0 -t0 \
    -o "$TMP/ObligationTree.olean" ObligationTree.lean)
rm -rf "$TMP"
```

The exact local source scans were:

```bash
rg -n -i '^\s*(sorry|admit|axiom)(\s|$)|sorryAx|^\s*(constant|opaque)\b[^:=]*$|^\s*unsafe\b|\bextern\b|implemented_by|native_decide|run_tac' \
  Stage1_Instances/THM-M-0590 --glob '*.lean'
rg -n 'brownDouglasFillmoreTarget|ForwardInvariantPackage|BackwardClassificationPackage' \
  --glob '*.lean' -g '!Stage1_Instances/THM-M-0590/**' .
rg -n -i 'Brown.?Douglas.?Fillmore|Calkin|essentialSpectrum|essential spectrum|IsFredholm|fredholmIndex|essentiallyNormal|essentially normal|Busby' \
  Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'
```

The exact public search command shape was:

```bash
curl -L --silent --show-error --max-time 60 --get \
  --data-urlencode 'q=context:global archived:yes fork:yes <TERM> lang:Lean count:100' \
  'https://sourcegraph.com/.api/search/stream'
```

Terms included exact BDF name variants, `essentialSpectrum`, `essentially
normal`, `Busby`, `Calkin algebra`, `Atkinson`, `FredholmIndex`, `KHomology`,
and `UnitaryEquivalent` with `IsCompactOperator`. All completed exhaustive-scope
queries had `skipped=[]`; none produced a relevant body.

This blocker record is not a proof receipt. It does not satisfy
`S56-M-0590-PROOF`, change scheduler state, or claim M0, audit completion,
theorem completion, validation, release, or master acceptance.
