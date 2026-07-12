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
canonical repo-local declaration, mutation tests, and all downstream assurance gates remain open.
The manifest's `source_status_untrusted` value `已验证` supplies no proof or completion credit.

