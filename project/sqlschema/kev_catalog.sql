-- # Class: KevEntry Description: A single entry in the CISA Known Exploited Vulnerabilities (KEV) catalog, representing one CVE that has been confirmed exploited in the wild and for which clear remediation guidance exists.
--     * Slot: vendor_project Description: The name of the vendor or project responsible for the affected product.
--     * Slot: product Description: The name of the affected product.
--     * Slot: vulnerability_name Description: A short, descriptive name for the vulnerability.
--     * Slot: date_added Description: The date (YYYY-MM-DD) the vulnerability was added to the KEV catalog.
--     * Slot: short_description Description: A brief description of the vulnerability.
--     * Slot: required_action Description: The remediation action required, e.g. "Apply updates per vendor instructions."
--     * Slot: due_date Description: The date (YYYY-MM-DD) by which federal civilian executive branch (FCEB) agencies must remediate the vulnerability per BOD 22-01.
--     * Slot: known_ransomware_campaign_use Description: Whether the vulnerability is known to have been leveraged as part of a ransomware campaign.
--     * Slot: notes Description: Additional notes or references related to the vulnerability or its remediation.
--     * Slot: cve_id Description: The CVE identifier assigned by a CVE Numbering Authority (CNA). Format: CVE-YYYY-NNNNN.
--     * Slot: title Description: Short human-readable title or name for this entity.
--     * Slot: description Description: Narrative description of the vulnerability.
--     * Slot: published_date Description: Date and time the vulnerability was first published.
--     * Slot: last_modified_date Description: Date and time the vulnerability record was last modified.
--     * Slot: status Description: Current lifecycle state of the vulnerability record.
--     * Slot: KevCatalog_id Description: Autocreated FK slot
--     * Slot: impact_id Description: Impact and severity assessment for this vulnerability.
-- # Class: KevCatalog Description: The CISA Known Exploited Vulnerabilities (KEV) Catalog — the authoritative source of vulnerabilities confirmed exploited in the wild, maintained by CISA per Binding Operational Directive (BOD) 22-01.
--     * Slot: id
--     * Slot: title Description: The title of the KEV catalog.
--     * Slot: catalog_version Description: The version string of the KEV catalog release.
--     * Slot: date_released Description: The ISO 8601 timestamp at which this catalog version was released.
--     * Slot: count Description: The total number of vulnerabilities in this catalog version.
-- # Abstract Class: Vulnerability Description: Abstract base representation of a security vulnerability. Extended by source-specific schemas (KEV, CVE, NVD).
--     * Slot: cve_id Description: The CVE identifier assigned by a CVE Numbering Authority (CNA). Format: CVE-YYYY-NNNNN.
--     * Slot: title Description: Short human-readable title or name for this entity.
--     * Slot: description Description: Narrative description of the vulnerability.
--     * Slot: published_date Description: Date and time the vulnerability was first published.
--     * Slot: last_modified_date Description: Date and time the vulnerability record was last modified.
--     * Slot: status Description: Current lifecycle state of the vulnerability record.
--     * Slot: impact_id Description: Impact and severity assessment for this vulnerability.
-- # Class: Product Description: Software or hardware entity affected by the vulnerability.
--     * Slot: id
--     * Slot: vendor Description: Name of the vendor or organization responsible for the product.
--     * Slot: name Description: Name of the entity (product, weakness, reference, etc.).
--     * Slot: version Description: Version string of the affected product.
--     * Slot: KevEntry_cve_id Description: Autocreated FK slot
--     * Slot: Vulnerability_cve_id Description: Autocreated FK slot
-- # Class: Reference Description: External reference such as an advisory or article.
--     * Slot: id
--     * Slot: url Description: URL pointing to the reference resource.
--     * Slot: name Description: Name of the entity (product, weakness, reference, etc.).
--     * Slot: source Description: Source or origin of the reference or data.
--     * Slot: KevEntry_cve_id Description: Autocreated FK slot
--     * Slot: Vulnerability_cve_id Description: Autocreated FK slot
-- # Class: Weakness Description: Weakness classification from CWE or a similar taxonomy.
--     * Slot: id
--     * Slot: cwe_id Description: CWE identifier for the weakness classification (e.g. CWE-79).
--     * Slot: name Description: Name of the entity (product, weakness, reference, etc.).
--     * Slot: description Description: Narrative description of the vulnerability.
--     * Slot: KevEntry_cve_id Description: Autocreated FK slot
--     * Slot: Vulnerability_cve_id Description: Autocreated FK slot
-- # Class: Impact Description: Assessment of the vulnerability's impact and severity.
--     * Slot: id
--     * Slot: severity Description: Qualitative severity rating.
--     * Slot: vector Description: CVSS vector string or equivalent scoring vector expression.
--     * Slot: score Description: Numeric vulnerability score (e.g. CVSS base score).
-- # Class: Configuration Description: Logical grouping of CPE match expressions.
--     * Slot: id
--     * Slot: cpe_uri Description: CPE 2.2 URI identifying an affected product configuration.
--     * Slot: operator Description: Logical operator (AND/OR) used in configuration node groupings.
-- # Class: Product_platforms
--     * Slot: Product_id Description: Autocreated FK slot
--     * Slot: platforms Description: Platforms or operating environments affected.

CREATE TABLE "KevCatalog" (
	id INTEGER NOT NULL,
	title TEXT,
	catalog_version TEXT,
	date_released TEXT,
	count INTEGER,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_KevCatalog_id" ON "KevCatalog" (id);

CREATE TABLE "Impact" (
	id INTEGER NOT NULL,
	severity VARCHAR(8),
	vector TEXT,
	score FLOAT,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_Impact_id" ON "Impact" (id);

CREATE TABLE "Configuration" (
	id INTEGER NOT NULL,
	cpe_uri TEXT,
	operator TEXT,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_Configuration_id" ON "Configuration" (id);

CREATE TABLE "KevEntry" (
	vendor_project TEXT NOT NULL,
	product TEXT NOT NULL,
	vulnerability_name TEXT NOT NULL,
	date_added TEXT NOT NULL,
	short_description TEXT NOT NULL,
	required_action TEXT NOT NULL,
	due_date TEXT NOT NULL,
	known_ransomware_campaign_use VARCHAR(7),
	notes TEXT,
	cve_id TEXT NOT NULL,
	title TEXT,
	description TEXT NOT NULL,
	published_date DATETIME,
	last_modified_date DATETIME,
	status VARCHAR(10),
	"KevCatalog_id" INTEGER,
	impact_id INTEGER,
	PRIMARY KEY (cve_id),
	FOREIGN KEY("KevCatalog_id") REFERENCES "KevCatalog" (id),
	FOREIGN KEY(impact_id) REFERENCES "Impact" (id)
);
CREATE INDEX "ix_KevEntry_cve_id" ON "KevEntry" (cve_id);

CREATE TABLE "Vulnerability" (
	cve_id TEXT NOT NULL,
	title TEXT,
	description TEXT NOT NULL,
	published_date DATETIME,
	last_modified_date DATETIME,
	status VARCHAR(10),
	impact_id INTEGER,
	PRIMARY KEY (cve_id),
	FOREIGN KEY(impact_id) REFERENCES "Impact" (id)
);
CREATE INDEX "ix_Vulnerability_cve_id" ON "Vulnerability" (cve_id);

CREATE TABLE "Product" (
	id INTEGER NOT NULL,
	vendor TEXT,
	name TEXT,
	version TEXT,
	"KevEntry_cve_id" TEXT,
	"Vulnerability_cve_id" TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY("KevEntry_cve_id") REFERENCES "KevEntry" (cve_id),
	FOREIGN KEY("Vulnerability_cve_id") REFERENCES "Vulnerability" (cve_id)
);
CREATE INDEX "ix_Product_id" ON "Product" (id);

CREATE TABLE "Reference" (
	id INTEGER NOT NULL,
	url TEXT,
	name TEXT,
	source TEXT,
	"KevEntry_cve_id" TEXT,
	"Vulnerability_cve_id" TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY("KevEntry_cve_id") REFERENCES "KevEntry" (cve_id),
	FOREIGN KEY("Vulnerability_cve_id") REFERENCES "Vulnerability" (cve_id)
);
CREATE INDEX "ix_Reference_id" ON "Reference" (id);

CREATE TABLE "Weakness" (
	id INTEGER NOT NULL,
	cwe_id TEXT,
	name TEXT,
	description TEXT,
	"KevEntry_cve_id" TEXT,
	"Vulnerability_cve_id" TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY("KevEntry_cve_id") REFERENCES "KevEntry" (cve_id),
	FOREIGN KEY("Vulnerability_cve_id") REFERENCES "Vulnerability" (cve_id)
);
CREATE INDEX "ix_Weakness_id" ON "Weakness" (id);

CREATE TABLE "Product_platforms" (
	"Product_id" INTEGER,
	platforms TEXT,
	PRIMARY KEY ("Product_id", platforms),
	FOREIGN KEY("Product_id") REFERENCES "Product" (id)
);
CREATE INDEX "ix_Product_platforms_Product_id" ON "Product_platforms" ("Product_id");
CREATE INDEX "ix_Product_platforms_platforms" ON "Product_platforms" (platforms);
