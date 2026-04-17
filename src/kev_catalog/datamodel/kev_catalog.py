# Auto generated from kev_catalog.yaml by pythongen.py version: 0.0.1
# Generation date: 2026-04-17T12:37:19
# Schema: kev-catalog
#
# id: https://w3id.org/lmodel/kev-catalog
# description: LinkML schema for the CISA Known Exploited Vulnerabilities (KEV) Catalog.
#   The KEV catalog is the authoritative source of vulnerabilities that have
#   been exploited in the wild, maintained by the Cybersecurity and
#   Infrastructure Security Agency (CISA).
# license: Apache-2.0

import dataclasses
import re
from dataclasses import dataclass
from datetime import (
    date,
    datetime,
    time
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)

from jsonasobj2 import (
    JsonObj,
    as_dict
)
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import (
    camelcase,
    sfx,
    underscore
)
from linkml_runtime.utils.metamodelcore import (
    bnode,
    empty_dict,
    empty_list
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str
)
from rdflib import (
    Namespace,
    URIRef
)

from linkml_runtime.linkml_model.types import Integer, String

metamodel_version = "1.7.0"
version = "1.0"

# Namespaces
WIKIDATA = CurieNamespace('WIKIDATA', 'http://identifiers.org/wikidata/')
DCTERMS = CurieNamespace('dcterms', 'http://purl.org/dc/terms/')
KEV_CATALOG = CurieNamespace('kev_catalog', 'https://w3id.org/lmodel/kev-catalog/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
RDFS = CurieNamespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
SKOS = CurieNamespace('skos', 'http://www.w3.org/2004/02/skos/core#')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = KEV_CATALOG


# Types
class CveId(str):
    """ A CVE identifier in the format CVE-YYYY-NNNNN as assigned by a CVE Numbering Authority (CNA). """
    type_class_uri = XSD["string"]
    type_class_curie = "xsd:string"
    type_name = "CveId"
    type_model_uri = KEV_CATALOG.CveId


class IsoDate(str):
    """ A date in ISO 8601 format (YYYY-MM-DD). """
    type_class_uri = XSD["date"]
    type_class_curie = "xsd:date"
    type_name = "IsoDate"
    type_model_uri = KEV_CATALOG.IsoDate


# Class references
class VulnerabilityCveId(extended_str):
    pass


@dataclass(repr=False)
class Vulnerability(YAMLRoot):
    """
    A single entry in the CISA Known Exploited Vulnerabilities (KEV) catalog, representing one CVE that has been
    confirmed exploited in the wild and for which clear remediation guidance exists.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KEV_CATALOG["Vulnerability"]
    class_class_curie: ClassVar[str] = "kev_catalog:Vulnerability"
    class_name: ClassVar[str] = "Vulnerability"
    class_model_uri: ClassVar[URIRef] = KEV_CATALOG.Vulnerability

    cve_id: Union[str, VulnerabilityCveId] = None
    vendor_project: str = None
    product: str = None
    vulnerability_name: str = None
    date_added: str = None
    short_description: str = None
    required_action: str = None
    due_date: str = None
    known_ransomware_campaign_use: Optional[Union[str, "KnownRansomwareCampaignUseEnum"]] = None
    notes: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.cve_id):
            self.MissingRequiredField("cve_id")
        if not isinstance(self.cve_id, VulnerabilityCveId):
            self.cve_id = VulnerabilityCveId(self.cve_id)

        if self._is_empty(self.vendor_project):
            self.MissingRequiredField("vendor_project")
        if not isinstance(self.vendor_project, str):
            self.vendor_project = str(self.vendor_project)

        if self._is_empty(self.product):
            self.MissingRequiredField("product")
        if not isinstance(self.product, str):
            self.product = str(self.product)

        if self._is_empty(self.vulnerability_name):
            self.MissingRequiredField("vulnerability_name")
        if not isinstance(self.vulnerability_name, str):
            self.vulnerability_name = str(self.vulnerability_name)

        if self._is_empty(self.date_added):
            self.MissingRequiredField("date_added")
        if not isinstance(self.date_added, str):
            self.date_added = str(self.date_added)

        if self._is_empty(self.short_description):
            self.MissingRequiredField("short_description")
        if not isinstance(self.short_description, str):
            self.short_description = str(self.short_description)

        if self._is_empty(self.required_action):
            self.MissingRequiredField("required_action")
        if not isinstance(self.required_action, str):
            self.required_action = str(self.required_action)

        if self._is_empty(self.due_date):
            self.MissingRequiredField("due_date")
        if not isinstance(self.due_date, str):
            self.due_date = str(self.due_date)

        if self.known_ransomware_campaign_use is not None and not isinstance(self.known_ransomware_campaign_use, KnownRansomwareCampaignUseEnum):
            self.known_ransomware_campaign_use = KnownRansomwareCampaignUseEnum(self.known_ransomware_campaign_use)

        if self.notes is not None and not isinstance(self.notes, str):
            self.notes = str(self.notes)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class KevCatalog(YAMLRoot):
    """
    The CISA Known Exploited Vulnerabilities (KEV) Catalog — the authoritative source of vulnerabilities confirmed
    exploited in the wild, maintained by CISA per Binding Operational Directive (BOD) 22-01.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KEV_CATALOG["KevCatalog"]
    class_class_curie: ClassVar[str] = "kev_catalog:KevCatalog"
    class_name: ClassVar[str] = "KevCatalog"
    class_model_uri: ClassVar[URIRef] = KEV_CATALOG.KevCatalog

    title: Optional[str] = None
    catalog_version: Optional[str] = None
    date_released: Optional[str] = None
    count: Optional[int] = None
    vulnerabilities: Optional[Union[dict[Union[str, VulnerabilityCveId], Union[dict, Vulnerability]], list[Union[dict, Vulnerability]]]] = empty_dict()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.catalog_version is not None and not isinstance(self.catalog_version, str):
            self.catalog_version = str(self.catalog_version)

        if self.date_released is not None and not isinstance(self.date_released, str):
            self.date_released = str(self.date_released)

        if self.count is not None and not isinstance(self.count, int):
            self.count = int(self.count)

        self._normalize_inlined_as_list(slot_name="vulnerabilities", slot_type=Vulnerability, key_name="cve_id", keyed=True)

        super().__post_init__(**kwargs)


# Enumerations
class KnownRansomwareCampaignUseEnum(EnumDefinitionImpl):
    """
    Whether the vulnerability is known to have been used in ransomware campaigns.
    """
    known = PermissibleValue(
        text="known",
        description="The vulnerability is known to have been used in a ransomware campaign.",
        meaning=WIKIDATA["Q532924"])
    unknown = PermissibleValue(
        text="unknown",
        description="It is not known whether the vulnerability has been used in a ransomware campaign.")

    _defn = EnumDefinition(
        name="KnownRansomwareCampaignUseEnum",
        description="Whether the vulnerability is known to have been used in ransomware campaigns.",
    )

# Slots
class slots:
    pass

slots.cve_id = Slot(uri=DCTERMS.identifier, name="cve_id", curie=DCTERMS.curie('identifier'),
                   model_uri=KEV_CATALOG.cve_id, domain=None, range=URIRef)

slots.vendor_project = Slot(uri=SCHEMA.Organization, name="vendor_project", curie=SCHEMA.curie('Organization'),
                   model_uri=KEV_CATALOG.vendor_project, domain=None, range=str)

slots.product = Slot(uri=SCHEMA.name, name="product", curie=SCHEMA.curie('name'),
                   model_uri=KEV_CATALOG.product, domain=None, range=str)

slots.vulnerability_name = Slot(uri=DCTERMS.title, name="vulnerability_name", curie=DCTERMS.curie('title'),
                   model_uri=KEV_CATALOG.vulnerability_name, domain=None, range=str)

slots.date_added = Slot(uri=DCTERMS.created, name="date_added", curie=DCTERMS.curie('created'),
                   model_uri=KEV_CATALOG.date_added, domain=None, range=str)

slots.short_description = Slot(uri=DCTERMS.description, name="short_description", curie=DCTERMS.curie('description'),
                   model_uri=KEV_CATALOG.short_description, domain=None, range=str)

slots.required_action = Slot(uri=KEV_CATALOG.required_action, name="required_action", curie=KEV_CATALOG.curie('required_action'),
                   model_uri=KEV_CATALOG.required_action, domain=None, range=str)

slots.due_date = Slot(uri=KEV_CATALOG.due_date, name="due_date", curie=KEV_CATALOG.curie('due_date'),
                   model_uri=KEV_CATALOG.due_date, domain=None, range=str)

slots.known_ransomware_campaign_use = Slot(uri=KEV_CATALOG.known_ransomware_campaign_use, name="known_ransomware_campaign_use", curie=KEV_CATALOG.curie('known_ransomware_campaign_use'),
                   model_uri=KEV_CATALOG.known_ransomware_campaign_use, domain=None, range=Optional[Union[str, "KnownRansomwareCampaignUseEnum"]])

slots.notes = Slot(uri=SKOS.note, name="notes", curie=SKOS.curie('note'),
                   model_uri=KEV_CATALOG.notes, domain=None, range=Optional[str])

slots.title = Slot(uri=DCTERMS.title, name="title", curie=DCTERMS.curie('title'),
                   model_uri=KEV_CATALOG.title, domain=None, range=Optional[str])

slots.catalog_version = Slot(uri=KEV_CATALOG.catalog_version, name="catalog_version", curie=KEV_CATALOG.curie('catalog_version'),
                   model_uri=KEV_CATALOG.catalog_version, domain=None, range=Optional[str])

slots.date_released = Slot(uri=KEV_CATALOG.date_released, name="date_released", curie=KEV_CATALOG.curie('date_released'),
                   model_uri=KEV_CATALOG.date_released, domain=None, range=Optional[str])

slots.count = Slot(uri=KEV_CATALOG.count, name="count", curie=KEV_CATALOG.curie('count'),
                   model_uri=KEV_CATALOG.count, domain=None, range=Optional[int])

slots.vulnerabilities = Slot(uri=KEV_CATALOG.vulnerabilities, name="vulnerabilities", curie=KEV_CATALOG.curie('vulnerabilities'),
                   model_uri=KEV_CATALOG.vulnerabilities, domain=None, range=Optional[Union[dict[Union[str, VulnerabilityCveId], Union[dict, Vulnerability]], list[Union[dict, Vulnerability]]]])
