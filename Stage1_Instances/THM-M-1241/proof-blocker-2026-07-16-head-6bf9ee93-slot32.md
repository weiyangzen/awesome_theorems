# THM-M-1241 proof-phase blocker at current base

Item: `S56-M-1241-PROOF`

Intent: `prove`

Recorded: `2026-07-16T04:50:40+08:00` (`Asia/Shanghai`)

Base revision: `6bf9ee93a322e7d25cf9249226222095f95d1cff`

Base tree: `24acf86e69ab2e6fca9480c6269b6429874ba295`

## Verdict

`blocked`. The required positive proof body cannot be implemented for the exact frozen target in a
consistent Lean environment. The tracked, placeholder-free declarations

```text
Stage1Instances.THM_M_1241.not_gagliardoNirenbergTarget :
  not Stage1Instances.THM_M_1241.GagliardoNirenbergTarget

Stage1Instances.THM_M_1241.not_infiniteEndpointPackage :
  not Stage1Instances.THM_M_1241.InfiniteEndpointPackage
```

kernel-refute both the canonical proposition and registered terminal obligation
`M1241-T-ENDPOINT`. Their source files and every frozen input still have the same bytes as the latest
accepted repository inventory. A positive inhabitant would contradict these checked negations, so
adding one without `sorry`, an axiom, an unsafe device, or inconsistency is impossible.

The counterexample uses

```text
n = 1, m = 1, j = 0, q = infinity, r = 1, p = infinity, a = 1,
u = the constant function 1.
```

All encoded parameter hypotheses hold. The critical restriction is vacuous because it assumes
`1 < r`; the zero-order exception is vacuous because its antecedent includes `1 < 1`. The constant
function has zeroth `L^infinity` seminorm `1` and first `L^1` derivative seminorm `0`. The asserted
bound therefore reduces to `1 <= C * 0 ^ 1 * 1 ^ 0 = 0` for every `C`.

This refutes only the frozen formal encoding. It does not refute a suitably corrected classical
Gagliardo-Nirenberg theorem. Correcting an endpoint or function-space hypothesis inside this proof
assignment would broaden or substitute the frozen target and invalidate the statement fingerprint,
obligation registry, typed graphs, and dependent evidence.

## Dependency context

The complete v2 context is genuinely empty: there are no direct hard parents, transitive hard
ancestors, hard edges, reuse hints, or shared groups. The required audited empty ledger is
`dependency-reuse-ledger.json`, schema `stage1-dependency-reuse-ledger/1.1`. It binds graph digest
`73e99d2276c8ba9fec8f89ed41b712308d7f5667e95ba8185e49f1f5bfd40eca`, context digest
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`, and this worker base.
No declaration or checkbox credit is reused.

## Narrow validation

All commands ran in this worker clone. The automation-provided `Formalizations/Lean/.lake` symlink
was reused read-only. No Lake update/build, dependency clone/fetch, network request, or `.lake`
mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1241` | 0 | Rank 422; lifecycle `planned`; theorem incomplete. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 1 | Expected worker-scope fail-closed result: the checked-in theorem DAG differs from a fresh deterministic generation because this new target-owned blocker JSON changes its generated evidence inventory; this proof worker is forbidden to edit the generated DAG. |
| `python3 Docs/tools/check_stage1_standard.py` | 1 | Fails only through the same v2 DAG freshness gate. |
| `python3 Stage1_Instances/THM-M-1241/check_obligation_tree.py` | 0 | 15 obligations and 31 typed edges passed; denominator `d2173828bd656ec7e4545903a4fdd42a5c759de71b31e46f8c4c189be864991e`; root remains M3 and both registered packages remain open in the stale pre-refutation projection. |
| schema 1.1 ledger validation through `scripts/stage1_execution_cron.py:validate_dependency_reuse_ledger` | 0 | Exact empty closure, graph digest, context digest, theorem ID, and base revision passed. |
| `python3 -m json.tool Stage1_Instances/THM-M-1241/dependency-reuse-ledger.json` | 0 | The audited dependency ledger is valid JSON. |
| isolated `lake env lean --trust=0 -t0` replay of `Statement.lean`, `ObligationTree.lean`, `Proof.lean`, `Counterexample.lean`, and `EndpointCounterexample.lean` with fresh temporary oleans | 0 | All five modules elaborated; fresh objects were 76664, 47368, 71384, 136784, and 147592 bytes. The composition theorem, partial lemmas, and both refutations depend only on `propext`, `Classical.choice`, and `Quot.sound`; all declarations with `#print sorries` are sorry-free. |
| `rg -n --pcre2 '(?x)(^|\s)(sorry\|admit\|axiom\|unsafe\|extern\|implemented_by\|native_decide)(\s|$)\|sorryAx' Stage1_Instances/THM-M-1241 --glob '*.lean'` | 1 | Expected no-match result: no prohibited proof device occurs in owned Lean sources. |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | No output; pinned mathlib remained unmodified. |

The current source identities are:

| Input | SHA-256 |
|---|---|
| `Docs/Stage1_Theorem_DAG_v2.json` | `73e99d2276c8ba9fec8f89ed41b712308d7f5667e95ba8185e49f1f5bfd40eca` |
| `Statement.lean` | `96f22aff1d5682cc341b84e4951c2ca36f01026cc0ba1748303ffc484765e7ac` |
| `ObligationTree.lean` | `e29b6cfc715f74cbb8bb2b7eefc6836c881e3ed80f02010e63c535b4baf894d2` |
| `Proof.lean` | `b4703ca1b688f9160edfabdff02e4c759f0bb3ec48fe2092811b56d048c03653` |
| `Counterexample.lean` | `419ba289bd4fbf4e748948ceccc81ff7ee480ef33c33f0d10b6c94dc8b480719` |
| `EndpointCounterexample.lean` | `3d1dfb7122ee65ac9caa7916b314b49565a791225e16afa6fd11cfb6d10249d8` |
| `obligation-registry.json` | `17c9c44de2327ede92ca86130049fb3e7ed363d6d10e1478393ca6238f7257ca` |
| `typed-graphs.json` | `12acdd8807000281295865ebf582c219a7fb3277c632de7152d1ed4ebe71d47d` |
| `dependency-reuse-ledger.json` | `1318548f9b37f1b2e7d48451423d73b944b6cbf8581436006bad818383effd35` |

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake `5.0.0-src+98dc76e`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

The successful isolated replay derived `LEAN_PATH` from `Formalizations/Lean` with `lake env
printenv LEAN_PATH`, wrote every object below a fresh `/tmp` directory, used the pinned executable
through `lake env lean`, and removed the directory afterward. `Statement.lean` used only the derived
base path; each later module used the temporary directory before that base path. Every invocation
set `ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0`, `LEAN_NUM_THREADS=1`, `--trust=0`, `-t0`, and a
300-second timeout.

## Failure boundary

The first failed gate is `M1241-T-ENDPOINT`: its exact formal target
`InfiniteEndpointPackage` is uninhabitable. The frozen root cut remains `M1241-T-FINITE` plus
`M1241-T-ENDPOINT`; the latter is positively refuted, not merely unimplemented. `Proof.lean` closes
no registry-v1 obligation.

Retry requires reopening source fidelity and statement review, identifying the missing endpoint or
function-space condition, correcting and re-elaborating the canonical target, and regenerating the
obligation registry, typed graphs, fingerprints, and dependent evidence before another proof run.

This is a current-base blocker handoff, not a proof receipt. It does not satisfy
`S56-M-1241-PROOF`, change its `[ ]` state, claim audit or theorem completion, or propose validation,
release, receipt acceptance, or master acceptance. Because the positive proof phase is not complete,
`.stage1-worker-selftest.json` is deliberately absent.
