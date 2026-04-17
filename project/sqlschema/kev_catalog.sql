-- # Class: Vulnerability Description: A single entry in the CISA Known Exploited Vulnerabilities (KEV) catalog, representing one CVE that has been confirmed exploited in the wild and for which clear remediation guidance exists.
--     * Slot: cve_id Description: The CVE identifier assigned to this vulnerability by a CVE Numbering Authority (CNA). Format: CVE-YYYY-NNNNN.
--     * Slot: vendor_project Description: The name of the vendor or project responsible for the affected product.
--     * Slot: product Description: The name of the affected product.
--     * Slot: vulnerability_name Description: A short, descriptive name for the vulnerability.
--     * Slot: date_added Description: The date (YYYY-MM-DD) the vulnerability was added to the KEV catalog.
--     * Slot: short_description Description: A brief description of the vulnerability.
--     * Slot: required_action Description: The remediation action required, e.g. "Apply updates per vendor instructions."
--     * Slot: due_date Description: The date (YYYY-MM-DD) by which federal civilian executive branch (FCEB) agencies must remediate the vulnerability per BOD 22-01.
--     * Slot: known_ransomware_campaign_use Description: Whether the vulnerability is known to have been leveraged as part of a ransomware campaign.
--     * Slot: notes Description: Additional notes or references related to the vulnerability or its remediation.
--     * Slot: KevCatalog_id Description: Autocreated FK slot
-- # Class: KevCatalog Description: The CISA Known Exploited Vulnerabilities (KEV) Catalog — the authoritative source of vulnerabilities confirmed exploited in the wild, maintained by CISA per Binding Operational Directive (BOD) 22-01.
--     * Slot: id
--     * Slot: title Description: The title of the KEV catalog.
--     * Slot: catalog_version Description: The version string of the KEV catalog release.
--     * Slot: date_released Description: The ISO 8601 timestamp at which this catalog version was released.
--     * Slot: count Description: The total number of vulnerabilities in this catalog version.

CREATE TABLE "KevCatalog" (
	id INTEGER NOT NULL,
	title TEXT,
	catalog_version TEXT,
	date_released TEXT,
	count INTEGER,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_KevCatalog_id" ON "KevCatalog" (id);

CREATE TABLE "Vulnerability" (
	cve_id TEXT NOT NULL,
	vendor_project TEXT NOT NULL,
	product TEXT NOT NULL,
	vulnerability_name TEXT NOT NULL,
	date_added TEXT NOT NULL,
	short_description TEXT NOT NULL,
	required_action TEXT NOT NULL,
	due_date TEXT NOT NULL,
	known_ransomware_campaign_use VARCHAR(7),
	notes TEXT,
	"KevCatalog_id" INTEGER,
	PRIMARY KEY (cve_id),
	FOREIGN KEY("KevCatalog_id") REFERENCES "KevCatalog" (id)
);
CREATE INDEX "ix_Vulnerability_cve_id" ON "Vulnerability" (cve_id);
