# THM-M-1259 proof-phase recheck at base `d5771f24`

Item: `S56-M-1259-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T18:18:16+08:00`

Base revision: `d5771f240b8fe26277d018c90fec963af76ed7f2`

Base tree: `f274a52fcf9e5edcd6b8f8dd43726122a041af50`

## Verdict

`blocked`. No consistent positive proof body can inhabit the exact frozen target. The existing
owned, placeholder-free declaration

```text
Stage1Instances.THM_M_1259.Counterexample.not_hormanderTarget :
  Not Stage1Instances.THM_M_1259.hormanderTarget
```

freshly kernel-checks at trust level zero against the existing pinned Lean and mathlib artifacts.

The target permits `n = r = 0` and quantifies over every measure. At the zero measure,
`IsSmoothDistribution` characterizes only the zero distribution. In zero-dimensional Euclidean
space, bracket generation and coefficient smoothness are automatic, the bundled zero operator maps
the nonzero evaluation distribution to zero, and that zero image is smooth. The target would
therefore make the nonzero evaluation distribution smooth relative to the zero measure, a
contradiction.

This refutes only the overbroad frozen Lean encoding, not Hormander's mathematical theorem. No
positive proof body or proof receipt was added, no obligation was closed, and the item remains
`[ ]`. Lifecycle remains `planned`; predecessor records remain `[H2, M4, R3]`. The negative
evidence warrants fail-closed `[H5, M5, R3]`, but this proof worker does not mutate predecessor or
authoritative state. Audit and theorem completion are false. `.stage1-worker-selftest.json` is
deliberately absent because the assigned proof phase is not complete.

## Failed gate and retry

The first failed gate is exact-target consistency. Rev-5.6 section 3.1 makes `H5` a terminal
classification and blocks ordinary theorem-proof execution. Repair requires reopening
`S56-M-1259-STATEMENT`, binding a source-audited reference measure and every source-required
nondegenerate condition, and accepting a new exact-expression fingerprint and obligation-registry
version. The anchor audit, obligation tree, and proof phase must then be rerun against that repaired
target.

The statement receipt is stale: it records SHA-256 `50c18b67...28d5`, while the actual statement
source hashes to `8258728f...c0c7`, and its prose says Lebesgue measure although the Lean root
accepts an arbitrary `Measure`. The source crosswalk does not contain the primary-source
transcription and assumption audit needed to repair this safely. A proof worker may neither guess
the missing mathematics nor broaden, weaken, or substitute the theorem.

The sole declared predecessor, `S56-M-1259-OBLIGATION_TREE`, is also provisional `[_]`, not
master-accepted `[x]`. That independently prevents dependency-legal proof acceptance, although the
kernel refutation is the first semantic failure.

## Frozen obligations

The seven root-relevant obligations remain unchanged:

```text
THM-M-1259-ROOT
THM-M-1259-S-OBJECT-MODEL
THM-M-1259-L-ANALYTIC-CORE
THM-M-1259-L-COMMUTATOR-ESTIMATE
THM-M-1259-L-REGULARITY-BOOTSTRAP
THM-M-1259-T-ROOT-COMPOSITION
THM-M-1259-X-MATHLIB-BOUNDARY
```

`expandedCore_composes_hormanderTarget` is only a checked conditional wrapper from the unproved
`ExpandedHypoellipticCore` premise. The anchor audit found supporting APIs but no pinned terminal
Hormander theorem. After any source-faithful statement repair, the localized commutator estimate
and regularity bootstrap remain real open proof obligations.

## Current-base replay

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink. It was reused read-only. No `lake update`, `lake build`,
dependency clone/fetch, network discovery, or dependency mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 targets; skill present. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required. |
| `python3 scripts/stage1_target.py show THM-M-1259` | 0 | Rank 161; lifecycle `planned`; lane `hard_mathlib_anchor_and_wrapper`; theorem incomplete. |
| `git status --short` | 0 | Before this packet, only `?? Formalizations/Lean/.lake`. |
| `cd Formalizations/Lean && lake env lean --version && lake --version && lake env which lean` | 0 | Lean 4.29.0 commit `98dc76e3...6740`; Lake 5.0.0; pinned executable resolved. |
| Isolated trust-zero replay below | 0 | Statement exit 0; counterexample exit 0; both stderr streams empty. |
| Prohibited-construct scan below | 1 | Expected no-match exit: no prohibited construct in either Lean input. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` and clean-status check | 0 | Commit `8a178386...ea95`; tree `bdc39a31...c2b`; worktree clean. |
| `git diff --quiet c45f3c70..HEAD --` the five frozen proof inputs | 0 | Inputs unchanged since the counterexample was first integrated. |
| `python3 -m json.tool` plus packet invariants and `git diff --check` | 0 | Recorded after packet creation; JSON valid, invariants held, no whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No self-test manifest for a blocked proof phase. |

The exact narrow replay was:

```bash
repo=$(git rev-parse --show-toplevel)
tmp=$(mktemp -d)
lean_path=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)

cd Formalizations/Lean
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  lake env lean --trust=0 -t0 \
    -R "$repo/Stage1_Instances/THM-M-1259" \
    -o "$tmp/Statement.olean" \
    "$repo/Stage1_Instances/THM-M-1259/Statement.lean"

LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  lake env lean --trust=0 -t0 \
    -R "$repo/Stage1_Instances/THM-M-1259" \
    "$repo/Stage1_Instances/THM-M-1259/Counterexample.lean"
```

It ran from `2026-07-15T18:16:47+08:00` through `18:17:20+08:00`. The output hashes were
`a65df923...abac6` for the statement and `aa64bb57...1dd2` for the counterexample; the temporary
`Statement.olean` hash was `af3e3399...130d`. The kernel reported exactly
`[propext, Classical.choice, Quot.sound]` for `not_hormanderTarget`.

The scoped scan was:

```bash
rg -n --pcre2 \
  '\b(?:sorry|admit|axiom)\b|sorryAx|unsafe|implemented_by|native_decide|\bexternal\b' \
  Stage1_Instances/THM-M-1259/Statement.lean \
  Stage1_Instances/THM-M-1259/Counterexample.lean
```

Its exit code was the expected no-match `1`.

## Boundary

This packet adds only this Markdown file and its JSON companion under the assigned owned path. It
does not change Lean source, frozen statements, graphs, scheduler state, generated checklists,
dependency artifacts, or another target. It is narrow negative evidence from the current dirty
nonrelease worker clone, not a proof receipt, validation receipt, release result, or master
acceptance. It does not satisfy `S56-M-1259-PROOF` and makes no theorem-completion claim.
