# Auto generated from kev_catalog.yaml by pythongen.py version: 0.0.1
# Generation date: 2026-04-17T16:36:20
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

from linkml_runtime.linkml_model.types import Datetime, Float, Integer, String, Uri
from linkml_runtime.utils.metamodelcore import URI, XSDDateTime

metamodel_version = "1.7.0"
version = "1.0"

# Namespaces
WIKIDATA = CurieNamespace('WIKIDATA', 'https://www.wikidata.org/wiki/')
CORE = CurieNamespace('core', 'https://w3id.org/lmodel/vulnerability-core/')
DCT = CurieNamespace('dct', 'http://purl.org/dc/terms/')
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
    """ A CVE identifier assigned by a CVE Numbering Authority (CNA). Format: CVE-YYYY-NNNNN. """
    type_class_uri = XSD["string"]
    type_class_curie = "xsd:string"
    type_name = "CveId"
    type_model_uri = KEV_CATALOG.CveId


class IsoDate(str):
    """ A calendar date in ISO 8601 format (YYYY-MM-DD). """
    type_class_uri = XSD["date"]
    type_class_curie = "xsd:date"
    type_name = "IsoDate"
    type_model_uri = KEV_CATALOG.IsoDate


# Class references
class VulnerabilityCveId(extended_str):
    pass


class KevEntryCveId(VulnerabilityCveId):
    pass


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
    vulnerabilities: Optional[Union[dict[Union[str, KevEntryCveId], Union[dict, "KevEntry"]], list[Union[dict, "KevEntry"]]]] = empty_dict()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.catalog_version is not None and not isinstance(self.catalog_version, str):
            self.catalog_version = str(self.catalog_version)

        if self.date_released is not None and not isinstance(self.date_released, str):
            self.date_released = str(self.date_released)

        if self.count is not None and not isinstance(self.count, int):
            self.count = int(self.count)

        self._normalize_inlined_as_list(slot_name="vulnerabilities", slot_type=KevEntry, key_name="cve_id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Vulnerability(YAMLRoot):
    """
    Abstract base representation of a security vulnerability. Extended by source-specific schemas (KEV, CVE, NVD).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CORE["Vulnerability"]
    class_class_curie: ClassVar[str] = "core:Vulnerability"
    class_name: ClassVar[str] = "Vulnerability"
    class_model_uri: ClassVar[URIRef] = KEV_CATALOG.Vulnerability

    cve_id: Union[str, VulnerabilityCveId] = None
    description: str = None
    title: Optional[str] = None
    published_date: Optional[Union[str, XSDDateTime]] = None
    last_modified_date: Optional[Union[str, XSDDateTime]] = None
    products: Optional[Union[Union[dict, "Product"], list[Union[dict, "Product"]]]] = empty_list()
    weaknesses: Optional[Union[Union[dict, "Weakness"], list[Union[dict, "Weakness"]]]] = empty_list()
    references: Optional[Union[Union[dict, "Reference"], list[Union[dict, "Reference"]]]] = empty_list()
    impact: Optional[Union[dict, "Impact"]] = None
    status: Optional[Union[str, "VulnerabilityStatus"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.cve_id):
            self.MissingRequiredField("cve_id")
        if not isinstance(self.cve_id, VulnerabilityCveId):
            self.cve_id = VulnerabilityCveId(self.cve_id)

        if self._is_empty(self.description):
            self.MissingRequiredField("description")
        if not isinstance(self.description, str):
            self.description = str(self.description)

        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.published_date is not None and not isinstance(self.published_date, XSDDateTime):
            self.published_date = XSDDateTime(self.published_date)

        if self.last_modified_date is not None and not isinstance(self.last_modified_date, XSDDateTime):
            self.last_modified_date = XSDDateTime(self.last_modified_date)

        if not isinstance(self.products, list):
            self.products = [self.products] if self.products is not None else []
        self.products = [v if isinstance(v, Product) else Product(**as_dict(v)) for v in self.products]

        if not isinstance(self.weaknesses, list):
            self.weaknesses = [self.weaknesses] if self.weaknesses is not None else []
        self.weaknesses = [v if isinstance(v, Weakness) else Weakness(**as_dict(v)) for v in self.weaknesses]

        if not isinstance(self.references, list):
            self.references = [self.references] if self.references is not None else []
        self.references = [v if isinstance(v, Reference) else Reference(**as_dict(v)) for v in self.references]

        if self.impact is not None and not isinstance(self.impact, Impact):
            self.impact = Impact(**as_dict(self.impact))

        if self.status is not None and not isinstance(self.status, VulnerabilityStatus):
            self.status = VulnerabilityStatus(self.status)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class KevEntry(Vulnerability):
    """
    A single entry in the CISA Known Exploited Vulnerabilities (KEV) catalog, representing one CVE that has been
    confirmed exploited in the wild and for which clear remediation guidance exists.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KEV_CATALOG["KevEntry"]
    class_class_curie: ClassVar[str] = "kev_catalog:KevEntry"
    class_name: ClassVar[str] = "KevEntry"
    class_model_uri: ClassVar[URIRef] = KEV_CATALOG.KevEntry

    cve_id: Union[str, KevEntryCveId] = None
    description: str = None
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
        if not isinstance(self.cve_id, KevEntryCveId):
            self.cve_id = KevEntryCveId(self.cve_id)

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
class Product(YAMLRoot):
    """
    Software or hardware entity affected by the vulnerability.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CORE["Product"]
    class_class_curie: ClassVar[str] = "core:Product"
    class_name: ClassVar[str] = "Product"
    class_model_uri: ClassVar[URIRef] = KEV_CATALOG.Product

    vendor: Optional[str] = None
    name: Optional[str] = None
    version: Optional[str] = None
    platforms: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.vendor is not None and not isinstance(self.vendor, str):
            self.vendor = str(self.vendor)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.version is not None and not isinstance(self.version, str):
            self.version = str(self.version)

        if not isinstance(self.platforms, list):
            self.platforms = [self.platforms] if self.platforms is not None else []
        self.platforms = [v if isinstance(v, str) else str(v) for v in self.platforms]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Reference(YAMLRoot):
    """
    External reference such as an advisory or article.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CORE["Reference"]
    class_class_curie: ClassVar[str] = "core:Reference"
    class_name: ClassVar[str] = "Reference"
    class_model_uri: ClassVar[URIRef] = KEV_CATALOG.Reference

    url: Optional[Union[str, URI]] = None
    name: Optional[str] = None
    source: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.url is not None and not isinstance(self.url, URI):
            self.url = URI(self.url)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.source is not None and not isinstance(self.source, str):
            self.source = str(self.source)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Weakness(YAMLRoot):
    """
    Weakness classification from CWE or a similar taxonomy.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CORE["Weakness"]
    class_class_curie: ClassVar[str] = "core:Weakness"
    class_name: ClassVar[str] = "Weakness"
    class_model_uri: ClassVar[URIRef] = KEV_CATALOG.Weakness

    cwe_id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.cwe_id is not None and not isinstance(self.cwe_id, str):
            self.cwe_id = str(self.cwe_id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Impact(YAMLRoot):
    """
    Assessment of the vulnerability's impact and severity.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CORE["Impact"]
    class_class_curie: ClassVar[str] = "core:Impact"
    class_name: ClassVar[str] = "Impact"
    class_model_uri: ClassVar[URIRef] = KEV_CATALOG.Impact

    severity: Optional[Union[str, "ImpactSeverity"]] = None
    vector: Optional[str] = None
    score: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.severity is not None and not isinstance(self.severity, ImpactSeverity):
            self.severity = ImpactSeverity(self.severity)

        if self.vector is not None and not isinstance(self.vector, str):
            self.vector = str(self.vector)

        if self.score is not None and not isinstance(self.score, float):
            self.score = float(self.score)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Configuration(YAMLRoot):
    """
    Logical grouping of CPE match expressions.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CORE["Configuration"]
    class_class_curie: ClassVar[str] = "core:Configuration"
    class_name: ClassVar[str] = "Configuration"
    class_model_uri: ClassVar[URIRef] = KEV_CATALOG.Configuration

    cpe_uri: Optional[str] = None
    operator: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.cpe_uri is not None and not isinstance(self.cpe_uri, str):
            self.cpe_uri = str(self.cpe_uri)

        if self.operator is not None and not isinstance(self.operator, str):
            self.operator = str(self.operator)

        super().__post_init__(**kwargs)


# Enumerations
class KnownRansomwareCampaignUseEnum(EnumDefinitionImpl):
    """
    Whether the vulnerability is known to have been used in ransomware campaigns.
    """
    known = PermissibleValue(
        text="known",
        description="The vulnerability is known to have been used in a ransomware campaign.")
    unknown = PermissibleValue(
        text="unknown",
        description="It is not known whether the vulnerability has been used in a ransomware campaign.")

    _defn = EnumDefinition(
        name="KnownRansomwareCampaignUseEnum",
        description="Whether the vulnerability is known to have been used in ransomware campaigns.",
    )

class VulnerabilityStatus(EnumDefinitionImpl):
    """
    Lifecycle state of a vulnerability record.
    """
    ACTIVE = PermissibleValue(
        text="ACTIVE",
        description="Vulnerability is actively maintained and published.")
    REJECTED = PermissibleValue(
        text="REJECTED",
        description="CVE ID was rejected and should not be used.")
    DISPUTED = PermissibleValue(
        text="DISPUTED",
        description="The vulnerability details are disputed by a party.")
    RESERVED = PermissibleValue(
        text="RESERVED",
        description="CVE ID is reserved but details are not yet published.")
    DEPRECATED = PermissibleValue(
        text="DEPRECATED",
        description="Entry has been superseded or withdrawn.")

    _defn = EnumDefinition(
        name="VulnerabilityStatus",
        description="Lifecycle state of a vulnerability record.",
    )

class ImpactSeverity(EnumDefinitionImpl):
    """
    CVSS qualitative severity rating.
    """
    NONE = PermissibleValue(
        text="NONE",
        description="No measurable impact.")
    LOW = PermissibleValue(
        text="LOW",
        description="Limited impact; exploitation requires specific conditions.")
    MEDIUM = PermissibleValue(
        text="MEDIUM",
        description="Moderate impact; partial compromise of security properties.")
    HIGH = PermissibleValue(
        text="HIGH",
        description="High impact; significant compromise of security properties.")
    CRITICAL = PermissibleValue(
        text="CRITICAL",
        description="Critical impact; complete compromise; remote exploitation likely.")
    UNKNOWN = PermissibleValue(
        text="UNKNOWN",
        description="Severity has not been assessed or is unavailable.")

    _defn = EnumDefinition(
        name="ImpactSeverity",
        description="CVSS qualitative severity rating.",
    )

# Slots
class slots:
    pass

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

slots.catalog_version = Slot(uri=KEV_CATALOG.catalog_version, name="catalog_version", curie=KEV_CATALOG.curie('catalog_version'),
                   model_uri=KEV_CATALOG.catalog_version, domain=None, range=Optional[str])

slots.date_released = Slot(uri=KEV_CATALOG.date_released, name="date_released", curie=KEV_CATALOG.curie('date_released'),
                   model_uri=KEV_CATALOG.date_released, domain=None, range=Optional[str])

slots.count = Slot(uri=KEV_CATALOG.count, name="count", curie=KEV_CATALOG.curie('count'),
                   model_uri=KEV_CATALOG.count, domain=None, range=Optional[int])

slots.vulnerabilities = Slot(uri=KEV_CATALOG.vulnerabilities, name="vulnerabilities", curie=KEV_CATALOG.curie('vulnerabilities'),
                   model_uri=KEV_CATALOG.vulnerabilities, domain=None, range=Optional[Union[dict[Union[str, KevEntryCveId], Union[dict, KevEntry]], list[Union[dict, KevEntry]]]])

slots.cve_id = Slot(uri=DCT.identifier, name="cve_id", curie=DCT.curie('identifier'),
                   model_uri=KEV_CATALOG.cve_id, domain=None, range=URIRef)

slots.title = Slot(uri=DCT.title, name="title", curie=DCT.curie('title'),
                   model_uri=KEV_CATALOG.title, domain=None, range=Optional[str])

slots.description = Slot(uri=DCT.description, name="description", curie=DCT.curie('description'),
                   model_uri=KEV_CATALOG.description, domain=None, range=Optional[str])

slots.published_date = Slot(uri=DCT.created, name="published_date", curie=DCT.curie('created'),
                   model_uri=KEV_CATALOG.published_date, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.last_modified_date = Slot(uri=DCT.modified, name="last_modified_date", curie=DCT.curie('modified'),
                   model_uri=KEV_CATALOG.last_modified_date, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.products = Slot(uri=CORE.products, name="products", curie=CORE.curie('products'),
                   model_uri=KEV_CATALOG.products, domain=None, range=Optional[Union[Union[dict, Product], list[Union[dict, Product]]]])

slots.weaknesses = Slot(uri=CORE.weaknesses, name="weaknesses", curie=CORE.curie('weaknesses'),
                   model_uri=KEV_CATALOG.weaknesses, domain=None, range=Optional[Union[Union[dict, Weakness], list[Union[dict, Weakness]]]])

slots.references = Slot(uri=CORE.references, name="references", curie=CORE.curie('references'),
                   model_uri=KEV_CATALOG.references, domain=None, range=Optional[Union[Union[dict, Reference], list[Union[dict, Reference]]]])

slots.impact = Slot(uri=CORE.impact, name="impact", curie=CORE.curie('impact'),
                   model_uri=KEV_CATALOG.impact, domain=None, range=Optional[Union[dict, Impact]])

slots.status = Slot(uri=CORE.status, name="status", curie=CORE.curie('status'),
                   model_uri=KEV_CATALOG.status, domain=None, range=Optional[Union[str, "VulnerabilityStatus"]])

slots.vendor = Slot(uri=SCHEMA.name, name="vendor", curie=SCHEMA.curie('name'),
                   model_uri=KEV_CATALOG.vendor, domain=None, range=Optional[str])

slots.name = Slot(uri=RDFS.label, name="name", curie=RDFS.curie('label'),
                   model_uri=KEV_CATALOG.name, domain=None, range=Optional[str])

slots.version = Slot(uri=SCHEMA.version, name="version", curie=SCHEMA.curie('version'),
                   model_uri=KEV_CATALOG.version, domain=None, range=Optional[str])

slots.platforms = Slot(uri=CORE.platforms, name="platforms", curie=CORE.curie('platforms'),
                   model_uri=KEV_CATALOG.platforms, domain=None, range=Optional[Union[str, list[str]]])

slots.url = Slot(uri=SCHEMA.url, name="url", curie=SCHEMA.curie('url'),
                   model_uri=KEV_CATALOG.url, domain=None, range=Optional[Union[str, URI]])

slots.source = Slot(uri=DCT.source, name="source", curie=DCT.curie('source'),
                   model_uri=KEV_CATALOG.source, domain=None, range=Optional[str])

slots.cwe_id = Slot(uri=DCT.identifier, name="cwe_id", curie=DCT.curie('identifier'),
                   model_uri=KEV_CATALOG.cwe_id, domain=None, range=Optional[str])

slots.severity = Slot(uri=CORE.severity, name="severity", curie=CORE.curie('severity'),
                   model_uri=KEV_CATALOG.severity, domain=None, range=Optional[Union[str, "ImpactSeverity"]])

slots.vector = Slot(uri=CORE.vector, name="vector", curie=CORE.curie('vector'),
                   model_uri=KEV_CATALOG.vector, domain=None, range=Optional[str])

slots.score = Slot(uri=CORE.score, name="score", curie=CORE.curie('score'),
                   model_uri=KEV_CATALOG.score, domain=None, range=Optional[float])

slots.cpe_uri = Slot(uri=CORE.cpe_uri, name="cpe_uri", curie=CORE.curie('cpe_uri'),
                   model_uri=KEV_CATALOG.cpe_uri, domain=None, range=Optional[str])

slots.operator = Slot(uri=CORE.operator, name="operator", curie=CORE.curie('operator'),
                   model_uri=KEV_CATALOG.operator, domain=None, range=Optional[str])

slots.KevCatalog_title = Slot(uri=DCT.title, name="KevCatalog_title", curie=DCT.curie('title'),
                   model_uri=KEV_CATALOG.KevCatalog_title, domain=KevCatalog, range=Optional[str])

slots.Vulnerability_cve_id = Slot(uri=DCT.identifier, name="Vulnerability_cve_id", curie=DCT.curie('identifier'),
                   model_uri=KEV_CATALOG.Vulnerability_cve_id, domain=Vulnerability, range=Union[str, VulnerabilityCveId])

slots.Vulnerability_description = Slot(uri=DCT.description, name="Vulnerability_description", curie=DCT.curie('description'),
                   model_uri=KEV_CATALOG.Vulnerability_description, domain=Vulnerability, range=str)
