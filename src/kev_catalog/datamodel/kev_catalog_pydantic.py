from __future__ import annotations

import re
import sys
from datetime import (
    date,
    datetime,
    time
)
from decimal import Decimal
from enum import Enum
from typing import (
    Any,
    ClassVar,
    Literal,
    Optional,
    Union
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    SerializationInfo,
    SerializerFunctionWrapHandler,
    field_validator,
    model_serializer
)


metamodel_version = "1.12.0"
version = "2026-09-17"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        serialize_by_alias = True,
        validate_by_name = True,
        validate_assignment = True,
        validate_default = True,
        extra = "forbid",
        arbitrary_types_allowed = True,
        use_enum_values = True,
        strict = False,
    )





class LinkMLMeta(RootModel):
    root: dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta({'annotations': {'upstream_license': {'tag': 'upstream_license',
                                          'value': 'CC0-1.0'},
                     'upstream_schema_blob': {'tag': 'upstream_schema_blob',
                                              'value': 'ec422845b354f58250d2e99cdfcce17a18659423'},
                     'upstream_schema_commit': {'tag': 'upstream_schema_commit',
                                                'value': 'd98075f22b11ca60ede428f4397966d3523dc692'},
                     'upstream_schema_draft': {'tag': 'upstream_schema_draft',
                                               'value': 'http://json-schema.org/draft-07/schema#'},
                     'upstream_schema_sha256': {'tag': 'upstream_schema_sha256',
                                                'value': '0d5865c98694c5bfba2c78a26caf814f406b3fce8bfb81bef79e99c7f288b0e7'}},
     'comments': ["CISA's JSON schema states no version, so the version here is "
                  'the date of the commit that last changed the file in '
                  'cisagov/kev-data. tests/upstream/ copies the file, and '
                  'scripts/check_upstream_release.py reports when it moves.',
                  "CISA states its data's terms as CC0 1.0, and says that "
                  'third-party links in the data keep their own terms and that use '
                  'of the data gives no right to the CISA Logo or the DHS Seal and '
                  'is no endorsement. NOTICE says the same.'],
     'default_prefix': 'kev_catalog',
     'default_range': 'string',
     'description': 'A LinkML model of the JSON format of the Known Exploited '
                    'Vulnerabilities (KEV) catalog that the Cybersecurity and '
                    "Infrastructure Security Agency (CISA) publishes. CISA's keys "
                    "and values are the schema's, so a real KEV file validates "
                    'unchanged.',
     'id': 'https://w3id.org/lmodel/kev-catalog',
     'imports': ['linkml:types'],
     'license': 'Apache-2.0',
     'name': 'kev_catalog',
     'notes': ["KEV's authority has moved to Binding Operational Directive (BOD) "
               "26-04, which the upstream's README and its forensicTriage "
               'description cite. Directive terms, dates and counts belong at '
               "their source, so none is restated here. CISA's directive pages "
               'answered a plain client with 403 on 2026-11-03: see '
               'https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk'],
     'prefixes': {'cve': {'prefix_prefix': 'cve',
                          'prefix_reference': 'https://w3id.org/lmodel/cve/'},
                  'dcat': {'prefix_prefix': 'dcat',
                           'prefix_reference': 'http://www.w3.org/ns/dcat#'},
                  'dcterms': {'prefix_prefix': 'dcterms',
                              'prefix_reference': 'http://purl.org/dc/terms/'},
                  'kev_catalog': {'prefix_prefix': 'kev_catalog',
                                  'prefix_reference': 'https://w3id.org/lmodel/kev-catalog/'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'schema': {'prefix_prefix': 'schema',
                             'prefix_reference': 'http://schema.org/'},
                  'sepses_cve': {'prefix_prefix': 'sepses_cve',
                                 'prefix_reference': 'http://w3id.org/sepses/vocab/ref/cve#'},
                  'skos': {'prefix_prefix': 'skos',
                           'prefix_reference': 'http://www.w3.org/2004/02/skos/core#'},
                  'spdx3': {'prefix_prefix': 'spdx3',
                            'prefix_reference': 'https://spdx.org/rdf/3.0.1/terms/'},
                  'stix': {'prefix_prefix': 'stix',
                           'prefix_reference': 'https://w3id.org/lmodel/stix/'},
                  'wd': {'prefix_prefix': 'wd',
                         'prefix_reference': 'http://www.wikidata.org/entity/'}},
     'see_also': ['https://lmodel.github.io/kev-catalog',
                  'https://www.cisa.gov/known-exploited-vulnerabilities-catalog',
                  'https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities_schema.json',
                  'https://github.com/cisagov/kev-data'],
     'source': 'https://github.com/cisagov/kev-data/blob/d98075f22b11ca60ede428f4397966d3523dc692/known_exploited_vulnerabilities_schema.json',
     'source_file': 'src/kev_catalog/schema/kev_catalog.yaml',
     'title': 'CISA Known Exploited Vulnerabilities Catalog'} )

class KevRansomwareCampaignUse(str, Enum):
    """
    What CISA can say about a vulnerability's use in ransomware campaigns.
    """
    Known = "Known"
    """
    CISA knows of a ransomware campaign that has used it.
    """
    Unknown = "Unknown"
    """
    CISA has no confirmation that a ransomware campaign has used it.
    """


class KevForensicTriage(str, Enum):
    """
    Whether BOD 26-04 calls for forensic triage of a vulnerability.
    """
    Yes = "Yes"
    """
    The directive calls for forensic triage of this vulnerability.
    """
    No = "No"
    """
    The directive does not call for forensic triage of this vulnerability.
    """



class KevCatalog(ConfiguredBaseModel):
    """
    One published release of the KEV catalog, with the entries it lists.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'upstream_path': {'tag': 'upstream_path', 'value': '#'}},
         'broad_mappings': ['dcat:Dataset', 'schema:Dataset'],
         'class_uri': 'kev_catalog:KevCatalog',
         'comments': ['Each release is a whole file: the catalog is republished as a '
                      'new file, with a new catalogVersion and dateReleased, when an '
                      'entry is added or changed.',
                      "CISA's objects are open, so a key the schema does not name "
                      "passes CISA's JSON schema. This class is closed, so a new key "
                      'fails here until the schema names it.'],
         'from_schema': 'https://w3id.org/lmodel/kev-catalog',
         'notes': ['DCAT 3 defines dcat:Catalog as a curated collection of metadata '
                   'about resources such as datasets, and an entry here describes a '
                   'vulnerability, so that mapping is only related despite the shared '
                   'word. A KEV release is a kind of dataset, so dcat:Dataset and '
                   'schema:Dataset are broader terms, not equivalents.'],
         'related_mappings': ['dcat:Catalog'],
         'see_also': ['https://www.w3.org/TR/vocab-dcat-3/#Class:Dataset',
                      'https://schema.org/Dataset'],
         'tree_root': True})

    title: Optional[str] = Field(default=None, description="""The catalog's human-readable name.""", json_schema_extra = { "linkml_meta": {'annotations': {'upstream_file_key': {'tag': 'upstream_file_key',
                                               'value': 'title'}},
         'comments': ["Every KEV file carries this key, though CISA's JSON schema "
                      'lists it under no property. It is optional here for that '
                      'reason.'],
         'domain_of': ['KevCatalog'],
         'exact_mappings': ['dcterms:title'],
         'slot_uri': 'kev_catalog:title'} })
    catalogVersion: str = Field(default=..., description="""The version label of this release of the catalog.""", json_schema_extra = { "linkml_meta": {'annotations': {'upstream_path': {'tag': 'upstream_path',
                                           'value': '#/properties/catalogVersion'}},
         'close_mappings': ['schema:version'],
         'comments': ['The value reads as a date, such as 2026.10.30, but CISA states '
                      'only a string, so no pattern is given.'],
         'domain_of': ['KevCatalog'],
         'exact_mappings': ['dcat:version'],
         'examples': [{'value': '2026.10.30'}],
         'see_also': ['https://www.w3.org/TR/vocab-dcat-3/#Property:resource_version'],
         'slot_uri': 'kev_catalog:catalogVersion'} })
    dateReleased: datetime  = Field(default=..., description="""The date and time this release of the catalog came out.""", json_schema_extra = { "linkml_meta": {'annotations': {'upstream_path': {'tag': 'upstream_path',
                                           'value': '#/properties/dateReleased'}},
         'close_mappings': ['dcterms:issued', 'schema:datePublished'],
         'domain_of': ['KevCatalog'],
         'examples': [{'value': '2026-10-30T17:02:45.3665Z'}],
         'notes': ["DCAT 3's dcterms:issued is a resource's first known date of "
                   "issuance. CISA's value moves with each release of a living "
                   'catalog, so the mapping is close, not exact.'],
         'see_also': ['https://www.w3.org/TR/vocab-dcat-3/#Property:resource_release_date'],
         'slot_uri': 'kev_catalog:dateReleased'} })
    count: int = Field(default=..., description="""How many entries CISA says the catalog holds.""", json_schema_extra = { "linkml_meta": {'annotations': {'upstream_path': {'tag': 'upstream_path',
                                           'value': '#/properties/count'}},
         'comments': ["CISA calls this the catalog's total. No validator here compares "
                      'it with the list; tests/test_data.py does that in Python, over '
                      'the examples and the pinned catalogue.'],
         'domain_of': ['KevCatalog'],
         'notes': ["schema.org's numberOfItems is declared on ItemList, not Dataset, "
                   'so the mapping is only related.'],
         'related_mappings': ['schema:numberOfItems'],
         'slot_uri': 'kev_catalog:count'} })
    vulnerabilities: list[KevVulnerability] = Field(default=..., description="""The entries this release of the catalog lists.""", json_schema_extra = { "linkml_meta": {'annotations': {'upstream_path': {'tag': 'upstream_path',
                                           'value': '#/properties/vulnerabilities'}},
         'broad_mappings': ['dcterms:hasPart'],
         'domain_of': ['KevCatalog'],
         'slot_uri': 'kev_catalog:vulnerabilities'} })


class KevVulnerability(ConfiguredBaseModel):
    """
    One entry of the KEV catalog, naming a CVE that CISA lists as exploited and the action it asks for by a due date.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'upstream_path': {'tag': 'upstream_path',
                                           'value': '#/$defs/vulnerability'}},
         'class_uri': 'kev_catalog:KevVulnerability',
         'close_mappings': ['spdx3:Security/ExploitCatalogVulnAssessmentRelationship'],
         'comments': ["Four keys are optional in CISA's JSON schema though every entry "
                      'of the pinned catalogue carries them: '
                      'knownRansomwareCampaignUse, forensicTriage, notes and cwes. The '
                      "schema follows CISA's JSON schema."],
         'from_schema': 'https://w3id.org/lmodel/kev-catalog',
         'notes': ['An entry is a statement in a catalog about a vulnerability, not '
                   "the vulnerability itself. Wikidata's Q631425, STIX's vulnerability "
                   "object and SPDX 3.0.1's Security/Vulnerability describe the "
                   'weakness and carry nothing about exploitation or a required '
                   "action, so each is only related. SPDX 3.0.1's "
                   'Security/ExploitCatalogVulnAssessmentRelationship says that a '
                   'vulnerability is listed in an exploit catalog, and names KEV as '
                   "one, so it is close. dcat:CatalogRecord is related, since DCAT's "
                   'record registers a dataset or a service.'],
         'related_mappings': ['wd:Q631425',
                              'stix:StixVulnerability',
                              'spdx3:Security/Vulnerability',
                              'sepses_cve:CVE',
                              'dcat:CatalogRecord',
                              'cve:CveRecord'],
         'see_also': ['https://spdx.github.io/spdx-spec/v3.0.1/model/Security/Classes/ExploitCatalogVulnAssessmentRelationship/',
                      'https://spdx.github.io/spdx-spec/v3.0.1/model/Security/Classes/Vulnerability/',
                      'https://www.wikidata.org/wiki/Q631425',
                      'https://www.w3.org/TR/vocab-dcat-3/#Class:Catalog_Record']})

    cveID: str = Field(default=..., description="""The CVE identifier of the listed vulnerability, which identifies the entry.""", json_schema_extra = { "linkml_meta": {'annotations': {'upstream_path': {'tag': 'upstream_path',
                                           'value': '#/$defs/vulnerability/properties/cveID'}},
         'domain_of': ['KevVulnerability'],
         'exact_mappings': ['cve:cveId'],
         'examples': [{'value': 'CVE-2021-44228'}],
         'notes': ['Exact: a seeded sample of 120 entries on 2026-11-03 found each '
                   "entry's value equal to cveMetadata.cveId in the CVE record of that "
                   'name.'],
         'slot_uri': 'kev_catalog:cveID'} })
    vendorProject: str = Field(default=..., description="""The vendor or project behind the affected product, as CISA names it.""", json_schema_extra = { "linkml_meta": {'annotations': {'upstream_path': {'tag': 'upstream_path',
                                           'value': '#/$defs/vulnerability/properties/vendorProject'}},
         'close_mappings': ['cve:vendor'],
         'domain_of': ['KevVulnerability'],
         'examples': [{'value': 'Apache'}],
         'notes': ['Close, not exact: both name who is responsible for the product, '
                   "but in the sample of 120 entries the value matched a CNA's "
                   'affected vendor on only 54, as CNAs often write a longer legal '
                   'name or n/a.'],
         'slot_uri': 'kev_catalog:vendorProject'} })
    product: str = Field(default=..., description="""The affected product, as CISA names it.""", json_schema_extra = { "linkml_meta": {'annotations': {'upstream_path': {'tag': 'upstream_path',
                                           'value': '#/$defs/vulnerability/properties/product'}},
         'close_mappings': ['cve:product'],
         'domain_of': ['KevVulnerability'],
         'examples': [{'value': 'Log4j2'}],
         'notes': ['Close, not exact: both name the affected product, but in the '
                   "sample of 120 entries the value matched a CNA's affected product "
                   'on only 14, as CNAs often name a release line or write n/a.'],
         'slot_uri': 'kev_catalog:product'} })
    vulnerabilityName: str = Field(default=..., description="""The name CISA gives the vulnerability.""", json_schema_extra = { "linkml_meta": {'annotations': {'upstream_path': {'tag': 'upstream_path',
                                           'value': '#/$defs/vulnerability/properties/vulnerabilityName'}},
         'domain_of': ['KevVulnerability'],
         'notes': ["Related: this is CISA's own wording. In the sample of 120 entries "
                   'only 39 CVE records had a CNA title at all, and 2 of those '
                   'equalled it.'],
         'related_mappings': ['cve:title'],
         'slot_uri': 'kev_catalog:vulnerabilityName'} })
    dateAdded: date = Field(default=..., description="""The day CISA added the vulnerability to the catalog.""", json_schema_extra = { "linkml_meta": {'annotations': {'upstream_path': {'tag': 'upstream_path',
                                           'value': '#/$defs/vulnerability/properties/dateAdded'}},
         'close_mappings': ['dcterms:issued'],
         'domain_of': ['KevVulnerability'],
         'examples': [{'value': '2021-12-10'}],
         'notes': ['DCAT 3 uses dcterms:issued on a catalog record for the date of '
                   'listing, of a dataset or service. An entry here lists a '
                   'vulnerability, so the mapping is close.'],
         'see_also': ['https://www.w3.org/TR/vocab-dcat-3/#Property:record_listing_date'],
         'slot_uri': 'kev_catalog:dateAdded'} })
    shortDescription: str = Field(default=..., description="""A brief account of the vulnerability, in CISA's words.""", json_schema_extra = { "linkml_meta": {'annotations': {'upstream_path': {'tag': 'upstream_path',
                                           'value': '#/$defs/vulnerability/properties/shortDescription'}},
         'domain_of': ['KevVulnerability'],
         'notes': ["Related: this is CISA's own account. In the sample of 120 entries "
                   "none equalled a description in the CVE record's CNA container."],
         'related_mappings': ['cve:descriptions'],
         'slot_uri': 'kev_catalog:shortDescription'} })
    requiredAction: str = Field(default=..., description="""What CISA says must be done about the vulnerability.""", json_schema_extra = { "linkml_meta": {'annotations': {'upstream_path': {'tag': 'upstream_path',
                                           'value': '#/$defs/vulnerability/properties/requiredAction'}},
         'comments': ["Free text. Older entries' text may name a directive since "
                      'replaced, and the schema leaves the text as CISA wrote it.'],
         'domain_of': ['KevVulnerability'],
         'notes': ["Related: a CVE record's solutions say what a CNA offers as a fix, "
                   'and this says what CISA requires, often by pointing to the '
                   "vendor's instructions. STIX's course-of-action is a kind of "
                   'object, not a key, so no slot mapping reaches it.'],
         'related_mappings': ['cve:solutions'],
         'slot_uri': 'kev_catalog:requiredAction'} })
    dueDate: date = Field(default=..., description="""The day by which CISA wants the required action done.""", json_schema_extra = { "linkml_meta": {'annotations': {'upstream_path': {'tag': 'upstream_path',
                                           'value': '#/$defs/vulnerability/properties/dueDate'}},
         'comments': ['CISA states no relation between this and dateAdded, so the '
                      'schema adds none.'],
         'domain_of': ['KevVulnerability'],
         'examples': [{'value': '2021-12-24'}],
         'slot_uri': 'kev_catalog:dueDate'} })
    knownRansomwareCampaignUse: Optional[KevRansomwareCampaignUse] = Field(default=None, description="""Whether CISA knows of the vulnerability's use in a ransomware campaign.""", json_schema_extra = { "linkml_meta": {'annotations': {'upstream_path': {'tag': 'upstream_path',
                                           'value': '#/$defs/vulnerability/properties/knownRansomwareCampaignUse'}},
         'comments': ['CISA types this as a string and names its two values only in '
                      "the property's description, so the enum rests on that sentence "
                      'and on the pinned catalogue.'],
         'domain_of': ['KevVulnerability'],
         'slot_uri': 'kev_catalog:knownRansomwareCampaignUse'} })
    forensicTriage: Optional[KevForensicTriage] = Field(default=None, description="""Whether the vulnerability calls for forensic triage under BOD 26-04.""", json_schema_extra = { "linkml_meta": {'annotations': {'upstream_path': {'tag': 'upstream_path',
                                           'value': '#/$defs/vulnerability/properties/forensicTriage'}},
         'comments': ['CISA types this as a string and names its two values only in '
                      "the property's description, so the enum rests on that sentence "
                      'and on the pinned catalogue.'],
         'domain_of': ['KevVulnerability'],
         'slot_uri': 'kev_catalog:forensicTriage'} })
    notes: Optional[str] = Field(default=None, description="""Anything else CISA adds about the entry, as free text.""", json_schema_extra = { "linkml_meta": {'annotations': {'upstream_path': {'tag': 'upstream_path',
                                           'value': '#/$defs/vulnerability/properties/notes'}},
         'close_mappings': ['skos:note'],
         'comments': ['Often holds addresses separated by " ; ", with empty places '
                      'between them. The schema keeps it one string and parses '
                      'nothing, since CISA states no form for it. Those addresses are '
                      "third parties', under their own terms."],
         'domain_of': ['KevVulnerability'],
         'slot_uri': 'kev_catalog:notes'} })
    cwes: Optional[list[str]] = Field(default=None, description="""The CWE codes CISA associates with the vulnerability.""", json_schema_extra = { "linkml_meta": {'annotations': {'upstream_path': {'tag': 'upstream_path',
                                           'value': '#/$defs/vulnerability/properties/cwes'}},
         'close_mappings': ['cve:cweId'],
         'comments': ['The list may be empty, as it is on some entries of the pinned '
                      'catalogue.'],
         'domain_of': ['KevVulnerability'],
         'examples': [{'value': 'CWE-502'}],
         'notes': ["Close, not exact: both give an entry's CWE codes, but in the "
                   'sample of 120 entries the list equalled the codes of the CVE '
                   "record's CNA and ADP containers together on 94. SEPSES's hasCWE "
                   'links a CVE to a CWE resource, not a code, so it is only related.'],
         'related_mappings': ['sepses_cve:hasCWE'],
         'slot_uri': 'kev_catalog:cwes'} })

    @field_validator('cveID')
    def pattern_cveID(cls, v):
        pattern=re.compile(r"^CVE-[0-9]{4}-[0-9]{4,19}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid cveID format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid cveID format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('cwes')
    def pattern_cwes(cls, v):
        pattern=re.compile(r"^CWE-([0-9])+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid cwes format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid cwes format: {v}"
            raise ValueError(err_msg)
        return v


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
KevCatalog.model_rebuild()
KevVulnerability.model_rebuild()
