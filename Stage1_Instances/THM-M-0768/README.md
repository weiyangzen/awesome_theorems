# THM-M-0768 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Cantor-Bernstein-Schroeder
theorem. The repository claim is: if there are injections between two sets in both directions,
then the sets are equipotent.

The scope map freezes the ordinary set/type reading, including empty and universe-polymorphic
carriers. The source crosswalk separates that repository claim from the stronger relational
variant and the embedding API exposed by pinned mathlib. `IntakeProbe.lean` checks that the pinned
library contains the expected theorem and that its type matches the intended ingredients; it is
discovery evidence, not the canonical statement artifact or proof credit.

This intake remains at `[H3, M3, R4]`. A primary-source edition/page, independent source review,
master acceptance, and all downstream assurance gates remain open. The manifest's
`source_status_untrusted` value `已验证` supplies no proof or completion credit.

## Statement phase handoff

The dependent statement phase proposes
`Stage1Instances.THM_M_0768.CantorBernsteinSchroederTarget` in `Statement.lean` as the exact
canonical target. It elaborates with one direct import, has a checked iff to the bundled
embedding/equivalence encoding, and distinguishes mutations of a hypothesis, carrier domains,
binder scope, and the empty-carrier boundary. `statement.json` freezes the expression and
environment hashes; exact commands and results are in `statement-validation.md`.

This proposal is statement-only and pending master acceptance. It does not invoke or credit the
pinned mathlib proof, and it does not advance any downstream node or theorem completion.
