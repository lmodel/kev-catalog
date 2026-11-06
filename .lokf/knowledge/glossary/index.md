# Glossary

* [Known Exploited Vulnerabilities (KEV)](kev.md) - The Known Exploited Vulnerabilities (KEV) catalog: the list of CVEs that the Cybersecurity and Infrastructure Security Agency (CISA) publishes as a JSON and a CSV file, each entry naming the action it asks for and a due date.
* [Adapt copy](adapt-copy.md) - An adapt copy: the copy of a published LinkML schema that `lokf adapt` writes so that it can sit beside LOKF's `lokf.yaml` in a domain schema, with its classes re-rooted on `Concept` and every name LOKF also defines renamed with its IRI kept. Here it is `.lokf/schema/kev-catalog.yaml`.
* [Forensic triage (forensicTriage)](forensic-triage.md) - The KEV key `forensicTriage`: `Yes` when BOD 26-04 calls for forensic triage of a vulnerability and `No` when it does not. CISA types it as a string and names the two values in its description, and the schema makes them an enum.
