export type KevVulnerabilityCveID = string;
/**
* What CISA can say about a vulnerability's use in ransomware campaigns.
*/
export enum KevRansomwareCampaignUse {
    
    /** CISA knows of a ransomware campaign that has used it. */
    Known = "Known",
    /** CISA has no confirmation that a ransomware campaign has used it. */
    Unknown = "Unknown",
};
/**
* Whether BOD 26-04 calls for forensic triage of a vulnerability.
*/
export enum KevForensicTriage {
    
    /** The directive calls for forensic triage of this vulnerability. */
    Yes = "Yes",
    /** The directive does not call for forensic triage of this vulnerability. */
    No = "No",
};


/**
 * One published release of the KEV catalog, with the entries it lists.
 */
export interface KevCatalog {
    /** The catalog's human-readable name. */
    title?: string,
    /** The version label of this release of the catalog. */
    catalogVersion: string,
    /** The date and time this release of the catalog came out. */
    dateReleased: string,
    /** How many entries CISA says the catalog holds. */
    count: number,
    /** The entries this release of the catalog lists. */
    vulnerabilities: KevVulnerability[],
}


/**
 * One entry of the KEV catalog, naming a CVE that CISA lists as exploited and the action it asks for by a due date.
 */
export interface KevVulnerability {
    /** The CVE identifier of the listed vulnerability, which identifies the entry. */
    cveID: string,
    /** The vendor or project behind the affected product, as CISA names it. */
    vendorProject: string,
    /** The affected product, as CISA names it. */
    product: string,
    /** The name CISA gives the vulnerability. */
    vulnerabilityName: string,
    /** The day CISA added the vulnerability to the catalog. */
    dateAdded: date,
    /** A brief account of the vulnerability, in CISA's words. */
    shortDescription: string,
    /** What CISA says must be done about the vulnerability. */
    requiredAction: string,
    /** The day by which CISA wants the required action done. */
    dueDate: date,
    /** Whether CISA knows of the vulnerability's use in a ransomware campaign. */
    knownRansomwareCampaignUse?: string,
    /** Whether the vulnerability calls for forensic triage under BOD 26-04. */
    forensicTriage?: string,
    /** Anything else CISA adds about the entry, as free text. */
    notes?: string,
    /** The CWE codes CISA associates with the vulnerability. */
    cwes?: string[],
}



