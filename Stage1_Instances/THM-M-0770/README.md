# THM-M-0770 rev-5.6 statement

This directory is the `planned` intake for Zorn's lemma: every nonempty partially ordered set in
which every chain has an upper bound has a maximal element. Here, maximal means that no strictly
larger element exists; it does not mean greatest.

The repository supplies only the gloss "existence of a maximal element in a partially ordered set,"
the attribution Max Zorn, the year 1935, and an untrusted "verified" label. Those fields omit the
chain-boundedness hypothesis and do not identify a source statement. This dossier restores the
necessary hypothesis. The statement phase selects the nonempty-carrier/nonempty-chain convention:
`Statement.lean` quantifies over a nonempty partially ordered type, assumes every nonempty chain is
bounded above, and concludes `IsMax`. It also checks that `IsMax` has the expected equality form in
a partial order. It does not silently identify this target with the separately owned Hausdorff
maximal principle or Kuratowski-Zorn target.

The exact Lean target is self-tested against the shape of pinned mathlib declaration
`zorn_le_nonempty`; four structural mutations and the empty/singleton boundaries are checked. The
provisional root vector remains `[H1, M3, R3]`: statement elaboration is not proof or anchor credit,
and the missing primary-source pinpoint still prevents H0. `statement.json` and
`statement-validation.md` record the exact expression and evidence. Audit completion and theorem
completion remain false pending every downstream gate and master acceptance.
