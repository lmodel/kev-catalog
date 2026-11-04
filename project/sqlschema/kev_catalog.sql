-- # Class: KevCatalog Description: One published release of the KEV catalog, with the entries it lists.
--     * Slot: id
--     * Slot: title Description: The catalog's human-readable name.
--     * Slot: catalogVersion Description: The version label of this release of the catalog.
--     * Slot: dateReleased Description: The date and time this release of the catalog came out.
--     * Slot: count Description: How many entries CISA says the catalog holds.
-- # Class: KevVulnerability Description: One entry of the KEV catalog, naming a CVE that CISA lists as exploited and the action it asks for by a due date.
--     * Slot: cveID Description: The CVE identifier of the listed vulnerability, which identifies the entry.
--     * Slot: vendorProject Description: The vendor or project behind the affected product, as CISA names it.
--     * Slot: product Description: The affected product, as CISA names it.
--     * Slot: vulnerabilityName Description: The name CISA gives the vulnerability.
--     * Slot: dateAdded Description: The day CISA added the vulnerability to the catalog.
--     * Slot: shortDescription Description: A brief account of the vulnerability, in CISA's words.
--     * Slot: requiredAction Description: What CISA says must be done about the vulnerability.
--     * Slot: dueDate Description: The day by which CISA wants the required action done.
--     * Slot: knownRansomwareCampaignUse Description: Whether CISA knows of the vulnerability's use in a ransomware campaign.
--     * Slot: forensicTriage Description: Whether the vulnerability calls for forensic triage under BOD 26-04.
--     * Slot: notes Description: Anything else CISA adds about the entry, as free text.
--     * Slot: KevCatalog_id Description: Autocreated FK slot
-- # Class: KevVulnerability_cwes
--     * Slot: KevVulnerability_cveID Description: Autocreated FK slot
--     * Slot: cwes Description: The CWE codes CISA associates with the vulnerability.

CREATE TABLE "KevCatalog" (
	id INTEGER NOT NULL,
	title TEXT,
	"catalogVersion" TEXT NOT NULL,
	"dateReleased" DATETIME NOT NULL,
	count INTEGER NOT NULL,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_KevCatalog_id" ON "KevCatalog" (id);

CREATE TABLE "KevVulnerability" (
	"cveID" TEXT NOT NULL,
	"vendorProject" TEXT NOT NULL,
	product TEXT NOT NULL,
	"vulnerabilityName" TEXT NOT NULL,
	"dateAdded" DATE NOT NULL,
	"shortDescription" TEXT NOT NULL,
	"requiredAction" TEXT NOT NULL,
	"dueDate" DATE NOT NULL,
	"knownRansomwareCampaignUse" VARCHAR(7),
	"forensicTriage" VARCHAR(3),
	notes TEXT,
	"KevCatalog_id" INTEGER,
	PRIMARY KEY ("cveID"),
	FOREIGN KEY("KevCatalog_id") REFERENCES "KevCatalog" (id)
);
CREATE INDEX "ix_KevVulnerability_cveID" ON "KevVulnerability" ("cveID");

CREATE TABLE "KevVulnerability_cwes" (
	"KevVulnerability_cveID" TEXT,
	cwes TEXT,
	PRIMARY KEY ("KevVulnerability_cveID", cwes),
	FOREIGN KEY("KevVulnerability_cveID") REFERENCES "KevVulnerability" ("cveID")
);
CREATE INDEX "ix_KevVulnerability_cwes_KevVulnerability_cveID" ON "KevVulnerability_cwes" ("KevVulnerability_cveID");
CREATE INDEX "ix_KevVulnerability_cwes_cwes" ON "KevVulnerability_cwes" (cwes);
