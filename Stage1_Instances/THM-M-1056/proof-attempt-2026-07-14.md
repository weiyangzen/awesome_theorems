# THM-M-1056 proof-phase recheck

Item: `S56-M-1056-PROOF`

Base revision: `3bb4cb3ae15dff8b48c93242019edec3bf858e48`

Attempt date: 2026-07-14 (Asia/Shanghai)

## Verdict

`blocked`. The first failed gate remains `M1056-T-CORE`: no placeholder-free
inhabitant of `OseledetsCorePackage` exists in the repository or pinned Lake
closure. That package is definitionally the entire universal target, so the
checked `root_of_oseledetsCorePackage` declaration is conditional composition,
not a proof body.

The exact target requires the full finite-dimensional invertible Oseledets
splitting. Its open core includes an exact Kingman bridge, exterior-power
processes, forward and backward measurable Lyapunov flags, transversality,
strongly measurable complementary projections, equivariance, simultaneous
vector growth, and transport from matrix coordinates to an arbitrary
finite-dimensional real normed Borel fiber.

Pinned mathlib at `8a178386ffc0f5fef0b77738bb5449d50efeea95` has no
named Kingman or Oseledets terminal declaration. The immutable external anchor
`marcmorningstar/lean4-ergodic-theory@ed3fa6b8a30594eeb791160563942ba115581aa0`
is absent from the pinned closure, requires Lean 4.30.0-rc2 and a different
mathlib revision, and returns a matrix/Euclidean submodule splitting rather
than the target's polymorphic strongly measurable projection family. It cannot
receive proof credit without substantial checked transports.

`SanityInstance.lean` closes a narrower diagnostic target only. It verifies that
all canonical hypotheses and the requested conclusion are jointly inhabited
for the identity cocycle on the one-point probability space with fiber
`Real`. Thus the universal statement is not vacuous through inconsistent
typeclasses. The count-one identity-projection construction works there because
every vector has growth rate zero; it provides no route for a general cocycle
with distinct Lyapunov rates and is deliberately not presented as root proof.

No proof obligation was closed and no state change is proposed. Because the
assigned phase is not self-tested complete, `.stage1-worker-selftest.json` is
deliberately absent.

## Narrow validation

All commands ran in this worker clone using the pre-existing pinned `.lake`
link read-only. No Lake update/build, dependency clone/fetch, network operation,
or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 unique ordered targets, ranks 1 through 1546, passed. |
| `python3 scripts/stage1_target.py show THM-M-1056` | 0 | Rank 248; lifecycle `planned`; `rework_required: true`; `theorem_complete: false`. |
| `python3 Stage1_Instances/THM-M-1056/check_obligation_tree.py` | 0 | The frozen 19-obligation, 49-edge graph passed; denominator `5246a9d5966e76ff5cb379c8f39f48100fafd3c2ce99bf7c7e10f953f8b57828`; root open M3 and core M4. |
| From `Formalizations/Lean`, copy `Statement.lean`, `ObligationTree.lean`, and `SanityInstance.lean` to a fresh directory under `/tmp`; run `lake env lean --root=<tmp> -o <tmp>/Statement.olean <tmp>/Statement.lean`, then run the other two files with `LEAN_PATH=<tmp>:$(lake env printenv LEAN_PATH)` and `LEAN_NUM_THREADS=1`; remove the directory | 0 | The exact statement, conditional root composition, and identity-cocycle sanity instance elaborated. `#print axioms` reported exactly `[propext, Classical.choice, Quot.sound]` for both checked conclusions. |
| `rg -n '^\\s*(sorry|admit|axiom)(\\s|$)|sorryAx|^\\s*unsafe\\s' Stage1_Instances/THM-M-1056 -g '*.lean'` | 1 | Expected no-match exit: no prohibited Lean declaration token occurs in owned sources. |
| `rg -n -i '(^|[^A-Za-z])(oseledets|multiplicative ergodic|kingman)([^A-Za-z]|$)' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | Expected no-match exit: no named terminal Oseledets or Kingman declaration in pinned mathlib. |
| `python3 -m json.tool Stage1_Instances/THM-M-1056/proof-blocker-2026-07-14.json >/dev/null` | 0 | Structured blocker parsed as valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-1056` | 0 | No scoped whitespace errors. |

The three new files were also checked individually with
`git diff --no-index --check /dev/null <file>`; each returned the expected
new-file difference exit 1 and no whitespace diagnostic.

Toolchain evidence: Lean 4.29.0, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`.

## Reopen condition

Resume after the frozen core branches have placeholder-free bodies, or after an
immutable compatible external proof is available with checked exact coordinate,
projection, provenance, and trust transports. Until then the root stays
`[H1, M3, R3]`, the minimal open root cut is `M1056-T-CORE`, and this proof item
cannot truthfully receive `[_]`, an accepted receipt, or theorem-completion
credit.
