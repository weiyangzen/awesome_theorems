# THM-M-0590 proof phase blocked at `506796f9`

Item: `S56-M-0590-PROOF`

Intent: `prove`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `506796f90c31097a0d170410e431f83da4b1853c`

Base tree: `32c911b35ce53ab8fd2ad6bfd6a34bdc603ef50d`

## Verdict

`blocked`. No eligible proof body closes the exact frozen Lean target. The
target is the full Brown-Douglas-Fillmore classification of essentially normal
bounded operators on separable infinite-dimensional complex Hilbert spaces by
essential spectrum and the off-spectrum Fredholm-index function.

The placeholder-free theorem `THMM0590.root_of_directional_packages` checks
under `--trust=0`, but it consumes `ForwardInvariantPackage` and
`BackwardClassificationPackage`. Those parameters contain exactly the two
missing directional BDF proofs. The declaration checks final biconditional
composition; it does not inhabit `brownDouglasFillmoreTarget` unconditionally.

Pinned mathlib supplies compact-operator, adjoint, and ordinary-spectrum
infrastructure, but the bounded source search found no Calkin-algebra, general
Fredholm-index, essential-spectrum, Busby-extension, or BDF-classification
implementation. The repo-local Lean search likewise found no unconditional
body outside this dossier. The predecessor anchor audit retained no exact
immutable external Lean 4 candidate. Its authenticated GitHub code-search lane
was unavailable. Fresh bounded public Sourcegraph searches found only unrelated
substring/structure matches, so this record still does not claim global
nonexistence.

No premise, axiom, placeholder, weaker target, altered convention, or moving
dependency was added. The proof item remains `[ ]`; the root stays
`[H1, M4, R3]`. No proof, validation, release, theorem-completion, receipt, or
master-acceptance claim is made. Because the requested proof phase is not
complete, `.stage1-worker-selftest.json` is deliberately absent.

## Failed Gate And Retry

The first failed gate is terminal proof-body availability for
`M0590-B-FORWARD` and `M0590-T-BACKWARD`; these obligations are the remaining
root cut set. The frozen route still requires Calkin and Atkinson bridges,
forward invariance of essential spectrum and Fredholm index, Busby extensions,
BDF extension classification, and completeness of the index invariant.

Resume after these obligations have local placeholder-free Lean
implementations, or after an independently audited immutable compatible Lean 4
dependency supplies both exact directional packages plus kernel-checked
exact-type, provenance, axiom, placeholder, composition, and pinned-replay
evidence. A citation or conditional composer does not satisfy this condition.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink to the canonical pinned artifacts was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, or `.lake`
mutation was performed. Temporary Lean objects were created under `/tmp` and
removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0590` | 0 | Rank 630; lifecycle `planned`; lane `hard_statement_first_partial_verification`; legacy artifacts unaccepted; theorem incomplete. |
| `git status --short` | 0 | Before this recheck, only the automation-provided untracked `Formalizations/Lean/.lake` link was present. |
| `python3 Stage1_Instances/THM-M-0590/check_obligation_tree.py` | 0 | 17 obligations and 37 typed edges passed; denominator `2d5b17d162ed0ef7a445673a25243da41d3aeb4a2be8f39eab68511e1809a9e8`; root and both directional packages remain M4. |
| Isolated `lake env lean --trust=0 -t0` replay of `Statement.lean` and `ObligationTree.lean` with a temporary `Statement.olean` | 0 | The exact target and conditional composition elaborated; the target printed `THMM0590.brownDouglasFillmoreTarget.{u_2, u_3} : Prop`, and `#print axioms` reported `[propext, Classical.choice, Quot.sound]`. |
| Prohibited-token `rg` scan (exact command below) | 1 (expected) | No prohibited Lean proof escape occurs in owned sources. |
| Repo-local `rg` proof-body search (exact command below) | 1 (expected) | No retained unconditional root or directional-package body was found. |
| Pinned-mathlib `rg` API search (exact command below) | 1 (expected) | No matching target or missing central API was found in the pinned mathlib source. |
| Four bounded Sourcegraph stream searches shown below | 0 each | Calkin produced 13 false substring matches in one unrelated repository; the Fredholm query produced 14 unrelated local structures; the other two queries produced zero matches. No exact proof body was found; global absence is not claimed. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` plus `status --porcelain=v1` | 0 | Revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`, clean dependency worktree. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| JSON parse plus current-base blocker invariant/source-hash assertions | 0 | Item, base, hashes, denominator, open state, cut set, empty bodies/receipts, changed paths, and self-test absence agreed. |
| Scoped `git diff --check` plus `git diff --no-index --check /dev/null` for both added files | 0 after accepting normal added-file exit 1 | No whitespace errors. |

The exact narrow Lean replay recipe was:

```bash
TMP=$(mktemp -d /tmp/thm-m-0590-proof-506796f9.XXXXXX)
LEAN=$(cd Formalizations/Lean && lake env which lean)
LP=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
(cd Stage1_Instances/THM-M-0590 &&
  LEAN_NUM_THREADS=1 LEAN_PATH="$LP" timeout 600 "$LEAN" --trust=0 -t0 \
    -o "$TMP/Statement.olean" Statement.lean)
(cd Stage1_Instances/THM-M-0590 &&
  LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$LP" timeout 600 "$LEAN" --trust=0 -t0 \
    ObligationTree.lean)
rm -rf "$TMP"
```

The exact source and placeholder search commands were:

```bash
rg -n '^\s*(sorry|admit|axiom)(\s|$)|sorryAx' \
  Stage1_Instances/THM-M-0590 --glob '*.lean'
rg -n 'brownDouglasFillmoreTarget|ForwardInvariantPackage|BackwardClassificationPackage' \
  --glob '*.lean' -g '!Stage1_Instances/THM-M-0590/**' .
rg -n -i 'Brown.?Douglas.?Fillmore|Calkin|essentialSpectrum|essential spectrum|IsFredholm|fredholmIndex|essentiallyNormal|essentially normal|Busby' \
  Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'
```

The exact bounded public search commands were:

```bash
curl -L --max-time 30 -sS -G 'https://sourcegraph.com/.api/search/stream' \
  --data-urlencode 'q=context:global archived:yes fork:yes Calkin lang:Lean count:100' | tail -20
curl -L --max-time 30 -sS -G 'https://sourcegraph.com/.api/search/stream' \
  --data-urlencode 'q=context:global archived:yes fork:yes Busby lang:Lean count:100' | tail -20
curl -L --max-time 30 -sS -G 'https://sourcegraph.com/.api/search/stream' \
  --data-urlencode 'q=context:global archived:yes fork:yes (FredholmIndex OR fredholmIndex OR IsFredholm) lang:Lean count:100' | tail -30
curl -L --max-time 30 -sS -G 'https://sourcegraph.com/.api/search/stream' \
  --data-urlencode 'q=context:global archived:yes fork:yes (essentialSpectrum OR essentiallyNormal OR "essential spectrum") lang:Lean count:100' | tail -30
```

These public searches ran on `2026-07-15` before `06:28:50+08:00`. Exact
client start timestamps and raw response bodies were not preserved, so they are
bounded discovery context rather than content-addressed negative-search
receipts. Their query SHA-256 values, in command order, are
`d3723300710909f6909fb2d013faf3b600c3fefb65a7170dede037d9317baaaa`,
`0b0376f8a5ae5222979c9878b202cb5e235400ffa286633780e76173516e4397`,
`851a380adedef5abc8aaa9bfed3d9ba9380fdd95379689c3af0031dbdd90991e`, and
`501d00367c8ee91b317c721924b1cd90bbd2957b77ea8305d904fee320a81d17`.
Independent read-only Sourcegraph and GitHub REST discovery also queried exact
BDF identifiers and related project names and found no exact candidate. Exact
start times and raw bodies were likewise not preserved. None of these searches
supplies proof credit or establishes global absence, and no dependency or
repository content was downloaded into the workspace.

Exact input hashes, structured outcomes, the open cut set, and the retry
condition are recorded in
`proof-recheck-2026-07-15-head-506796f9.json`. This is durable current-base
blocker evidence, not a proof receipt.
