# Machine-checked audit

Root declaration: `S5_CLM_00003485.arxiv_id0911_2077_conjecture6_3`.

The root was elaborated from the claim-owned `Proof.lean` using the repository-pinned Lean toolchain and `lake env lean --trust=0`. Lean reports exactly `propext`, `Classical.choice`, and `Quot.sound`. There is no `sorryAx`, claim-specific axiom, unsafe declaration, opaque declaration, or unreviewed bodyless oracle.

The 165 theorem/lemma declarations in `Proof.lean` cover combinatorial identities, the finite PMF-to-integral bridge, Gaussian calculus, Wallis/central-binomial estimates, derivative-shape analysis, endpoint closure, the unimodal-gap composition, and the final frozen theorem. `Statement.lean` and `Audit.lean` independently elaborate at trust zero. The declaration-policy scan confirms that all three files contain only theorem/lemma semantic declarations.

The source theorem is pinned as semantic authority but is not in the target dependency graph because its provider body contains `sorryAx`. Master acceptance remains contingent on independent source/target elaborated-root recomputation and cold replay.
