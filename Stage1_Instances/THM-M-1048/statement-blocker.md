# Statement-phase blocker

Item: `S56-M-1048-STATEMENT`  
Theorem: `THM-M-1048`  
Base revision: `6f569ca05f8d51664a074ab74399896295f38dee`

## Verdict

The exact Lean 4 target cannot be frozen truthfully. The repository source contains only the title
"Martingale problem," the gloss "martingale characterization of Markov processes," a 1969
Stroock/Varadhan attribution, and the untrusted label `verified`. It does not identify a
bibliographic work, theorem, page, or exact wording. The intake consequently leaves open choices
that change the proposition: state and path spaces, path regularity, filtration, operator and test
domain, initial law, solution and uniqueness notions, exceptional-set semantics, and whether the
conclusion is Markov, strong Markov, existence, uniqueness, or an equivalence. The adjacent
`THM-M-1049` separately owns the diffusion-specific Stroock-Varadhan martingale problem, so choosing
that familiar variant here would also conflate two targets.

Dynkin's generator formula, the implication from well-posed martingale problems to a Markov family,
and a converse characterization of a given Markov process are related but materially different
theorems. None is selected by the available metadata. Selecting one would invent missing
mathematics, contrary to the exact-statement gate. Therefore there is no canonical expression to
hash and no sound removed-hypothesis, changed-domain, binder-scope, or boundary mutation suite.
Machine debt remains `M4`.

## Pinned Lean boundary

The pinned environment is Lean `v4.29.0` with mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. A scoped source search found no declaration mentioning
a martingale problem or a martingale/Markov characterization in pinned mathlib.

The historical module `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_241.lean` elaborates, but it
explicitly describes itself as a conservative statement boundary rather than a terminal theorem.
It cannot substitute for a source-derived target:

- its generator compensator is arbitrary supplied data, not the asserted time integral of an
  operator applied to the process;
- its hypotheses already assume that every supplied transition object is a Markov kernel, while
  the conclusion repeats that property;
- its well-posedness predicate encodes only finite-dimensional-law uniqueness for packages with one
  fixed initial law and does not freeze the existence or all-initial-state family used by standard
  Markov conclusions; and
- its conclusion bundles regular conditional laws, conditional expectations,
  Chapman-Kolmogorov, marginal laws, and kernel Markovness although the metadata selects none of
  these precise conclusions or their conjunction.

Thus successful elaboration of that legacy abstraction establishes only that its local definitions
typecheck. It supplies neither exact-statement identity nor proof credit for `THM-M-1048`.

## Validation record

Commands ran in this worker clone on 2026-07-12. Lean used the existing pinned Lake artifacts; no
dependency update, build, clone, fetch, or other `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1048` | 0 | rank 241; planned; L0/rework-required; theorem incomplete |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_241.lean` | 0 | historical abstract boundary elaborated and printed 147 declaration/type lines; this is not exact-target evidence |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i 'martingale problem\|well.?posed.*martingale\|martingale.*markov\|markov.*martingale' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no matching occurrence in pinned mathlib source |

## Retry condition

Retry after an accountable source reviewer provides an immutable authoritative source, exact
theorem/page and definitions, a crosswalk of every ordered binder and hypothesis, and a decision
that distinguishes this general target from `THM-M-1049`. The statement phase can then encode the
exact claim with concrete objects, minimize imports, serialize the elaborated expression and
environment, and run all four mutation classes.

This artifact does not complete the statement node, accept a receipt, or claim theorem completion.
No `.stage1-worker-selftest.json` is emitted because the assigned deliverable is blocked and is not
genuinely self-tested.
