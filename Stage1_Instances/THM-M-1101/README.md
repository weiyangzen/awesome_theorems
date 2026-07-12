# THM-M-1101 rev-5.6 intake

This directory is the fail-closed `planned` intake for the repository label
"Metropolis-Hastings algorithm". The only mathematical gloss in the repository is "the basic
algorithm of MCMC". That describes a method, not one proposition: it does not say whether the root
claim is detailed balance, invariance of the target law, irreducibility, convergence, or an
estimator theorem.

The intake identifies Hastings's 1970 article and the earlier Metropolis et al. article as primary
source candidates, but it does not select or paraphrase a numbered result that has not been
inspected. The provisional claim family is construction of an accept/reject Markov transition from
a proposal and target, with a source-specified correctness conclusion. The proposal/target
domains, density conventions, zero-support cases, and correctness conclusion remain open.

The provisional root vector is `[H1, M4, R4]`. The historical `已验证` label and the presence of
general reversible-kernel infrastructure in pinned mathlib receive no proof credit. There is no
canonical Lean expression, accepted proof state, audit completion, or theorem completion.

