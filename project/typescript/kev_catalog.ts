export type VulnerabilityCveId = string;
export type KevEntryCveId = string;
/**
* Lifecycle state of a vulnerability record.
*/
export enum VulnerabilityStatus {
    
    /** Vulnerability is actively maintained and published. */
    ACTIVE = "ACTIVE",
    /** CVE ID was rejected and should not be used. */
    REJECTED = "REJECTED",
    /** The vulnerability details are disputed by a party. */
    DISPUTED = "DISPUTED",
    /** CVE ID is reserved but details are not yet published. */
    RESERVED = "RESERVED",
    /** Entry has been superseded or withdrawn. */
    DEPRECATED = "DEPRECATED",
};
/**
* CVSS qualitative severity rating.
*/
export enum ImpactSeverity {
    
    /** No measurable impact. */
    NONE = "NONE",
    /** Limited impact; exploitation requires specific conditions. */
    LOW = "LOW",
    /** Moderate impact; partial compromise of security properties. */
    MEDIUM = "MEDIUM",
    /** High impact; significant compromise of security properties. */
    HIGH = "HIGH",
    /** Critical impact; complete compromise; remote exploitation likely. */
    CRITICAL = "CRITICAL",
    /** Severity has not been assessed or is unavailable. */
    UNKNOWN = "UNKNOWN",
};
/**
* Whether the vulnerability is known to have been used in ransomware campaigns.
*/
export enum KnownRansomwareCampaignUseEnum {
    
    /** The vulnerability is known to have been used in a ransomware campaign. */
    known = "known",
    /** It is not known whether the vulnerability has been used in a ransomware campaign. */
    unknown = "unknown",
};


/**
 * Abstract base representation of a security vulnerability. Extended by source-specific schemas (KEV, CVE, NVD).
 */
export interface Vulnerability {
    /** The CVE identifier assigned by a CVE Numbering Authority (CNA). Format: CVE-YYYY-NNNNN. */
    cve_id: string,
    /** Short human-readable title or name for this entity. */
    title?: string,
    /** Narrative description of the vulnerability. */
    description: string,
    /** Date and time the vulnerability was first published. */
    published_date?: string,
    /** Date and time the vulnerability record was last modified. */
    last_modified_date?: string,
    /** Products affected by this vulnerability. */
    products?: Product[],
    /** Weakness classifications (e.g. CWE) associated with this vulnerability. */
    weaknesses?: Weakness[],
    /** External references such as advisories and articles. */
    references?: Reference[],
    /** Impact and severity assessment for this vulnerability. */
    impact?: Impact,
    /** Current lifecycle state of the vulnerability record. */
    status?: string,
}


/**
 * Software or hardware entity affected by the vulnerability.
 */
export interface Product {
    /** Name of the vendor or organization responsible for the product. */
    vendor?: string,
    /** Name of the entity (product, weakness, reference, etc.). */
    name?: string,
    /** Version string of the affected product. */
    version?: string,
    /** Platforms or operating environments affected. */
    platforms?: string[],
}


/**
 * External reference such as an advisory or article.
 */
export interface Reference {
    /** URL pointing to the reference resource. */
    url?: string,
    /** Name of the entity (product, weakness, reference, etc.). */
    name?: string,
    /** Source or origin of the reference or data. */
    source?: string,
}


/**
 * Weakness classification from CWE or a similar taxonomy.
 */
export interface Weakness {
    /** CWE identifier for the weakness classification (e.g. CWE-79). */
    cwe_id?: string,
    /** Name of the entity (product, weakness, reference, etc.). */
    name?: string,
    /** Narrative description of the vulnerability. */
    description?: string,
}


/**
 * Assessment of the vulnerability's impact and severity.
 */
export interface Impact {
    /** Qualitative severity rating. */
    severity?: string,
    /** CVSS vector string or equivalent scoring vector expression. */
    vector?: string,
    /** Numeric vulnerability score (e.g. CVSS base score). */
    score?: number,
}


/**
 * Logical grouping of CPE match expressions.
 */
export interface Configuration {
    /** CPE 2.2 URI identifying an affected product configuration. */
    cpe_uri?: string,
    /** Logical operator (AND/OR) used in configuration node groupings. */
    operator?: string,
}


/**
 * A single entry in the CISA Known Exploited Vulnerabilities (KEV) catalog, representing one CVE that has been confirmed exploited in the wild and for which clear remediation guidance exists.
 */
export interface KevEntry extends Vulnerability {
    /** The name of the vendor or project responsible for the affected product. */
    vendor_project: string,
    /** The name of the affected product. */
    product: string,
    /** A short, descriptive name for the vulnerability. */
    vulnerability_name: string,
    /** The date (YYYY-MM-DD) the vulnerability was added to the KEV catalog. */
    date_added: string,
    /** A brief description of the vulnerability. */
    short_description: string,
    /** The remediation action required, e.g. "Apply updates per vendor instructions." */
    required_action: string,
    /** The date (YYYY-MM-DD) by which federal civilian executive branch (FCEB) agencies must remediate the vulnerability per BOD 22-01. */
    due_date: string,
    /** Whether the vulnerability is known to have been leveraged as part of a ransomware campaign. */
    known_ransomware_campaign_use?: string,
    /** Additional notes or references related to the vulnerability or its remediation. */
    notes?: string,
}


/**
 * The CISA Known Exploited Vulnerabilities (KEV) Catalog — the authoritative source of vulnerabilities confirmed exploited in the wild, maintained by CISA per Binding Operational Directive (BOD) 22-01.
 */
export interface KevCatalog {
    /** The title of the KEV catalog. */
    title?: string,
    /** The version string of the KEV catalog release. */
    catalog_version?: string,
    /** The ISO 8601 timestamp at which this catalog version was released. */
    date_released?: string,
    /** The total number of vulnerabilities in this catalog version. */
    count?: number,
    /** The list of known exploited vulnerabilities. */
    vulnerabilities?: KevEntry[],
}



