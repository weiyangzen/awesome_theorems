# Machine-checked audit

The root declaration is
`AwesomeTheorems.Stage5.S5_CLM_00003519.rank_2_2`. Its exact proposition is
the frozen provider proposition: an element of
`Arxiv.«2605.12342».gammaSubgroup 2 2` generates the whole subgroup.

The proof is local (`M0-L`). It classifies permutations of `Fin 2` by a
kernel-checked finite decision, constructs the diagonal transposition, unfolds
the provider's exact `gammaSubgroup` and `signDiffHom` definitions to establish
kernel membership, excludes both mixed-sign pairs, and proves every element is
either identity or the generator. `Subgroup.top_unique` then closes the root.

All owned Lean files import
`FormalConjectures.Arxiv.2605.12342.Conjecture1` exactly. The source theorem is
mentioned for semantic binding but not used in the proof term. Trust-zero
elaboration, the forbidden-oracle scan, exact-import check, source-declaration
reference check, and local shadow/parser-substitution scan form the machine
gate. Observed foundation axioms are recorded in `machine-closure.json`; the
provider's `sorryAx` is absent from the local root's observed axiom set.

Cold replay uses the pinned Lean toolchain with `LAKE_NO_CACHE=1`. The release
still requires the canonical Master to repeat semantic recomputation after
integration.
