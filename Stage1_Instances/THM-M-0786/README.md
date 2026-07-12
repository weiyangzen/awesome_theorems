# THM-M-0786 rev-5.6 intake

This directory is the fail-closed `planned` intake for Martin's Borel determinacy theorem. The
repository phrase "Borel games are determined" is provisionally scoped to Gale-Stewart games in
which two players alternately choose natural numbers and the resulting play belongs, or does not
belong, to a Borel payoff set in Baire space.

Donald A. Martin's 1975 paper *Borel Determinacy* is identified as the primary source candidate.
The paper's exact definitions, theorem wording, foundation assumptions, page-level proof crosswalk,
and errata have not been independently inspected and accepted. In particular, this intake does not
silently replace arbitrary Borel payoff sets by open, closed, finite, or otherwise easier games.

The manifest label `已验证` is untrusted metadata and provides no human-proof or machine-proof
credit. The anchor audit classifies the provisional root as `[H1, M3, R3]`: a published complete
human proof is identified but not source-audited, while a highly relevant immutable external Lean
source anchor lacks accepted kernel/trust evidence, a checked statement adapter, and repo-local
integration. The intake-selected
Gale-Stewart target now elaborates in `Statement.lean` and is self-tested pending master acceptance;
this supplies no proof credit. The version-1 obligation registry freezes 14 typed nodes and an
external-theorem adapter route. Its conditional final composition elaborates, but the external
kernel integration and all substantive transports remain open. No accepted proof state, audit
completion, or theorem completion is claimed.
