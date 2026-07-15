# THM-M-1056 proof recheck: blocked

Item: `S56-M-1056-PROOF`

Attempt: 2026-07-15 (Asia/Shanghai)

Base revision: `dafb8b51c4561eee5fcf162a8d5ee49555584bdb`

Base tree: `cca569d6bbc491441652aae678232353fb385a74`

## Verdict

The assigned proof phase remains `blocked`. No exact proof body was added, no
frozen obligation was closed, and no state change or receipt is proposed. The
root remains `[H1, M3, R3]`; its minimal open proof cut is `M1056-T-CORE`,
which remains M4. Because this phase is not genuinely self-tested complete,
`.stage1-worker-selftest.json` is deliberately absent and the item remains
`[ ]`.

## First Failed Gate

The first failed gate is `M1056-T-CORE`: neither the repository nor its pinned
dependency closure contains a placeholder-free inhabitant of
`OseledetsCorePackage`. That package is definitionally the complete universal
target, so `root_of_oseledetsCorePackage` checks only conditional identity
composition. `SanityInstance.lean` constructs a valid splitting for the
one-point identity cocycle, but this special case cannot prove the target's
universal quantification over every admissible invertible cocycle.

Repository-local `THM-M-1057` provides checked Kingman bodies, including
`ErgodicTheory.tendsto_kingman_ergodic_means`. This supplies one analytic input,
not the forward and backward Lyapunov flags, transversality, measurable
complementary projections, equivariance, or simultaneous vector-growth field.

## External Port Frontier

The only substantive external candidate remains
`ErgodicTheory.oseledets_splitting` from
`marcmorningstar/lean4-ergodic-theory@ed3fa6b8a30594eeb791160563942ba115581aa0`.
It pins Lean 4.30.0-rc2 and mathlib `34f7a6cd...`, while this target pins Lean
4.29.0 and mathlib `8a178386...`.

Scratch-only compatibility work under `/tmp/m1056-bandprojector-slot38`
advanced the 62-module transitive port through module 33. Fresh trust-zero
compiles of modules 32 and 33 both exited 0 without compatibility edits:

| Index | Module | Source SHA-256 | Olean evidence |
| ---: | --- | --- | --- |
| 32 | `ErgodicTheory.Lyapunov.SpectrumConstancy` | `f96d04d4acda3d91707ed4bd9813270db912326ea402a7f878f5002e425269e4` | 121,496 bytes; SHA-256 `0a2a2b90e9b778f4292568619e7ad993c927e5e23d97425d9dc753499c17ae` |
| 33 | `ErgodicTheory.Lyapunov.StratumLogGrowthBounds` | `126173e14634f57054f97d2d2cc1fb14beba8cb990203d4522155e8a1415e881` | 515,896 bytes; SHA-256 `59a7fd3c8132fa53b2a155ca1b5110faf127bb5a90ef42725d9dc753499c17ae` |

Both logs were empty, with SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
The first missing module is now 34,
`ErgodicTheory.Lyapunov.FiltrationFromSpectralUpper`. Scratch sources, edits,
oleans, and logs remain outside the repository and receive no target proof
credit.

The exact scratch command was run once for each module after setting `SRC` and
`OUT` to its respective `.lean` and `.olean` paths:

```bash
ROOT=$PWD
SCR=/tmp/m1056-bandprojector-slot38
LEANP=$(printf '%s:' "$ROOT/Formalizations/Lean/.lake/build/lib/lean" \
  "$ROOT"/Formalizations/Lean/.lake/packages/*/.lake/build/lib/lean | sed 's/:$//')
LEAN_NUM_THREADS=1 LEAN_PATH="$SCR:$LEANP" timeout 600 \
  /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean \
  --trust=0 -t0 --root="$SCR" -o "$OUT" "$SRC"
```

## Exact Target Gap

Even a complete compatible port would not directly inhabit the frozen target.
The external theorem returns measurable submodules and an internal direct sum
for a Euclidean matrix cocycle. An exact wrapper must still:

- choose coordinates for arbitrary finite-dimensional normed Borel `E` and
  transport strong measurability, inversion, both log-integrability
  hypotheses, cocycle iterates, and equivalent-norm growth;
- construct strongly measurable oblique component projections from the
  generally nonorthogonal internal direct sum;
- prove idempotence, pairwise annihilation, sum-to-identity, nonzero,
  equivariance, positive count, fixed-space identification, and the target's
  common-conull-set growth field;
- align `Real.posLog`, normalization, and cocycle conventions.

Importing only the Euclidean matrix/submodule theorem would substitute a
narrower theorem and cannot close `M1056-T-CORE`.

## Fresh Validation

All repository commands ran in this worker clone. The automation-provided
untracked `Formalizations/Lean/.lake` symlink was reused read-only. No
`lake update`, `lake build`, dependency clone/fetch, network action, or `.lake`
mutation was performed.

| Command | Exit | Exact result |
| --- | ---: | --- |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique ordered targets at ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-1056` | 0 | Rank 248; lifecycle `planned`; rework required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1056/check_obligation_tree.py` | 0 | Passed 19 obligations and 49 typed edges; denominator `5246a9d5966e76ff5cb379c8f39f48100fafd3c2ce99bf7c7e10f953f8b57828`; root M3 and core M4 remain open. |
| `python3 Stage1_Instances/THM-M-1056/check_statement.py` | 1 | Shared-cache infrastructure failure before validation completed: the canonical `flt-regular` package had no valid `HEAD` (`git` exit 128). No fetch, repair, or cache mutation was attempted; the direct replay below is the narrow statement evidence. |
| Direct pinned `lean --version` and `lake --version` | 0 | Lean 4.29.0 commit `98dc76e3...`; Lake `5.0.0-src+98dc76e`. |
| Fresh direct Lean 4.29.0 `--trust=0 -t0` replay of `Statement.lean`, `ObligationTree.lean`, and `SanityInstance.lean` with fresh `/tmp` oleans | 0 | All three modules elaborated; conditional composition and the sanity result reported exactly `[propext, Classical.choice, Quot.sound]`; olean SHA-256 values were `c55d17a...f64db`, `a75c5008...57f0e`, and `ff4de13c...178b7`. |
| `rg -n '^\\s*(sorry|admit|axiom)(\\s|$)|sorryAx|^\\s*unsafe\\s|implemented_by|^\\s*extern\\s' Stage1_Instances/THM-M-1056 -g '*.lean'` | 1 | Expected no-match exit; no prohibited Lean declaration token occurs. |
| Search repository targets and pinned mathlib for an Oseledets terminal body | 0 | Found target/interface definitions only; no local or pinned-mathlib terminal proof. |
| Search `THM-M-1057` for its Kingman terminal declarations | 0 | Found the three repository-local Kingman theorems and its package/root bodies. |
| Direct pinned Lean 4.29.0 with `LEAN_NUM_THREADS=1`, existing build-library `LEAN_PATH`, `timeout 600`, `--trust=0 -t0`, scratch root, and scratch output for external modules 32 and 33 | 0, 0 | Both modules elaborated; the hashes and sizes are recorded above; the port reached 33 of 62. |
| Pinned mathlib revision/tree and worktree check | 0 | Revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`, clean package worktree. |
| `python3 -m json.tool` plus focused blocker-invariant assertions | 0 | The structured artifact parses and truthfully records blocked state, base, frontier, changed paths, and completion flags. |
| `git diff --check -- Stage1_Instances/THM-M-1056`; `git diff --no-index --check /dev/null` for each new artifact | 0; 1, 1 | No whitespace diagnostic occurred; exit 1 is the expected new-file difference result for each untracked artifact. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The completion self-test manifest is absent because the assigned proof phase is incomplete. |

The owned source hashes remain `00c1ca02...f3886` for `Statement.lean`,
`4286d312...47c` for `ObligationTree.lean`, and `f83dcbb4...802` for
`SanityInstance.lean`. The canonical expression SHA-256 remains
`8e1a96a304ce3dd43838f934406d58ac3594b9d34c6e1617461abc17e65d403b`.

## Retry Condition

Resume at external module 34 or provide equivalent placeholder-free local
bodies, then implement and kernel-check the arbitrary-`E` coordinate,
integrability, measurable-oblique-projection, equivariance, count, growth,
exact-type, provenance, and trust transports.

## Status Boundary

This is current-base, nonrelease blocker evidence only. Lifecycle remains
`planned -> planned`; accepted receipt IDs are empty; audit completion and
theorem completion are false. It does not satisfy the proof item or authorize
validation, release, checklist edits, or master acceptance.
