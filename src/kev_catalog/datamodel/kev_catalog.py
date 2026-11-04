# Auto generated from kev_catalog.yaml by pythongen.py version: 0.0.1
# Schema: kev_catalog
#
# id: https://w3id.org/lmodel/kev-catalog
# description: A LinkML model of the JSON format of the Known Exploited Vulnerabilities (KEV) catalog that the Cybersecurity and Infrastructure Security Agency (CISA) publishes. CISA's keys and values are the schema's, so a real KEV file validates unchanged.
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

from linkml_runtime.linkml_model.types import Date, Datetime, Integer, String
from linkml_runtime.utils.metamodelcore import XSDDate, XSDDateTime

metamodel_version = "1.12.0"
version = "2026-09-17"

# Namespaces
CVE = CurieNamespace('cve', 'https://w3id.org/lmodel/cve/')
DCAT = CurieNamespace('dcat', 'http://www.w3.org/ns/dcat#')
DCTERMS = CurieNamespace('dcterms', 'http://purl.org/dc/terms/')
KEV_CATALOG = CurieNamespace('kev_catalog', 'https://w3id.org/lmodel/kev-catalog/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
SEPSES_CVE = CurieNamespace('sepses_cve', 'http://w3id.org/sepses/vocab/ref/cve#')
SKOS = CurieNamespace('skos', 'http://www.w3.org/2004/02/skos/core#')
SPDX3 = CurieNamespace('spdx3', 'https://spdx.org/rdf/3.0.1/terms/')
STIX = CurieNamespace('stix', 'https://w3id.org/lmodel/stix/')
WD = CurieNamespace('wd', 'http://www.wikidata.org/entity/')
WDT = CurieNamespace('wdt', 'http://www.wikidata.org/prop/direct/')
DEFAULT_ = KEV_CATALOG


# Types

# Class references
class KevVulnerabilityCveID(extended_str):
    pass


@dataclass(repr=False)
class KevCatalog(YAMLRoot):
    """
    One published release of the KEV catalog, with the entries it lists.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KEV_CATALOG["KevCatalog"]
    class_class_curie: ClassVar[str] = "kev_catalog:KevCatalog"
    class_name: ClassVar[str] = "KevCatalog"
    class_model_uri: ClassVar[URIRef] = KEV_CATALOG.KevCatalog

    catalogVersion: str = None
    dateReleased: Union[str, XSDDateTime] = None
    count: int = None
    vulnerabilities: Union[dict[Union[str, KevVulnerabilityCveID], Union[dict, "KevVulnerability"]], list[Union[dict, "KevVulnerability"]]] = empty_dict()
    title: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.catalogVersion):
            self.MissingRequiredField("catalogVersion")
        if not isinstance(self.catalogVersion, str):
            self.catalogVersion = str(self.catalogVersion)

        if self._is_empty(self.dateReleased):
            self.MissingRequiredField("dateReleased")
        if not isinstance(self.dateReleased, XSDDateTime):
            self.dateReleased = XSDDateTime(self.dateReleased)

        if self._is_empty(self.count):
            self.MissingRequiredField("count")
        if not isinstance(self.count, int):
            self.count = int(self.count)

        if self._is_empty(self.vulnerabilities):
            self.MissingRequiredField("vulnerabilities")
        self._normalize_inlined_as_list(slot_name="vulnerabilities", slot_type=KevVulnerability, key_name="cveID", keyed=True)

        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class KevVulnerability(YAMLRoot):
    """
    One entry of the KEV catalog, naming a CVE that CISA lists as exploited and the action it asks for by a due date.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KEV_CATALOG["KevVulnerability"]
    class_class_curie: ClassVar[str] = "kev_catalog:KevVulnerability"
    class_name: ClassVar[str] = "KevVulnerability"
    class_model_uri: ClassVar[URIRef] = KEV_CATALOG.KevVulnerability

    cveID: Union[str, KevVulnerabilityCveID] = None
    vendorProject: str = None
    product: str = None
    vulnerabilityName: str = None
    dateAdded: Union[str, XSDDate] = None
    shortDescription: str = None
    requiredAction: str = None
    dueDate: Union[str, XSDDate] = None
    knownRansomwareCampaignUse: Optional[Union[str, "KevRansomwareCampaignUse"]] = None
    forensicTriage: Optional[Union[str, "KevForensicTriage"]] = None
    notes: Optional[str] = None
    cwes: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.cveID):
            self.MissingRequiredField("cveID")
        if not isinstance(self.cveID, KevVulnerabilityCveID):
            self.cveID = KevVulnerabilityCveID(self.cveID)

        if self._is_empty(self.vendorProject):
            self.MissingRequiredField("vendorProject")
        if not isinstance(self.vendorProject, str):
            self.vendorProject = str(self.vendorProject)

        if self._is_empty(self.product):
            self.MissingRequiredField("product")
        if not isinstance(self.product, str):
            self.product = str(self.product)

        if self._is_empty(self.vulnerabilityName):
            self.MissingRequiredField("vulnerabilityName")
        if not isinstance(self.vulnerabilityName, str):
            self.vulnerabilityName = str(self.vulnerabilityName)

        if self._is_empty(self.dateAdded):
            self.MissingRequiredField("dateAdded")
        if not isinstance(self.dateAdded, XSDDate):
            self.dateAdded = XSDDate(self.dateAdded)

        if self._is_empty(self.shortDescription):
            self.MissingRequiredField("shortDescription")
        if not isinstance(self.shortDescription, str):
            self.shortDescription = str(self.shortDescription)

        if self._is_empty(self.requiredAction):
            self.MissingRequiredField("requiredAction")
        if not isinstance(self.requiredAction, str):
            self.requiredAction = str(self.requiredAction)

        if self._is_empty(self.dueDate):
            self.MissingRequiredField("dueDate")
        if not isinstance(self.dueDate, XSDDate):
            self.dueDate = XSDDate(self.dueDate)

        if self.knownRansomwareCampaignUse is not None and not isinstance(self.knownRansomwareCampaignUse, KevRansomwareCampaignUse):
            self.knownRansomwareCampaignUse = KevRansomwareCampaignUse(self.knownRansomwareCampaignUse)

        if self.forensicTriage is not None and not isinstance(self.forensicTriage, KevForensicTriage):
            self.forensicTriage = KevForensicTriage(self.forensicTriage)

        if self.notes is not None and not isinstance(self.notes, str):
            self.notes = str(self.notes)

        if not isinstance(self.cwes, list):
            self.cwes = [self.cwes] if self.cwes is not None else []
        self.cwes = [v if isinstance(v, str) else str(v) for v in self.cwes]

        super().__post_init__(**kwargs)


# Enumerations
class KevRansomwareCampaignUse(EnumDefinitionImpl):
    """
    What CISA can say about a vulnerability's use in ransomware campaigns.
    """
    Known = PermissibleValue(
        text="Known",
        description="CISA knows of a ransomware campaign that has used it.")
    Unknown = PermissibleValue(
        text="Unknown",
        description="CISA has no confirmation that a ransomware campaign has used it.")

    _defn = EnumDefinition(
        name="KevRansomwareCampaignUse",
        description="What CISA can say about a vulnerability's use in ransomware campaigns.",
    )

class KevForensicTriage(EnumDefinitionImpl):
    """
    Whether BOD 26-04 calls for forensic triage of a vulnerability.
    """
    Yes = PermissibleValue(
        text="Yes",
        description="The directive calls for forensic triage of this vulnerability.")
    No = PermissibleValue(
        text="No",
        description="The directive does not call for forensic triage of this vulnerability.")

    _defn = EnumDefinition(
        name="KevForensicTriage",
        description="Whether BOD 26-04 calls for forensic triage of a vulnerability.",
    )

# Slots
class slots:
    pass

slots.title = Slot(uri=KEV_CATALOG.title, name="title", curie=KEV_CATALOG.curie('title'),
                   model_uri=KEV_CATALOG.title, domain=None, range=Optional[str])

slots.catalogVersion = Slot(uri=KEV_CATALOG.catalogVersion, name="catalogVersion", curie=KEV_CATALOG.curie('catalogVersion'),
                   model_uri=KEV_CATALOG.catalogVersion, domain=None, range=str)

slots.dateReleased = Slot(uri=KEV_CATALOG.dateReleased, name="dateReleased", curie=KEV_CATALOG.curie('dateReleased'),
                   model_uri=KEV_CATALOG.dateReleased, domain=None, range=Union[str, XSDDateTime])

slots.count = Slot(uri=KEV_CATALOG.count, name="count", curie=KEV_CATALOG.curie('count'),
                   model_uri=KEV_CATALOG.count, domain=None, range=int)

slots.vulnerabilities = Slot(uri=KEV_CATALOG.vulnerabilities, name="vulnerabilities", curie=KEV_CATALOG.curie('vulnerabilities'),
                   model_uri=KEV_CATALOG.vulnerabilities, domain=None, range=Union[dict[Union[str, KevVulnerabilityCveID], Union[dict, KevVulnerability]], list[Union[dict, KevVulnerability]]])

slots.cveID = Slot(uri=KEV_CATALOG.cveID, name="cveID", curie=KEV_CATALOG.curie('cveID'),
                   model_uri=KEV_CATALOG.cveID, domain=None, range=URIRef,
                   pattern=re.compile(r'^CVE-[0-9]{4}-[0-9]{4,19}$'))

slots.vendorProject = Slot(uri=KEV_CATALOG.vendorProject, name="vendorProject", curie=KEV_CATALOG.curie('vendorProject'),
                   model_uri=KEV_CATALOG.vendorProject, domain=None, range=str)

slots.product = Slot(uri=KEV_CATALOG.product, name="product", curie=KEV_CATALOG.curie('product'),
                   model_uri=KEV_CATALOG.product, domain=None, range=str)

slots.vulnerabilityName = Slot(uri=KEV_CATALOG.vulnerabilityName, name="vulnerabilityName", curie=KEV_CATALOG.curie('vulnerabilityName'),
                   model_uri=KEV_CATALOG.vulnerabilityName, domain=None, range=str)

slots.dateAdded = Slot(uri=KEV_CATALOG.dateAdded, name="dateAdded", curie=KEV_CATALOG.curie('dateAdded'),
                   model_uri=KEV_CATALOG.dateAdded, domain=None, range=Union[str, XSDDate])

slots.shortDescription = Slot(uri=KEV_CATALOG.shortDescription, name="shortDescription", curie=KEV_CATALOG.curie('shortDescription'),
                   model_uri=KEV_CATALOG.shortDescription, domain=None, range=str)

slots.requiredAction = Slot(uri=KEV_CATALOG.requiredAction, name="requiredAction", curie=KEV_CATALOG.curie('requiredAction'),
                   model_uri=KEV_CATALOG.requiredAction, domain=None, range=str)

slots.dueDate = Slot(uri=KEV_CATALOG.dueDate, name="dueDate", curie=KEV_CATALOG.curie('dueDate'),
                   model_uri=KEV_CATALOG.dueDate, domain=None, range=Union[str, XSDDate])

slots.knownRansomwareCampaignUse = Slot(uri=KEV_CATALOG.knownRansomwareCampaignUse, name="knownRansomwareCampaignUse", curie=KEV_CATALOG.curie('knownRansomwareCampaignUse'),
                   model_uri=KEV_CATALOG.knownRansomwareCampaignUse, domain=None, range=Optional[Union[str, "KevRansomwareCampaignUse"]])

slots.forensicTriage = Slot(uri=KEV_CATALOG.forensicTriage, name="forensicTriage", curie=KEV_CATALOG.curie('forensicTriage'),
                   model_uri=KEV_CATALOG.forensicTriage, domain=None, range=Optional[Union[str, "KevForensicTriage"]])

slots.notes = Slot(uri=KEV_CATALOG.notes, name="notes", curie=KEV_CATALOG.curie('notes'),
                   model_uri=KEV_CATALOG.notes, domain=None, range=Optional[str])

slots.cwes = Slot(uri=KEV_CATALOG.cwes, name="cwes", curie=KEV_CATALOG.curie('cwes'),
                   model_uri=KEV_CATALOG.cwes, domain=None, range=Optional[Union[str, list[str]]],
                   pattern=re.compile(r'^CWE-([0-9])+$'))
