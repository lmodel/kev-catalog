export type VulnerabilityCveId = string;
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
 * A single entry in the CISA Known Exploited Vulnerabilities (KEV) catalog, representing one CVE that has been confirmed exploited in the wild and for which clear remediation guidance exists.
 */
export interface Vulnerability {
    /** The CVE identifier assigned to this vulnerability by a CVE Numbering Authority (CNA). Format: CVE-YYYY-NNNNN. */
    cve_id: string,
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
    vulnerabilities?: Vulnerability[],
}



