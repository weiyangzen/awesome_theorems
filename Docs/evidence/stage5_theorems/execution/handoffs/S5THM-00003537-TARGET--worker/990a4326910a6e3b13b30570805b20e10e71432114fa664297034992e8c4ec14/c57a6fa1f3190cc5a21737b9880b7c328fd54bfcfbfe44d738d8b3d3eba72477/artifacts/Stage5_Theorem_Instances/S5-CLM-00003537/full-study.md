# Full study: S5-CLM-00003537

## Statement and identity

For every positive lacunary sequence of natural numbers `m`, the real
parameters whose multiplicative orbit `ξ m_n` is not dense modulo one form a
set of Hausdorff dimension one. The frozen record is
`Bugeaud06.pollington_de_mathan`, source revision
`2270d31e8dd611521f979de6d86da364930b7669`, and its current Stage6 alias is
`S6-CLM-00001772` / `S6-VAR-00003257`.

## Mathematical reconstruction

Lacunarity is stronger than unboundedness: consecutive frequencies grow by a
uniform factor. On an interval of candidate parameters, multiplication by a
frequency expands length, while reduction modulo one produces periodically
spaced dangerous intervals corresponding to a fixed target arc. Frequencies
chosen in separated blocks ensure that only uniformly many such dangerous
components intersect a current Schmidt-game interval. The player therefore
retains a child interval avoiding all components in that block. Iterating
across blocks yields a winning set whose entire orbit omits the target arc.

Omitting a nonempty open arc is an explicit certificate of nondensity. Hence
the winning parameter set is contained in the set appearing under `dimH` in
the frozen statement. A Schmidt-winning subset of the real line has full
Hausdorff dimension, while every subset of the real line has Hausdorff
dimension at most one. Monotonicity supplies the lower bound and the ambient
dimension supplies the upper bound, proving equality.

The complete node-by-node account, including exceptional cases and trust
boundaries, lives once in `proof-outline.md`; the structured inventory in
`proof-units.json` references rather than duplicates it.

## Formal and trust boundary

The statement provider is pinned by declaration, type, source, revision, and
body digests. `Statement.lean`, `Proof.lean`, and `Audit.lean` carry the exact
provider-module spelling plus the qualified source name and reject local
semantic capture. `Audit.lean` supplies named endpoints for both transport
directions. The worker records `master_recompute_required=true`: textual
agreement and worker-attested hashes are not canonical semantic acceptance.

The foundation profile admits no bodyless declarations and no transitive
axioms. The machine record therefore reports trust zero, no observed axioms,
and an empty machine cut set. Cold replay and adversarial semantic-substitution
mutations are required again from the integrated byte snapshot.

## Strict dominance over THM-M-0387

The negative fixture has root `H1/M2/R0`, only 29 of 93 machine targets closed,
and `root_machine_closed=false`. This package adds an exact semantic environment
lock, bidirectional transport, exact-root M0-P claim, empty H/M/R cut sets,
cold from-source replay, semantic-substitution mutations, and a total injective
four-node readable map with reverse coverage. The comparison is predicate- and
digest-based, not a comparison of page count.
