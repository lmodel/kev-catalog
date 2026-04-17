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


metamodel_version = "1.7.0"
version = "1.0"


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


linkml_meta = LinkMLMeta({'default_prefix': 'kev_catalog',
     'default_range': 'string',
     'description': 'LinkML schema for the CISA Known Exploited Vulnerabilities '
                    '(KEV) Catalog.\n'
                    'The KEV catalog is the authoritative source of '
                    'vulnerabilities that have\n'
                    'been exploited in the wild, maintained by the Cybersecurity '
                    'and\n'
                    'Infrastructure Security Agency (CISA).',
     'id': 'https://w3id.org/lmodel/kev-catalog',
     'imports': ['linkml:types'],
     'license': 'Apache-2.0',
     'name': 'kev-catalog',
     'notes': ['This is a Schema. The KEV database is distributed under the CC0 '
               '1.0 Universal license. You may use this data in any legal manner '
               'but note that information  provided at any 3rd party links '
               'included in the KEV database are bound by the policies and '
               'licenses of those 3rd party websites. Use of the information does '
               'not authorize you to use the CISA Logo or DHS Seal, nor should '
               'such use be interpreted as an endorsement by CISA or DHS.',
               'Mandated by Binding Operational Directive (BOD) 22-01, "Reducing '
               'the Significant Risk of Known Exploited Vulnerabilities", issued '
               'under the authority of Section 3553(b)(2) of title 44, U.S. Code.',
               'BOD 22-01 applies to all federal civilian executive branch (FCEB) '
               'departments and agencies. It does NOT apply to statutorily defined '
               'national security systems nor to systems operated by the '
               'Department of Defense or the Intelligence Community.',
               'BOD 22-01 key compliance milestones: Nov 17 2021 — remediate CVEs '
               'assigned 2021+; Jan 2 2022 — update agency policies; Jan 17 2022 — '
               'first CyberScope status report; May 3 2022 — remediate pre-2021 '
               'CVEs; Oct 1 2022 — reporting via CDM Federal Dashboard.',
               'As of 2022-07-15 the KEV catalog contained 787 entries drawn from '
               'a universe of ~179,383 total CVEs (56,342 Critical/High by CVSS).',
               'Contact: CyberDirectives@cisa.dhs.gov for questions about BOD '
               '22-01 and the KEV catalog; CyberLiaison@cisa.dhs.gov for all other '
               'CISA questions.'],
     'prefixes': {'WIKIDATA': {'prefix_prefix': 'WIKIDATA',
                               'prefix_reference': 'http://identifiers.org/wikidata/'},
                  'dcterms': {'prefix_prefix': 'dcterms',
                              'prefix_reference': 'http://purl.org/dc/terms/'},
                  'kev_catalog': {'prefix_prefix': 'kev_catalog',
                                  'prefix_reference': 'https://w3id.org/lmodel/kev-catalog/'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'rdfs': {'prefix_prefix': 'rdfs',
                           'prefix_reference': 'http://www.w3.org/2000/01/rdf-schema#'},
                  'schema': {'prefix_prefix': 'schema',
                             'prefix_reference': 'http://schema.org/'},
                  'skos': {'prefix_prefix': 'skos',
                           'prefix_reference': 'http://www.w3.org/2004/02/skos/core#'},
                  'xsd': {'prefix_prefix': 'xsd',
                          'prefix_reference': 'http://www.w3.org/2001/XMLSchema#'}},
     'see_also': ['https://lmodel.github.io/kev-catalog',
                  'https://www.cisa.gov/known-exploited-vulnerabilities-catalog',
                  'https://www.cisa.gov/directives',
                  'https://www.cisa.gov/binding-operational-directive-22-01',
                  'https://weis2020.econinfosec.org/wp-content/uploads/sites/8/2020/06/weis20-final6.pdf'],
     'source': 'https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities_schema.json',
     'source_file': 'src/kev_catalog/schema/kev_catalog.yaml',
     'title': 'CISA Known Exploited Vulnerabilities (KEV) Catalog',
     'types': {'CveId': {'base': 'str',
                         'description': 'A CVE identifier in the format '
                                        'CVE-YYYY-NNNNN as assigned by a CVE '
                                        'Numbering Authority (CNA).',
                         'from_schema': 'https://w3id.org/lmodel/kev-catalog',
                         'name': 'CveId',
                         'notes': ['The first KEV inclusion criterion: the '
                                   'vulnerability must have an assigned CVE ID. '
                                   'The CVE Program is sponsored by CISA and '
                                   'operated by The MITRE Corporation.'],
                         'pattern': '^CVE-[0-9]{4}-[0-9]+$',
                         'uri': 'xsd:string'},
               'IsoDate': {'base': 'str',
                           'description': 'A date in ISO 8601 format (YYYY-MM-DD).',
                           'from_schema': 'https://w3id.org/lmodel/kev-catalog',
                           'name': 'IsoDate',
                           'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}$',
                           'uri': 'xsd:date'}}} )

class KnownRansomwareCampaignUseEnum(str, Enum):
    """
    Whether the vulnerability is known to have been used in ransomware campaigns.
    """
    known = "known"
    """
    The vulnerability is known to have been used in a ransomware campaign.
    """
    unknown = "unknown"
    """
    It is not known whether the vulnerability has been used in a ransomware campaign.
    """



class Vulnerability(ConfiguredBaseModel):
    """
    A single entry in the CISA Known Exploited Vulnerabilities (KEV) catalog, representing one CVE that has been confirmed exploited in the wild and for which clear remediation guidance exists.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'comments': ['Three criteria must all be met for inclusion: (1) assigned CVE '
                      'ID, (2) reliable evidence of active exploitation in the wild, '
                      'and (3) clear remediation guidance (vendor update or EOL '
                      'removal).',
                      'BOD 22-01 focuses on a small, high-signal subset of all '
                      'vulnerabilities: as of 2022-07-15 the catalog contained 787 '
                      'KEVs from a universe of ~179,383 CVEs, and approximately 20 of '
                      'those KEVs were the most prevalent across the entire federal '
                      'enterprise.'],
         'exact_mappings': ['schema:SoftwareApplication', 'WIKIDATA:Q16798631'],
         'from_schema': 'https://w3id.org/lmodel/kev-catalog',
         'see_also': ['https://www.cisa.gov/known-exploited-vulnerabilities-catalog']})

    cve_id: str = Field(default=..., description="""The CVE identifier assigned to this vulnerability by a CVE Numbering Authority (CNA). Format: CVE-YYYY-NNNNN.""", json_schema_extra = { "linkml_meta": {'aliases': ['cveID'],
         'domain_of': ['Vulnerability'],
         'exact_mappings': ['schema:identifier'],
         'slot_uri': 'dcterms:identifier'} })
    vendor_project: str = Field(default=..., description="""The name of the vendor or project responsible for the affected product.""", json_schema_extra = { "linkml_meta": {'aliases': ['vendorProject'],
         'domain_of': ['Vulnerability'],
         'slot_uri': 'schema:Organization'} })
    product: str = Field(default=..., description="""The name of the affected product.""", json_schema_extra = { "linkml_meta": {'aliases': ['product'],
         'domain_of': ['Vulnerability'],
         'slot_uri': 'schema:name'} })
    vulnerability_name: str = Field(default=..., description="""A short, descriptive name for the vulnerability.""", json_schema_extra = { "linkml_meta": {'aliases': ['vulnerabilityName'],
         'domain_of': ['Vulnerability'],
         'slot_uri': 'dcterms:title'} })
    date_added: str = Field(default=..., description="""The date (YYYY-MM-DD) the vulnerability was added to the KEV catalog.""", json_schema_extra = { "linkml_meta": {'aliases': ['dateAdded'],
         'domain_of': ['Vulnerability'],
         'slot_uri': 'dcterms:created'} })
    short_description: str = Field(default=..., description="""A brief description of the vulnerability.""", json_schema_extra = { "linkml_meta": {'aliases': ['shortDescription'],
         'comments': ['KEV inclusion criterion #2 requires reliable evidence that the '
                      'vulnerability has been actively exploited in the wild. Active '
                      'exploitation includes attempted and successful exploitation; '
                      'scanning, security research, and public PoC alone do not '
                      'qualify.'],
         'domain_of': ['Vulnerability'],
         'slot_uri': 'dcterms:description'} })
    required_action: str = Field(default=..., description="""The remediation action required, e.g. \"Apply updates per vendor instructions.\"""", json_schema_extra = { "linkml_meta": {'aliases': ['requiredAction'],
         'comments': ['BOD 22-01 specifies two acceptable actions: (1) apply updates '
                      'per vendor instructions, or (2) remove the product from agency '
                      'networks if it is end-of-life or cannot otherwise be updated. '
                      'Temporary mitigations and workarounds may be applied while '
                      'awaiting a vendor patch.'],
         'domain_of': ['Vulnerability']} })
    due_date: str = Field(default=..., description="""The date (YYYY-MM-DD) by which federal civilian executive branch (FCEB) agencies must remediate the vulnerability per BOD 22-01.""", json_schema_extra = { "linkml_meta": {'aliases': ['dueDate'],
         'comments': ['Deadline set by CISA. Under BOD 19-02, internet-accessible '
                      'critical vulnerabilities (CVSS >9.0) must be remediated within '
                      '15 calendar days and high vulnerabilities (7.0-9.0) within 30 '
                      'calendar days of initial detection; BOD 22-01 due dates may be '
                      'tighter and apply to all agency systems, not only '
                      'internet-accessible ones.'],
         'domain_of': ['Vulnerability']} })
    known_ransomware_campaign_use: Optional[KnownRansomwareCampaignUseEnum] = Field(default=None, description="""Whether the vulnerability is known to have been leveraged as part of a ransomware campaign.""", json_schema_extra = { "linkml_meta": {'aliases': ['knownRansomwareCampaignUse'],
         'domain_of': ['Vulnerability'],
         'notes': ['CISA encourages organizations with evidence of exploited '
                   'vulnerabilities not listed in the KEV to submit them to '
                   'vulnerability@mail.cisa.dhs.gov.']} })
    notes: Optional[str] = Field(default=None, description="""Additional notes or references related to the vulnerability or its remediation.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Vulnerability'], 'slot_uri': 'skos:note'} })


class KevCatalog(ConfiguredBaseModel):
    """
    The CISA Known Exploited Vulnerabilities (KEV) Catalog — the authoritative source of vulnerabilities confirmed exploited in the wild, maintained by CISA per Binding Operational Directive (BOD) 22-01.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'contact_directives': {'tag': 'contact_directives',
                                                'value': 'CyberDirectives@cisa.dhs.gov'},
                         'contact_general': {'tag': 'contact_general',
                                             'value': 'CyberLiaison@cisa.dhs.gov'},
                         'directive_date': {'tag': 'directive_date',
                                            'value': '2021-11-03'},
                         'directive_id': {'tag': 'directive_id', 'value': 'BOD 22-01'},
                         'issuing_body': {'tag': 'issuing_body',
                                          'value': 'Department of Homeland Security / '
                                                   'CISA'},
                         'legal_authority': {'tag': 'legal_authority',
                                             'value': '44 U.S.C. § 3553(b)(2)'}},
         'comments': ['BOD 22-01, "Reducing the Significant Risk of Known Exploited '
                      'Vulnerabilities", was issued under Section 3553(b)(2) of title '
                      '44, U.S. Code by the Secretary of Homeland Security. It is a '
                      'compulsory direction to all FCEB departments and agencies.',
                      'CISA strongly recommends all organizations — including state, '
                      'local, tribal and territorial (SLTT) governments and private '
                      'sector — prioritize remediation of KEV catalog entries as part '
                      'of their vulnerability management plan, even though BOD 22-01 '
                      'itself only binds FCEB agencies.',
                      'BOD 22-01 does not apply to: national security systems (as '
                      'defined by statute), systems operated by the Department of '
                      'Defense, or systems operated by the Intelligence Community.'],
         'exact_mappings': ['schema:Dataset', 'WIKIDATA:Q1172284'],
         'from_schema': 'https://w3id.org/lmodel/kev-catalog',
         'see_also': ['https://www.cisa.gov/directives',
                      'https://www.cisa.gov/binding-operational-directive-22-01'],
         'tree_root': True})

    title: Optional[str] = Field(default=None, description="""The title of the KEV catalog.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KevCatalog'], 'slot_uri': 'dcterms:title'} })
    catalog_version: Optional[str] = Field(default=None, description="""The version string of the KEV catalog release.""", json_schema_extra = { "linkml_meta": {'aliases': ['catalogVersion'], 'domain_of': ['KevCatalog']} })
    date_released: Optional[str] = Field(default=None, description="""The ISO 8601 timestamp at which this catalog version was released.""", json_schema_extra = { "linkml_meta": {'aliases': ['dateReleased'], 'domain_of': ['KevCatalog']} })
    count: Optional[int] = Field(default=None, description="""The total number of vulnerabilities in this catalog version.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KevCatalog']} })
    vulnerabilities: Optional[list[Vulnerability]] = Field(default=None, description="""The list of known exploited vulnerabilities.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KevCatalog']} })


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
Vulnerability.model_rebuild()
KevCatalog.model_rebuild()
