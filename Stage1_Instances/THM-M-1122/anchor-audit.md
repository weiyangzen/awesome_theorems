# Formal anchor audit

Item: `S56-M-1122-ANCHOR_AUDIT`. Audit date: 2026-07-12.

The audit found one exact pinned interface anchor and no proof anchor for the canonical root. Pinned
mathlib at commit `8a178386ffc0f5fef0b77738bb5449d50efeea95` supplies
`ProbabilityTheory.IdentDistrib` in `Mathlib.Probability.IdentDistrib`; this is exactly the target's
equality-in-distribution conclusion type. `AnchorAudit.lean` elaborates that interface and its basic
law transports under Lean 4.29.0. It does not supply Brownian motion, the radial Loewner equations,
the LERW scaling limit, or Schramm's conditional identification theorem.

## Candidate inventory

| Candidate | Immutable revision | Toolchain / dependency | Exact-root result |
|---|---|---|---|
| pinned mathlib `ProbabilityTheory.IdentDistrib` | `8a178386ffc0f5fef0b77738bb5449d50efeea95` | Lean 4.29.0; repo-pinned | no; conclusion interface only |
| `RemyDegenne/brownian-motion`, `BrownianMotion.Gaussian.BrownianMotion` | `bdf5ea0c34f9e6d75bce5f0609a968d6e9e99e8e` | Lean 4.31.0; mathlib `fabf563a7c95a166b8d7b6efca11c8b4dc9d911f` | no; real Brownian infrastructure only |
| `banr1/tailored-brownian-motion`, `BrownianMotion.Gaussian.BrownianMotion` | `5f7e47403f707ba69d2534c884712eb08ea37134` | Lean 4.28.0-rc1; mathlib `9227fd8e495705d7b4e97f0b0cc5098c655fc458` | no; older real Brownian infrastructure only |

The current Brownian-motion project exposes `IsPreBrownianReal`, `IsBrownianReal`, `brownian`,
`isBrownianReal_brownian`, and `hasLaw_brownian`. That is credible future infrastructure, but its
time parameter and state are real-valued; it contains no circle-valued Brownian driver, radial
Loewner solution, LERW scaling-limit object, Conjecture 1.2 bridge, or Theorem 1.3 proof. It also
targets newer Lean and mathlib commits, so it cannot be imported into this pinned environment
without an audited upgrade or backport. The older tailored branch has the same semantic gap and a
different toolchain. Neither external project was fetched into `.lake`, imported, kernel-credited,
or classified as root closure.

## Negative search and classification

Repository-local and pinned-mathlib searches for Schramm, stochastic/radial Loewner, LERW,
loop-erased random walk, and Brownian motion found no relevant root candidate. The only pinned
mathlib `Loewner` hits are the unrelated partial order on positive operators. GitHub repository
searches restricted to Lean returned zero repositories for `Schramm-Loewner` and `Loewner`; a
Brownian search returned the two projects audited above. GitHub repository search is not a proof of
global nonexistence, so this is a bounded discovery result, not an absolute claim.

The canonical root remains open with `formalization_debt` and machine state
`not_repo_local_closed`. There is no external exact closure to integrate, hence no discovered
`repo_local_integration_debt`. This phase is complete as an anchor inventory only; it claims no H0,
M0, R0, audit completion, proof, or theorem completion.

## Validation evidence

| Command | Result |
|---|---|
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i 'Schramm\|Loewner\|LERW\|loop.erased\|circle Brownian\|radial Loewner\|Brownian motion' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | exit 0 only because of unrelated operator-order `Loewner` hits; no target candidate |
| GitHub repository API searches for exact `Schramm-Loewner` and `Loewner`, language Lean | exit 0; both `total_count: 0` |
| GitHub repository API search for `Brownian`, language Lean | exit 0; two repositories, audited above |
| immutable raw-file/API inspection of both external commits, their `lean-toolchain`, `lake-manifest.json`, tree, and Brownian module | exit 0; revisions, dependency pins, and declarations recorded above |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1122/AnchorAudit.lean)` | exit 0; exact pinned interface probe elaborated |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1122/Statement.lean)` | exit 0; frozen canonical target still elaborates |
| JSON parsing and scoped anchor-audit invariant assertions | exit 0 |
| placeholder-token scan of `AnchorAudit.lean` | exit 0; no forbidden declaration or proof placeholder |
| `git diff --check -- Stage1_Instances/THM-M-1122 .stage1-worker-selftest.json` | exit 0; no output |
