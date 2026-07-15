# THM-M-0669 proof-phase validation

Item: `S56-M-0669-PROOF`

Intent: `prove`

Base revision: `a23d86cd84f03c26102b43c6b1b3b6d0a7a31e61`

Base tree: `9268aa9f5379837642b6f748f01255e8744c4e78`

Date: `2026-07-15` (`Asia/Shanghai`)

## Implemented bodies

`Proof.lean` adds unconditional, placeholder-free syntax bodies. Pure-ring
atoms have no relation-symbol case; their equality terms are interpreted as
universal integer polynomials in `FreeCommRing`, with a checked evaluation
theorem in every compatible commutative ring. Quantifier-free formulas are
closed under negation, implication, conjunction, and disjunction. The latter
body provisionally closes `M0669-C-BOOLEAN`; the atomic bodies are recorded
only as partial progress toward `M0669-C-ATOMIC` because the frozen
source-theory/definable-order presentation bridge remains open.

The module also freezes the exact remaining semantic interface as
`OneVariableEliminationPackage` and proves structural formula elimination and
the unchanged canonical root from that explicit premise. These conditional
bodies make the composition boundary kernel-visible, but they do not construct
the premise and receive no one-variable or root proof credit.

The exact root remains `[H1, M3, R3]`. No pinned or audited external candidate
contains the required real-closed-field sign, root-cell, projection, and
semantics proof.

## Commands and results

All successful evidence commands ran in this worker clone. The final Lean
recipe invokes the already installed pinned Lean binary directly and constructs
`LEAN_PATH` from existing build artifacts; it runs no Lake or network command.
During development, before that recipe was installed, an aborted `lake env`
environment-resolution attempt unexpectedly started an incomplete
`flt-regular` fetch through the automation-provided shared `.lake` symlink. It
was terminated, never produced a checked-out revision, and was not present on
the final proof `LEAN_PATH`. This attempt therefore makes no whole-run
read-only `.lake` or release-evidence claim.

Later, a separate standard-check process running elsewhere attempted the same
shared dependency resolution and left that `flt-regular` directory without a
Git `HEAD`. The proof recipe does not reference it, but only the canonical-cache
owner can repair this shared state. It remains an explicit blocker to any
clean-cache or release claim from this worker evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `bash Stage1_Instances/THM-M-0669/check_proof.sh` | 0 | Disposable `Statement.olean` and `Proof.lean` elaborated with `--trust=0 -t0`; all seven declarations passed `assert_no_sorry`; axiom closures were subsets of `propext`, `Classical.choice`, and `Quot.sound`; the structured checker passed. The script resolves the already installed pinned Lean binary and composes `LEAN_PATH` from existing package build artifacts directly, so Lake performs no dependency resolution or fetch. |
| `python3 Stage1_Instances/THM-M-0669/check_obligation_tree.py` | 0 | Frozen 14-obligation registry and typed graphs passed; authoritative root remains open at M3. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Rev-5.6 standard, 15 assurance groups, and all 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0669` | 0 | Rank 713; planned hard-statement-first lane; theorem incomplete. |
| `rg -n --pcre2 '(?i)\b(sorry|admit|sorryAx)\b|^[[:space:]]*(axiom|constant|opaque|unsafe|extern)\b|\b(implemented_by|native_decide|run_tac)\b' Stage1_Instances/THM-M-0669/Proof.lean` | 1, expected | Empty output; no prohibited executable proof device. |
| `python3 -m json.tool` on `proof-receipt.json`, `proof-blocker.json`, and `.stage1-worker-selftest.json` | 0 | All three structured artifacts parsed. |
| `git diff --check -- Stage1_Instances/THM-M-0669 .stage1-worker-selftest.json` plus no-index checks for new files | 0 | No whitespace diagnostics. |

The isolated Lean recipe copies only `Statement.lean` and `Proof.lean` into a
disposable directory, checks the installed Lean version and commit, composes
`LEAN_PATH` directly from the existing project and pinned package build
directories, compiles the local statement module, and elaborates the proof
with trust level zero. The temporary directory is removed on exit.

Lean is `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib is pinned at
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

## Remaining blocker

The first failed general gate is `M0669-E-ONE-VAR`. Closing it requires the
frozen `M0669-E-SIGN`, `M0669-E-ROOTS`, `M0669-E-PROJECT`, and
`M0669-E-SEMANTICS` bodies or an exact immutable compatible Lean 4 proof.
Until then, the conditional formula recursion cannot close the root.

This is self-tested partial proof execution proposed as `[_]`, not accepted
state. Accepted closure remains empty. It does not satisfy the full proof node,
close the canonical target, establish M0, or claim validation, release,
`AUDIT-Z`, `THEOREM-Z`, or theorem completion.
