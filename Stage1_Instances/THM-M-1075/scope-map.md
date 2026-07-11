# Scope map

## Preserved source scope

- Repository identity: `THM-M-1075`, titled "renewal process" (`更新过程`).
- Repository content: only "renewal theory" (`更新理论`).
- Broad subject: stochastic processes built from successive waiting times and their renewal epochs.
- Attribution and date: "many mathematicians", twentieth century. These are discovery metadata,
  not a theorem-bearing citation.

This subject description does not itself assert a truth-valued claim.

## Decisions required before statement freeze

An authoritative source must first select one proposition. Only then may the statement phase freeze:

- ordinary versus delayed, terminating, arithmetic, or continuous-time renewal processes;
- probability space, independence and identical-distribution assumptions, positivity or
  nonnegativity of interarrival times, and finiteness/nonarithmetic/moment hypotheses;
- renewal epochs `S_n`, counting convention for `N(t)`, and the renewal measure/function;
- whether the conclusion is a construction, measurability result, renewal equation, expectation
  identity, almost-sure limit, expectation asymptotic, or distributional assertion;
- ordered binders, endpoint conventions at time zero, zero interarrivals, defective laws, infinite
  means, and the exact Lean probability APIs and universes.

## Explicit exclusions

- Treating the definition `N(t) = sup {n | S_n <= t}` as a proved theorem.
- Choosing the elementary renewal theorem merely because it is a standard result.
- Choosing a renewal-equation existence or uniqueness result without source support.
- Importing Smith's key renewal theorem (`THM-M-1076`) or Blackwell's renewal theorem
  (`THM-M-1077`) into this target.
- Assuming the desired asymptotic or renewal property as an abstract hypothesis and then projecting
  it from a structure.
- Using the metadata label `已验证` as source or kernel evidence.

The statement gate must remain blocked until a primary source resolves these choices without
broadening or substituting the catalog entry.
