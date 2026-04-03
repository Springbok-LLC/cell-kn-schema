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


metamodel_version = "None"
version = "None"


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

    @model_serializer(mode='wrap', when_used='unless-none')
    def treat_empty_lists_as_none(
            self, handler: SerializerFunctionWrapHandler,
            info: SerializationInfo) -> dict[str, Any]:
        if info.exclude_none:
            _instance = self.model_copy()
            for field, field_info in type(_instance).model_fields.items():
                if getattr(_instance, field) == [] and not(
                        field_info.is_required()):
                    setattr(_instance, field, None)
        else:
            _instance = self
        return handler(_instance, info)



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


linkml_meta = LinkMLMeta({'default_prefix': 'nlm-ckn',
     'description': 'Data model for cell phenotypes and biological entities they '
                    'relate to.',
     'id': 'https://w3id.org/nlm-ckn-schema',
     'imports': ['linkml:types'],
     'name': 'nlm-ckn-schema',
     'prefixes': {'CHEBI': {'prefix_prefix': 'CHEBI',
                            'prefix_reference': 'https://purl.obolibrary.org/obo/CHEBI_'},
                  'CL': {'prefix_prefix': 'CL',
                         'prefix_reference': 'https://purl.obolibrary.org/obo/CL_'},
                  'DRON': {'prefix_prefix': 'DRON',
                           'prefix_reference': 'https://purl.obolibrary.org/obo/DRON_'},
                  'GO': {'prefix_prefix': 'GO',
                         'prefix_reference': 'https://purl.obolibrary.org/obo/GO_'},
                  'HP': {'prefix_prefix': 'HP',
                         'prefix_reference': 'https://purl.obolibrary.org/obo/HP_'},
                  'HsapDv': {'prefix_prefix': 'HsapDv',
                             'prefix_reference': 'https://purl.obolibrary.org/obo/HsapDv_'},
                  'IAO': {'prefix_prefix': 'IAO',
                          'prefix_reference': 'https://purl.obolibrary.org/obo/IAO_'},
                  'MONDO': {'prefix_prefix': 'MONDO',
                            'prefix_reference': 'https://purl.obolibrary.org/obo/MONDO_'},
                  'NCBITaxon': {'prefix_prefix': 'NCBITaxon',
                                'prefix_reference': 'https://purl.obolibrary.org/obo/NCBITaxon_'},
                  'OBI': {'prefix_prefix': 'OBI',
                          'prefix_reference': 'https://purl.obolibrary.org/obo/OBI_'},
                  'OPMI': {'prefix_prefix': 'OPMI',
                           'prefix_reference': 'https://purl.obolibrary.org/obo/OPMI_'},
                  'PATO': {'prefix_prefix': 'PATO',
                           'prefix_reference': 'https://purl.obolibrary.org/obo/PATO_'},
                  'PR': {'prefix_prefix': 'PR',
                         'prefix_reference': 'https://purl.obolibrary.org/obo/PR_'},
                  'SO': {'prefix_prefix': 'SO',
                         'prefix_reference': 'https://purl.obolibrary.org/obo/SO_'},
                  'UBERON': {'prefix_prefix': 'UBERON',
                             'prefix_reference': 'https://purl.obolibrary.org/obo/UBERON_'},
                  'foaf': {'prefix_prefix': 'foaf',
                           'prefix_reference': 'http://xmlns.com/foaf/0.1/'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'nlm-ckn': {'prefix_prefix': 'nlm-ckn',
                              'prefix_reference': 'https://w3id.org/nlm-ckn-schema'},
                  'obo': {'prefix_prefix': 'obo',
                          'prefix_reference': 'http://www.geneontology.org/formats/oboInOwl#'},
                  'rdfs': {'prefix_prefix': 'rdfs',
                           'prefix_reference': 'http://www.w3.org/2000/01/rdf-schema#'},
                  'xsd': {'prefix_prefix': 'xsd',
                          'prefix_reference': 'http://www.w3.org/2001/XMLSchema#'}},
     'source_file': 'ckn-schema.yaml',
     'types': {'doi': {'from_schema': 'https://w3id.org/nlm-ckn-schema',
                       'name': 'doi',
                       'typeof': 'uriorcurie',
                       'uri': 'xsd:anyURI'},
               'https identifier': {'from_schema': 'https://w3id.org/nlm-ckn-schema',
                                    'name': 'https identifier',
                                    'typeof': 'string'}}} )


class Association(ConfiguredBaseModel):
    """
    A typed association between two entities, linked by a predicate.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'defining_slots': ['subject', 'predicate', 'object'],
         'from_schema': 'https://w3id.org/nlm-ckn-schema'})

    subject: Optional[str] = Field(default=None, description="""The subject of a triple.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })
    predicate: Optional[str] = Field(default=None, description="""The predicate of a triple.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })
    object: Optional[str] = Field(default=None, description="""The object of a triple.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })


class CellSet(ConfiguredBaseModel):
    """
    A collection of cells that have some common property.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/nlm-ckn-schema',
         'slot_usage': {'ontology_purl': {'name': 'ontology_purl',
                                          'range': 'CellType'}}})

    author_cell_term: Optional[str] = Field(default=None, description="""A label for a cell set that was assigned to it by some author of the dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellSet']} })
    assay: Optional[str] = Field(default=None, description="""A planned process that has the objective to produce information about a material entity (the evaluant) by examining it.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellSet'],
         'examples': [{'value': "10x 5' v1, EFO:0011025"}],
         'slot_uri': 'OBI:0000070'} })
    ontology_purl: Optional[CellType] = Field(default=None, description="""A Uniform Resource Locator that redirects to an ontology resource.""", json_schema_extra = { "linkml_meta": {'abstract': True,
         'domain_of': ['CellSet',
                       'CellType',
                       'AnatomicalStructure',
                       'Species',
                       'Disease',
                       'BiologicalProcess',
                       'CellularComponent',
                       'MolecularFunction',
                       'LifeCycleStage',
                       'ChemicalEntity',
                       'OrganismTrait',
                       'VariantConsequence']} })
    anatomical_structure: Optional[str] = Field(default=None, description="""Material anatomical entity that is a single connected structure with inherent 3D shape generated by coordinated expression of the organism's own genome.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellSet', 'CellSetDataset'],
         'examples': [{'value': 'UBERON:0000006'}],
         'slot_uri': 'UBERON:0001062'} })
    species: Optional[str] = Field(default=None, description="""The taxonomical classification of an organism.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellSet', 'Gene', 'CellSetDataset', 'Protein'],
         'examples': [{'value': 'NCBITaxon:10090'}],
         'slot_uri': 'NCBITaxon:131567'} })
    publication: Optional[str] = Field(default=None, description="""A textual entity intended to identify a particular publication.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellSet', 'CellSetDataset'], 'slot_uri': 'IAO:0000301'} })
    dataset_name: Optional[str] = Field(default=None, description="""The label for a dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellSet', 'CellSetDataset'], 'is_a': 'label'} })
    cell_count: Optional[int] = Field(default=None, description="""A count of all cells within a material entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellSet', 'CellSetDataset'], 'examples': [{'value': '31497'}]} })
    biomarker_combination: Optional[str] = Field(default=None, description="""A collection of biological entities that together can be used to identify some entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellSet'], 'examples': [{'value': '[CCL21]'}]} })
    binary_gene_set: Optional[str] = Field(default=None, description="""A collection of genes that are highly expresssed in an instance of some entity (e.g., cell).""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellSet'],
         'examples': [{'value': '[TM4SF18, VPS35L, CCL21, MMRN1, SNCG, PPFIBP1, NRP2, '
                                'AKAP12, PDPN, GNG11]'}]} })
    expressed_genes: Optional[str] = Field(default=None, description="""A collection of genes that are associated with an instance of some entity (e.g., cell).""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellSet'],
         'examples': [{'value': '[CCL21, PKHD1L1, SEMA3D, LYVE1, SEMA3A, PROX1, MMRN1, '
                                'PPFIBP1, AKAP12, PDPN]'}]} })
    cellxgene_collection: Optional[str] = Field(default=None, description="""A set of multiple datasets associated with a publication.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellSet', 'CellSetDataset']} })
    cellxgene_dataset: Optional[str] = Field(default=None, description="""A datasets associated with a publication.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellSet', 'CellSetDataset'], 'is_a': 'dataset_identifier'} })
    label: Optional[str] = Field(default=None, description="""The name for an entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellSet',
                       'CellType',
                       'Gene',
                       'AnatomicalStructure',
                       'Species',
                       'Protein',
                       'Disease',
                       'BiologicalProcess',
                       'CellularComponent',
                       'MolecularFunction',
                       'LifeCycleStage',
                       'ChemicalEntity',
                       'OrganismTrait'],
         'slot_uri': 'rdfs:label'} })
    f_beta_score: Optional[float] = Field(default=None, description="""A measure of a binary classification model's accuracy that is calculated by taking the harmonic mean of precision and recall and applying weights to recall.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellSet', 'BiomarkerCombination'], 'slot_uri': 'STATO:0000663'} })
    silhouette_score: Optional[float] = Field(default=None, description="""A measure of clustering quality that quantifies how similar an object is to its own cluster compared to other clusters, ranging from -1 to 1.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellSet']} })


class CellType(ConfiguredBaseModel):
    """
    A material entity of anatomical origin (part of or deriving from an organism) that has as its parts a maximally connected cell compartment surrounded by a plasma membrane.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'CL:0000000',
         'from_schema': 'https://w3id.org/nlm-ckn-schema',
         'slot_usage': {'ontology_purl': {'name': 'ontology_purl',
                                          'pattern': 'CL:[0-9]{7}'}}})

    label: Optional[str] = Field(default=None, description="""The name for an entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellSet',
                       'CellType',
                       'Gene',
                       'AnatomicalStructure',
                       'Species',
                       'Protein',
                       'Disease',
                       'BiologicalProcess',
                       'CellularComponent',
                       'MolecularFunction',
                       'LifeCycleStage',
                       'ChemicalEntity',
                       'OrganismTrait'],
         'slot_uri': 'rdfs:label'} })
    definition: Optional[str] = Field(default=None, description="""The official description of something that explains its meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellType',
                       'Disease',
                       'BiologicalProcess',
                       'CellularComponent',
                       'MolecularFunction',
                       'LifeCycleStage',
                       'OrganismTrait'],
         'slot_uri': 'IAO:0000115'} })
    exact_synonym: Optional[str] = Field(default=None, description="""An alternative name for an entity that has the exact same meaning as the preferred or primary label.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellType', 'Drug', 'AnatomicalStructure', 'Disease'],
         'slot_uri': 'obo:hasExactSynonym'} })
    related_synonym: Optional[str] = Field(default=None, description="""An alternative name for an entity that has a related meaning to the preferred or primary label.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellType', 'Disease'], 'slot_uri': 'obo:hasRelatedSynonym'} })
    database_cross_reference: Optional[str] = Field(default=None, description="""An annotation property that links an ontology entity or a statement to a prefixed identifier or URI.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellType', 'AnatomicalStructure', 'Species', 'Disease'],
         'slot_uri': 'obo:hasDbXref'} })
    ontology_purl: Optional[str] = Field(default=None, description="""A Uniform Resource Locator that redirects to an ontology resource.""", json_schema_extra = { "linkml_meta": {'abstract': True,
         'domain_of': ['CellSet',
                       'CellType',
                       'AnatomicalStructure',
                       'Species',
                       'Disease',
                       'BiologicalProcess',
                       'CellularComponent',
                       'MolecularFunction',
                       'LifeCycleStage',
                       'ChemicalEntity',
                       'OrganismTrait',
                       'VariantConsequence']} })
    biological_process: Optional[str] = Field(default=None, description="""A biological process is the execution of a genetically-encoded biological module or program. It consists of all the steps required to achieve the specific biological objective of the module. A biological process is accomplished by a particular set of molecular functions carried out by specific gene products (or macromolecular complexes), often in a highly regulated manner and in a particular temporal sequence.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellType'],
         'examples': [{'value': 'GO:0040016'}],
         'slot_uri': 'GO:0008150'} })

    @field_validator('ontology_purl')
    def pattern_ontology_purl(cls, v):
        pattern=re.compile(r"CL:[0-9]{7}")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid ontology_purl format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid ontology_purl format: {v}"
            raise ValueError(err_msg)
        return v


class Gene(ConfiguredBaseModel):
    """
    A region (or regions) that includes all of the sequence elements necessary to encode a functional transcript. A gene may include regulatory regions, transcribed regions and/or other functional sequence regions.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Gene Symbol'],
         'class_uri': 'SO:0000704',
         'from_schema': 'https://w3id.org/nlm-ckn-schema',
         'slot_usage': {'gene_symbol': {'name': 'gene_symbol', 'required': True}}})

    gene_symbol: str = Field(default=..., description="""A unique, standardized short name for a gene, often formed by the abbreviation of the gene name, that is assigned by the HUGO Gene Nomenclature Committee (HGNC).""", json_schema_extra = { "linkml_meta": {'domain_of': ['Gene', 'Protein'], 'examples': [{'value': 'HSPA1B'}]} })
    label: Optional[str] = Field(default=None, description="""The name for an entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellSet',
                       'CellType',
                       'Gene',
                       'AnatomicalStructure',
                       'Species',
                       'Protein',
                       'Disease',
                       'BiologicalProcess',
                       'CellularComponent',
                       'MolecularFunction',
                       'LifeCycleStage',
                       'ChemicalEntity',
                       'OrganismTrait'],
         'slot_uri': 'rdfs:label'} })
    uniprot_id: Optional[str] = Field(default=None, description="""An identifier for a protein in Uniprot.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Gene', 'Drug', 'Protein']} })
    species: Optional[str] = Field(default=None, description="""The taxonomical classification of an organism.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellSet', 'Gene', 'CellSetDataset', 'Protein'],
         'examples': [{'value': 'NCBITaxon:10090'}],
         'slot_uri': 'NCBITaxon:131567'} })
    gene_type: Optional[str] = Field(default=None, description="""A category for genes based on whether they encode or don't encode proteins.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Gene']} })
    refseq_summary: Optional[str] = Field(default=None, description="""A description of a gene from the NIH RefSeq database.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Gene']} })
    mrna__nm__and_protein__np__sequences: Optional[str] = Field(default=None, alias="mrna_(nm)_and_protein_(np)_sequences", description="""The mRNA and protein reference sequences for a given gene.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Gene'],
         'examples': [{'value': 'NM_032119 -> NP_115495, adhesion G-protein coupled '
                                'receptor V1'}]} })
    reference_sequence_identifier: Optional[str] = Field(default=None, description="""An identifier assigned by the NIH RefSeq database to the reference sequence for a gene.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Gene', 'Mutation'],
         'examples': [{'value': 'GCF_000001405.40-RS_2025_08'}]} })
    gene_id: Optional[str] = Field(default=None, description="""A numeric identifier assigned by the NCBI Entrez Gene database.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Gene'], 'examples': [{'value': '1000'}]} })
    also_known_as: Optional[str] = Field(default=None, description="""Alternative names or aliases for an entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Gene']} })
    uniprot_name: Optional[str] = Field(default=None, description="""The protein name associated with a gene as curated by UniProt.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Gene']} })
    link_to_uniprot_id: Optional[str] = Field(default=None, description="""A URL linking to a protein record in the UniProt database.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Gene', 'Drug'],
         'examples': [{'value': 'https://www.uniprot.org/uniprot/P19022'}]} })


class Drug(ConfiguredBaseModel):
    """
    A drug product that is bearer of a clinical drug role.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Bioactive Compound'],
         'class_uri': 'DRON:00000005',
         'from_schema': 'https://w3id.org/nlm-ckn-schema'})

    drug_name: Optional[str] = Field(default=None, description="""An name for a drug compound.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Drug']} })
    disease: Optional[str] = Field(default=None, description="""A disease associated with an entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Drug']} })
    study_id: Optional[str] = Field(default=None, description="""An identifier for a research study.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Drug', 'ClinicalTrial'], 'examples': [{'value': 'NCT00494511'}]} })
    uniprot_id: Optional[str] = Field(default=None, description="""An identifier for a protein in Uniprot.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Gene', 'Drug', 'Protein']} })
    protein: Optional[str] = Field(default=None, description="""An amino acid chain that is canonically produced de novo by ribosome-mediated translation of a genetically-encoded mRNA, and any derivatives thereof.""", json_schema_extra = { "linkml_meta": {'aliases': ['protein_target'],
         'domain_of': ['Drug'],
         'examples': [{'value': 'PR:000003246'}],
         'slot_uri': 'PR:000000001'} })
    mechanism_of_action: Optional[str] = Field(default=None, description="""A drug category based on biological mechanism or pathway that a given drug acts on.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Drug']} })
    trade_names: Optional[str] = Field(default=None, description="""The names for an entity that businesses use to market their product to consumers.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Drug']} })
    exact_synonym: Optional[str] = Field(default=None, description="""An alternative name for an entity that has the exact same meaning as the preferred or primary label.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellType', 'Drug', 'AnatomicalStructure', 'Disease'],
         'slot_uri': 'obo:hasExactSynonym'} })
    approval_status: Optional[str] = Field(default=None, description="""An indication of the clinical trial phases a drug has successfully gone through.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Drug']} })
    drug_description: Optional[str] = Field(default=None, description="""A textual description of a drug product.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Drug']} })
    drug_type: Optional[str] = Field(default=None, description="""A classification of a drug based on its molecular characteristics.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Drug'], 'examples': [{'value': 'Small molecule'}]} })
    link_to_pubchem_record: Optional[str] = Field(default=None, description="""A URL linking to a compound record in the PubChem database.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Drug'],
         'examples': [{'value': 'https://pubchem.ncbi.nlm.nih.gov/compound/5090'}]} })
    link_to_uniprot_id: Optional[str] = Field(default=None, description="""A URL linking to a protein record in the UniProt database.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Gene', 'Drug'],
         'examples': [{'value': 'https://www.uniprot.org/uniprot/P19022'}]} })


class AnatomicalStructure(ConfiguredBaseModel):
    """
    Material anatomical entity that is a single connected structure with inherent 3D shape generated by coordinated expression of the organism's own genome.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'UBERON:0001062',
         'from_schema': 'https://w3id.org/nlm-ckn-schema'})

    exact_synonym: Optional[str] = Field(default=None, description="""An alternative name for an entity that has the exact same meaning as the preferred or primary label.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellType', 'Drug', 'AnatomicalStructure', 'Disease'],
         'slot_uri': 'obo:hasExactSynonym'} })
    label: Optional[str] = Field(default=None, description="""The name for an entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellSet',
                       'CellType',
                       'Gene',
                       'AnatomicalStructure',
                       'Species',
                       'Protein',
                       'Disease',
                       'BiologicalProcess',
                       'CellularComponent',
                       'MolecularFunction',
                       'LifeCycleStage',
                       'ChemicalEntity',
                       'OrganismTrait'],
         'slot_uri': 'rdfs:label'} })
    ontology_purl: Optional[str] = Field(default=None, description="""A Uniform Resource Locator that redirects to an ontology resource.""", json_schema_extra = { "linkml_meta": {'abstract': True,
         'domain_of': ['CellSet',
                       'CellType',
                       'AnatomicalStructure',
                       'Species',
                       'Disease',
                       'BiologicalProcess',
                       'CellularComponent',
                       'MolecularFunction',
                       'LifeCycleStage',
                       'ChemicalEntity',
                       'OrganismTrait',
                       'VariantConsequence']} })
    database_cross_reference: Optional[str] = Field(default=None, description="""An annotation property that links an ontology entity or a statement to a prefixed identifier or URI.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellType', 'AnatomicalStructure', 'Species', 'Disease'],
         'slot_uri': 'obo:hasDbXref'} })


class Species(ConfiguredBaseModel):
    """
    The taxonomical classification of an organism.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Taxonomy'],
         'class_uri': 'NCBITaxon:131567',
         'from_schema': 'https://w3id.org/nlm-ckn-schema'})

    ontology_purl: Optional[str] = Field(default=None, description="""A Uniform Resource Locator that redirects to an ontology resource.""", json_schema_extra = { "linkml_meta": {'abstract': True,
         'domain_of': ['CellSet',
                       'CellType',
                       'AnatomicalStructure',
                       'Species',
                       'Disease',
                       'BiologicalProcess',
                       'CellularComponent',
                       'MolecularFunction',
                       'LifeCycleStage',
                       'ChemicalEntity',
                       'OrganismTrait',
                       'VariantConsequence']} })
    label: Optional[str] = Field(default=None, description="""The name for an entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellSet',
                       'CellType',
                       'Gene',
                       'AnatomicalStructure',
                       'Species',
                       'Protein',
                       'Disease',
                       'BiologicalProcess',
                       'CellularComponent',
                       'MolecularFunction',
                       'LifeCycleStage',
                       'ChemicalEntity',
                       'OrganismTrait'],
         'slot_uri': 'rdfs:label'} })
    database_cross_reference: Optional[str] = Field(default=None, description="""An annotation property that links an ontology entity or a statement to a prefixed identifier or URI.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellType', 'AnatomicalStructure', 'Species', 'Disease'],
         'slot_uri': 'obo:hasDbXref'} })


class CellSetDataset(ConfiguredBaseModel):
    """
    A dataset that is about cells taken from one or more tissue samples.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/nlm-ckn-schema'})

    dataset_name: Optional[str] = Field(default=None, description="""The label for a dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellSet', 'CellSetDataset'], 'is_a': 'label'} })
    dataset_identifier: Optional[str] = Field(default=None, description="""An identifier for a data set.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellSetDataset'],
         'examples': [{'value': 'e51bae9a-c747-4b64-904a-4da7cda218ab'}]} })
    species: Optional[str] = Field(default=None, description="""The taxonomical classification of an organism.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellSet', 'Gene', 'CellSetDataset', 'Protein'],
         'examples': [{'value': 'NCBITaxon:10090'}],
         'slot_uri': 'NCBITaxon:131567'} })
    version: Optional[str] = Field(default=None, description="""An information content entity which is a sequence of characters borne by part of each of a class of manufactured products or its packaging and indicates its order within a set of other products having the same name.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellSetDataset'],
         'examples': [{'value': 'v0.1'}],
         'slot_uri': 'IAO:0000129'} })
    dataset_collection_version: Optional[str] = Field(default=None, description="""The version number for a data set collection.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellSetDataset'],
         'examples': [{'value': '2fd47593-5bcb-4b07-878f-263ad03f2206'}],
         'is_a': 'version'} })
    publication: Optional[str] = Field(default=None, description="""A textual entity intended to identify a particular publication.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellSet', 'CellSetDataset'], 'slot_uri': 'IAO:0000301'} })
    anatomical_structure: Optional[str] = Field(default=None, description="""Material anatomical entity that is a single connected structure with inherent 3D shape generated by coordinated expression of the organism's own genome.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellSet', 'CellSetDataset'],
         'examples': [{'value': 'UBERON:0000006'}],
         'slot_uri': 'UBERON:0001062'} })
    disease_status: Optional[str] = Field(default=None, description="""The name of the disease the donor organism had. If it was healthy, then the default value is 'normal'.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellSetDataset']} })
    cell_count: Optional[int] = Field(default=None, description="""A count of all cells within a material entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellSet', 'CellSetDataset'], 'examples': [{'value': '31497'}]} })
    cell_type: Optional[str] = Field(default=None, description="""A material entity of anatomical origin (part of or deriving from an organism) that has as its parts a maximally connected cell compartment surrounded by a plasma membrane.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellSetDataset'],
         'examples': [{'value': 'CL:0000095'}],
         'slot_uri': 'CL:0000000'} })
    cellxgene_collection: Optional[str] = Field(default=None, description="""A set of multiple datasets associated with a publication.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellSet', 'CellSetDataset']} })
    cellxgene_dataset: Optional[str] = Field(default=None, description="""A datasets associated with a publication.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellSet', 'CellSetDataset'], 'is_a': 'dataset_identifier'} })
    collection_id: Optional[str] = Field(default=None, description="""An identifier for a CELLxGENE collection.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellSetDataset'],
         'examples': [{'value': 'bcb61471-2a44-4c97-8c7a-26512e27ccc8'}]} })
    citation: Optional[str] = Field(default=None, description="""A formatted bibliographic reference to a publication.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellSetDataset']} })


class Publication(ConfiguredBaseModel):
    """
    A document that is the output of a publishing process.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'IAO:0000311', 'from_schema': 'https://w3id.org/nlm-ckn-schema'})

    year: Optional[str] = Field(default=None, description="""A numeric string that represents one calendar year.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Publication'], 'examples': [{'value': '2005'}]} })
    title: Optional[str] = Field(default=None, description="""A word or phrase used as a name for some entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Publication']} })
    author_list: Optional[str] = Field(default=None, description="""A list of people who contributed to a publication.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Publication'], 'slot_uri': 'IAO:0000321'} })
    pmcid: Optional[str] = Field(default=None, description="""An identifier curated by Pubmed Central for a publication.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Publication'], 'examples': [{'value': 'PMC10387117'}]} })
    pmid: Optional[str] = Field(default=None, description="""An identifier curated by Pubmed for a publication.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Publication'],
         'examples': [{'value': '37516747'}],
         'slot_uri': 'OBI:0001617'} })
    publication_doi: Optional[str] = Field(default=None, description="""An identifier for a scientific publication.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Publication'],
         'examples': [{'value': 'https://doi.org/10.1101/2025.01.17.633590'}]} })
    journal: Optional[str] = Field(default=None, description="""A shortened name for a journal.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Publication'], 'examples': [{'value': 'Nat Commun'}]} })


class BiomarkerCombination(ConfiguredBaseModel):
    """
    A cell type marker gene is a gene that is selectively expressed in cells of a given type and can be reliably used alone or in combination as a canonical characteristic to optimally classify them.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'SO:0001260', 'from_schema': 'https://w3id.org/nlm-ckn-schema'})

    markers: Optional[str] = Field(default=None, description="""A collection of biological entities that collectively characterizes a biological state or condition.""", json_schema_extra = { "linkml_meta": {'domain_of': ['BiomarkerCombination', 'BinaryGeneSet'],
         'slot_uri': 'CHEBI:59163'} })
    f_beta_score: Optional[float] = Field(default=None, description="""A measure of a binary classification model's accuracy that is calculated by taking the harmonic mean of precision and recall and applying weights to recall.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellSet', 'BiomarkerCombination'], 'slot_uri': 'STATO:0000663'} })


class Protein(ConfiguredBaseModel):
    """
    An amino acid chain that is canonically produced de novo by ribosome-mediated translation of a genetically-encoded mRNA, and any derivatives thereof.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'PR:000000001',
         'from_schema': 'https://w3id.org/nlm-ckn-schema',
         'slot_usage': {'gene_symbol': {'name': 'gene_symbol', 'required': True}}})

    comment: Optional[str] = Field(default=None, description="""One or more statements that provide additional information about a resource.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Protein'], 'slot_uri': 'rdfs:comment'} })
    label: Optional[str] = Field(default=None, description="""The name for an entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellSet',
                       'CellType',
                       'Gene',
                       'AnatomicalStructure',
                       'Species',
                       'Protein',
                       'Disease',
                       'BiologicalProcess',
                       'CellularComponent',
                       'MolecularFunction',
                       'LifeCycleStage',
                       'ChemicalEntity',
                       'OrganismTrait'],
         'slot_uri': 'rdfs:label'} })
    uniprot_id: Optional[str] = Field(default=None, description="""An identifier for a protein in Uniprot.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Gene', 'Drug', 'Protein']} })
    number_of_amino_acids: Optional[int] = Field(default=None, description="""A count of the amino acids in a protein.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Protein']} })
    protein_function: Optional[str] = Field(default=None, description="""A description of the actions carried out by a given protein.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Protein']} })
    species: Optional[str] = Field(default=None, description="""The taxonomical classification of an organism.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellSet', 'Gene', 'CellSetDataset', 'Protein'],
         'examples': [{'value': 'NCBITaxon:10090'}],
         'slot_uri': 'NCBITaxon:131567'} })
    gene_symbol: str = Field(default=..., description="""A unique, standardized short name for a gene, often formed by the abbreviation of the gene name, that is assigned by the HUGO Gene Nomenclature Committee (HGNC).""", json_schema_extra = { "linkml_meta": {'domain_of': ['Gene', 'Protein'], 'examples': [{'value': 'HSPA1B'}]} })
    annotation_score: Optional[int] = Field(default=None, description="""A score indicating the level of annotation for a protein.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Protein']} })


class Disease(ConfiguredBaseModel):
    """
    A disease is a disposition to undergo pathological processes that exists in an organism because of one or more disorders in that organism.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'MONDO:0000001', 'from_schema': 'https://w3id.org/nlm-ckn-schema'})

    label: Optional[str] = Field(default=None, description="""The name for an entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellSet',
                       'CellType',
                       'Gene',
                       'AnatomicalStructure',
                       'Species',
                       'Protein',
                       'Disease',
                       'BiologicalProcess',
                       'CellularComponent',
                       'MolecularFunction',
                       'LifeCycleStage',
                       'ChemicalEntity',
                       'OrganismTrait'],
         'slot_uri': 'rdfs:label'} })
    definition: Optional[str] = Field(default=None, description="""The official description of something that explains its meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellType',
                       'Disease',
                       'BiologicalProcess',
                       'CellularComponent',
                       'MolecularFunction',
                       'LifeCycleStage',
                       'OrganismTrait'],
         'slot_uri': 'IAO:0000115'} })
    exact_synonym: Optional[str] = Field(default=None, description="""An alternative name for an entity that has the exact same meaning as the preferred or primary label.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellType', 'Drug', 'AnatomicalStructure', 'Disease'],
         'slot_uri': 'obo:hasExactSynonym'} })
    related_synonym: Optional[str] = Field(default=None, description="""An alternative name for an entity that has a related meaning to the preferred or primary label.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellType', 'Disease'], 'slot_uri': 'obo:hasRelatedSynonym'} })
    ontology_purl: Optional[str] = Field(default=None, description="""A Uniform Resource Locator that redirects to an ontology resource.""", json_schema_extra = { "linkml_meta": {'abstract': True,
         'domain_of': ['CellSet',
                       'CellType',
                       'AnatomicalStructure',
                       'Species',
                       'Disease',
                       'BiologicalProcess',
                       'CellularComponent',
                       'MolecularFunction',
                       'LifeCycleStage',
                       'ChemicalEntity',
                       'OrganismTrait',
                       'VariantConsequence']} })
    database_cross_reference: Optional[str] = Field(default=None, description="""An annotation property that links an ontology entity or a statement to a prefixed identifier or URI.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellType', 'AnatomicalStructure', 'Species', 'Disease'],
         'slot_uri': 'obo:hasDbXref'} })


class BinaryGeneSet(ConfiguredBaseModel):
    """
    A collection of discontinuous sequences.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'SO:0001260', 'from_schema': 'https://w3id.org/nlm-ckn-schema'})

    markers: Optional[str] = Field(default=None, description="""A collection of biological entities that collectively characterizes a biological state or condition.""", json_schema_extra = { "linkml_meta": {'domain_of': ['BiomarkerCombination', 'BinaryGeneSet'],
         'slot_uri': 'CHEBI:59163'} })


class ClinicalTrial(ConfiguredBaseModel):
    """
    A clinical investigation that involves an intervention.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'OBI:0003699', 'from_schema': 'https://w3id.org/nlm-ckn-schema'})

    study_id: Optional[str] = Field(default=None, description="""An identifier for a research study.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Drug', 'ClinicalTrial'], 'examples': [{'value': 'NCT00494511'}]} })


class BiologicalProcess(ConfiguredBaseModel):
    """
    A biological process is the execution of a genetically-encoded biological module or program. It consists of all the steps required to achieve the specific biological objective of the module. A biological process is accomplished by a particular set of molecular functions carried out by specific gene products (or macromolecular complexes), often in a highly regulated manner and in a particular temporal sequence.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'GO:0008150', 'from_schema': 'https://w3id.org/nlm-ckn-schema'})

    ontology_purl: Optional[str] = Field(default=None, description="""A Uniform Resource Locator that redirects to an ontology resource.""", json_schema_extra = { "linkml_meta": {'abstract': True,
         'domain_of': ['CellSet',
                       'CellType',
                       'AnatomicalStructure',
                       'Species',
                       'Disease',
                       'BiologicalProcess',
                       'CellularComponent',
                       'MolecularFunction',
                       'LifeCycleStage',
                       'ChemicalEntity',
                       'OrganismTrait',
                       'VariantConsequence']} })
    label: Optional[str] = Field(default=None, description="""The name for an entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellSet',
                       'CellType',
                       'Gene',
                       'AnatomicalStructure',
                       'Species',
                       'Protein',
                       'Disease',
                       'BiologicalProcess',
                       'CellularComponent',
                       'MolecularFunction',
                       'LifeCycleStage',
                       'ChemicalEntity',
                       'OrganismTrait'],
         'slot_uri': 'rdfs:label'} })
    definition: Optional[str] = Field(default=None, description="""The official description of something that explains its meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellType',
                       'Disease',
                       'BiologicalProcess',
                       'CellularComponent',
                       'MolecularFunction',
                       'LifeCycleStage',
                       'OrganismTrait'],
         'slot_uri': 'IAO:0000115'} })


class CellularComponent(ConfiguredBaseModel):
    """
    A location, relative to cellular compartments and structures, occupied by a macromolecular machine. There are three types of cellular components described in the gene ontology: (1) the cellular anatomical entity where a gene product carries out a molecular function (e.g., plasma membrane, cytoskeleton) or membrane-enclosed compartments (e.g., mitochondrion); (2)virion components, where viral proteins act, and (3) the stable macromolecular complexes of which gene product are parts (e.g., the clathrin complex).
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'GO:0005575', 'from_schema': 'https://w3id.org/nlm-ckn-schema'})

    ontology_purl: Optional[str] = Field(default=None, description="""A Uniform Resource Locator that redirects to an ontology resource.""", json_schema_extra = { "linkml_meta": {'abstract': True,
         'domain_of': ['CellSet',
                       'CellType',
                       'AnatomicalStructure',
                       'Species',
                       'Disease',
                       'BiologicalProcess',
                       'CellularComponent',
                       'MolecularFunction',
                       'LifeCycleStage',
                       'ChemicalEntity',
                       'OrganismTrait',
                       'VariantConsequence']} })
    label: Optional[str] = Field(default=None, description="""The name for an entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellSet',
                       'CellType',
                       'Gene',
                       'AnatomicalStructure',
                       'Species',
                       'Protein',
                       'Disease',
                       'BiologicalProcess',
                       'CellularComponent',
                       'MolecularFunction',
                       'LifeCycleStage',
                       'ChemicalEntity',
                       'OrganismTrait'],
         'slot_uri': 'rdfs:label'} })
    definition: Optional[str] = Field(default=None, description="""The official description of something that explains its meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellType',
                       'Disease',
                       'BiologicalProcess',
                       'CellularComponent',
                       'MolecularFunction',
                       'LifeCycleStage',
                       'OrganismTrait'],
         'slot_uri': 'IAO:0000115'} })


class MolecularFunction(ConfiguredBaseModel):
    """
    A molecular process that can be carried out by the action of a single macromolecular machine, usually via direct physical interactions with other molecular entities. Function in this sense denotes an action, or activity, that a gene product (or a complex) performs.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'GO:0003674', 'from_schema': 'https://w3id.org/nlm-ckn-schema'})

    ontology_purl: Optional[str] = Field(default=None, description="""A Uniform Resource Locator that redirects to an ontology resource.""", json_schema_extra = { "linkml_meta": {'abstract': True,
         'domain_of': ['CellSet',
                       'CellType',
                       'AnatomicalStructure',
                       'Species',
                       'Disease',
                       'BiologicalProcess',
                       'CellularComponent',
                       'MolecularFunction',
                       'LifeCycleStage',
                       'ChemicalEntity',
                       'OrganismTrait',
                       'VariantConsequence']} })
    label: Optional[str] = Field(default=None, description="""The name for an entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellSet',
                       'CellType',
                       'Gene',
                       'AnatomicalStructure',
                       'Species',
                       'Protein',
                       'Disease',
                       'BiologicalProcess',
                       'CellularComponent',
                       'MolecularFunction',
                       'LifeCycleStage',
                       'ChemicalEntity',
                       'OrganismTrait'],
         'slot_uri': 'rdfs:label'} })
    definition: Optional[str] = Field(default=None, description="""The official description of something that explains its meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellType',
                       'Disease',
                       'BiologicalProcess',
                       'CellularComponent',
                       'MolecularFunction',
                       'LifeCycleStage',
                       'OrganismTrait'],
         'slot_uri': 'IAO:0000115'} })


class LifeCycleStage(ConfiguredBaseModel):
    """
    A spatiotemporal region encompassing some part of the life cycle of an organism.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'UBERON:0000105',
         'from_schema': 'https://w3id.org/nlm-ckn-schema'})

    label: Optional[str] = Field(default=None, description="""The name for an entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellSet',
                       'CellType',
                       'Gene',
                       'AnatomicalStructure',
                       'Species',
                       'Protein',
                       'Disease',
                       'BiologicalProcess',
                       'CellularComponent',
                       'MolecularFunction',
                       'LifeCycleStage',
                       'ChemicalEntity',
                       'OrganismTrait'],
         'slot_uri': 'rdfs:label'} })
    ontology_purl: Optional[str] = Field(default=None, description="""A Uniform Resource Locator that redirects to an ontology resource.""", json_schema_extra = { "linkml_meta": {'abstract': True,
         'domain_of': ['CellSet',
                       'CellType',
                       'AnatomicalStructure',
                       'Species',
                       'Disease',
                       'BiologicalProcess',
                       'CellularComponent',
                       'MolecularFunction',
                       'LifeCycleStage',
                       'ChemicalEntity',
                       'OrganismTrait',
                       'VariantConsequence']} })
    definition: Optional[str] = Field(default=None, description="""The official description of something that explains its meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellType',
                       'Disease',
                       'BiologicalProcess',
                       'CellularComponent',
                       'MolecularFunction',
                       'LifeCycleStage',
                       'OrganismTrait'],
         'slot_uri': 'IAO:0000115'} })


class ChemicalEntity(ConfiguredBaseModel):
    """
    A chemical entity is a physical entity of interest in chemistry including molecular entities, parts thereof, and chemical substances.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Phenotype'],
         'class_uri': 'CHEBI:24431',
         'from_schema': 'https://w3id.org/nlm-ckn-schema'})

    label: Optional[str] = Field(default=None, description="""The name for an entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellSet',
                       'CellType',
                       'Gene',
                       'AnatomicalStructure',
                       'Species',
                       'Protein',
                       'Disease',
                       'BiologicalProcess',
                       'CellularComponent',
                       'MolecularFunction',
                       'LifeCycleStage',
                       'ChemicalEntity',
                       'OrganismTrait'],
         'slot_uri': 'rdfs:label'} })
    ontology_purl: Optional[str] = Field(default=None, description="""A Uniform Resource Locator that redirects to an ontology resource.""", json_schema_extra = { "linkml_meta": {'abstract': True,
         'domain_of': ['CellSet',
                       'CellType',
                       'AnatomicalStructure',
                       'Species',
                       'Disease',
                       'BiologicalProcess',
                       'CellularComponent',
                       'MolecularFunction',
                       'LifeCycleStage',
                       'ChemicalEntity',
                       'OrganismTrait',
                       'VariantConsequence']} })


class OrganismTrait(ConfiguredBaseModel):
    """
    A dependent entity that inheres in a bearer by virtue of how the bearer is related to other entities.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Phenotype'],
         'class_uri': 'PATO:0000001',
         'from_schema': 'https://w3id.org/nlm-ckn-schema'})

    label: Optional[str] = Field(default=None, description="""The name for an entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellSet',
                       'CellType',
                       'Gene',
                       'AnatomicalStructure',
                       'Species',
                       'Protein',
                       'Disease',
                       'BiologicalProcess',
                       'CellularComponent',
                       'MolecularFunction',
                       'LifeCycleStage',
                       'ChemicalEntity',
                       'OrganismTrait'],
         'slot_uri': 'rdfs:label'} })
    ontology_purl: Optional[str] = Field(default=None, description="""A Uniform Resource Locator that redirects to an ontology resource.""", json_schema_extra = { "linkml_meta": {'abstract': True,
         'domain_of': ['CellSet',
                       'CellType',
                       'AnatomicalStructure',
                       'Species',
                       'Disease',
                       'BiologicalProcess',
                       'CellularComponent',
                       'MolecularFunction',
                       'LifeCycleStage',
                       'ChemicalEntity',
                       'OrganismTrait',
                       'VariantConsequence']} })
    definition: Optional[str] = Field(default=None, description="""The official description of something that explains its meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CellType',
                       'Disease',
                       'BiologicalProcess',
                       'CellularComponent',
                       'MolecularFunction',
                       'LifeCycleStage',
                       'OrganismTrait'],
         'slot_uri': 'IAO:0000115'} })


class Mutation(ConfiguredBaseModel):
    """
    A sequence_alteration is a sequence_feature whose extent is the deviation from another sequence.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'SO:0001059', 'from_schema': 'https://w3id.org/nlm-ckn-schema'})

    reference_sequence_identifier: Optional[str] = Field(default=None, description="""An identifier assigned by the NIH RefSeq database to the reference sequence for a gene.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Gene', 'Mutation'],
         'examples': [{'value': 'GCF_000001405.40-RS_2025_08'}]} })
    genotype_id: Optional[str] = Field(default=None, description="""An identifier for a specific genotype.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Mutation']} })
    genotype: Optional[str] = Field(default=None, description="""The genetic constitution of an organism at one or more loci.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Mutation']} })
    phenotype: Optional[str] = Field(default=None, description="""An observable characteristic of an organism resulting from the interaction of its genotype with the environment.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Mutation']} })
    genotype_annotation: Optional[str] = Field(default=None, description="""A textual annotation describing the functional effect of a genotype.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Mutation']} })
    evidence_level: Optional[str] = Field(default=None, description="""A classification indicating the strength of the evidence supporting a genotype-phenotype or pharmacogenomic association.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Mutation']} })
    source: Optional[str] = Field(default=None, description="""The resource from which some information, data, or knowledge originated.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Mutation', 'ProteinLocatedInCellularComponent'],
         'slot_uri': 'dc:source'} })
    literature: Optional[str] = Field(default=None, description="""A reference to a publication or body of published work.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Mutation']} })


class VariantConsequence(ConfiguredBaseModel):
    """
    The predicted effect of a sequence variant on a gene product or genomic feature, classified using Sequence Ontology terms.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'SO:0001537', 'from_schema': 'https://w3id.org/nlm-ckn-schema'})

    ontology_purl: Optional[str] = Field(default=None, description="""A Uniform Resource Locator that redirects to an ontology resource.""", json_schema_extra = { "linkml_meta": {'abstract': True,
         'domain_of': ['CellSet',
                       'CellType',
                       'AnatomicalStructure',
                       'Species',
                       'Disease',
                       'BiologicalProcess',
                       'CellularComponent',
                       'MolecularFunction',
                       'LifeCycleStage',
                       'ChemicalEntity',
                       'OrganismTrait',
                       'VariantConsequence']} })
    variant_consequence_label: Optional[str] = Field(default=None, description="""A label describing the predicted consequence of a sequence variant.""", json_schema_extra = { "linkml_meta": {'domain_of': ['VariantConsequence'],
         'examples': [{'value': 'missense_variant'}]} })


class CellTypePartOfAnatomicalStructure(Association):
    """
    A relationship between a cell type and the anatomical structure it is part of.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'defining_slots': ['subject', 'predicate', 'object'],
         'from_schema': 'https://w3id.org/nlm-ckn-schema',
         'slot_usage': {'object': {'description': 'Material anatomical entity that is '
                                                  'a single connected structure with '
                                                  'inherent 3D shape generated by '
                                                  'coordinated expression of the '
                                                  "organism's own genome.",
                                   'name': 'object',
                                   'range': 'AnatomicalStructure'},
                        'predicate': {'description': 'A relation between a part and '
                                                     'some whole entity.',
                                      'name': 'predicate',
                                      'subproperty_of': 'part_of'},
                        'subject': {'description': 'A material entity of anatomical '
                                                   'origin (part of or deriving from '
                                                   'an organism) that has as its parts '
                                                   'a maximally connected cell '
                                                   'compartment surrounded by a plasma '
                                                   'membrane.',
                                    'name': 'subject',
                                    'range': 'CellType'}}})

    subject: Optional[CellType] = Field(default=None, description="""A material entity of anatomical origin (part of or deriving from an organism) that has as its parts a maximally connected cell compartment surrounded by a plasma membrane.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })
    predicate: Optional[str] = Field(default=None, description="""A relation between a part and some whole entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association'], 'subproperty_of': 'part_of'} })
    object: Optional[AnatomicalStructure] = Field(default=None, description="""Material anatomical entity that is a single connected structure with inherent 3D shape generated by coordinated expression of the organism's own genome.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })


class AnatomicalStructurePartOfAnatomicalStructure(Association):
    """
    A relationship between an anatomical structure and another anatomical structure it is part of.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'defining_slots': ['subject', 'predicate', 'object'],
         'from_schema': 'https://w3id.org/nlm-ckn-schema',
         'slot_usage': {'object': {'description': 'Material anatomical entity that is '
                                                  'a single connected structure with '
                                                  'inherent 3D shape generated by '
                                                  'coordinated expression of the '
                                                  "organism's own genome.",
                                   'name': 'object',
                                   'range': 'AnatomicalStructure'},
                        'predicate': {'description': 'A relation between a part and '
                                                     'some whole entity.',
                                      'name': 'predicate',
                                      'subproperty_of': 'part_of'},
                        'subject': {'description': 'Material anatomical entity that is '
                                                   'a single connected structure with '
                                                   'inherent 3D shape generated by '
                                                   'coordinated expression of the '
                                                   "organism's own genome.",
                                    'name': 'subject',
                                    'range': 'AnatomicalStructure'}}})

    subject: Optional[AnatomicalStructure] = Field(default=None, description="""Material anatomical entity that is a single connected structure with inherent 3D shape generated by coordinated expression of the organism's own genome.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })
    predicate: Optional[str] = Field(default=None, description="""A relation between a part and some whole entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association'], 'subproperty_of': 'part_of'} })
    object: Optional[AnatomicalStructure] = Field(default=None, description="""Material anatomical entity that is a single connected structure with inherent 3D shape generated by coordinated expression of the organism's own genome.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })


class CellTypeInteractsWithCellType(Association):
    """
    A relationship between two cell types that are causally connected.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'defining_slots': ['subject', 'predicate', 'object'],
         'from_schema': 'https://w3id.org/nlm-ckn-schema',
         'slot_usage': {'object': {'description': 'A material entity of anatomical '
                                                  'origin (part of or deriving from an '
                                                  'organism) that has as its parts a '
                                                  'maximally connected cell '
                                                  'compartment surrounded by a plasma '
                                                  'membrane.',
                                   'name': 'object',
                                   'range': 'CellType'},
                        'predicate': {'description': 'Symmetric relation between two '
                                                     'entities that directly bind or '
                                                     'modify the behavior of the '
                                                     'other.',
                                      'name': 'predicate',
                                      'subproperty_of': 'interacts_with'},
                        'subject': {'description': 'A material entity of anatomical '
                                                   'origin (part of or deriving from '
                                                   'an organism) that has as its parts '
                                                   'a maximally connected cell '
                                                   'compartment surrounded by a plasma '
                                                   'membrane.',
                                    'name': 'subject',
                                    'range': 'CellType'}}})

    subject: Optional[CellType] = Field(default=None, description="""A material entity of anatomical origin (part of or deriving from an organism) that has as its parts a maximally connected cell compartment surrounded by a plasma membrane.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })
    predicate: Optional[str] = Field(default=None, description="""Symmetric relation between two entities that directly bind or modify the behavior of the other.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association'], 'subproperty_of': 'interacts_with'} })
    object: Optional[CellType] = Field(default=None, description="""A material entity of anatomical origin (part of or deriving from an organism) that has as its parts a maximally connected cell compartment surrounded by a plasma membrane.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })


class CellTypeDevelopsFromCellType(Association):
    """
    A relationship between a cell type and another cell type it directly or indirectly develops from.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'defining_slots': ['subject', 'predicate', 'object'],
         'from_schema': 'https://w3id.org/nlm-ckn-schema',
         'slot_usage': {'object': {'description': 'A material entity of anatomical '
                                                  'origin (part of or deriving from an '
                                                  'organism) that has as its parts a '
                                                  'maximally connected cell '
                                                  'compartment surrounded by a plasma '
                                                  'membrane.',
                                   'name': 'object',
                                   'range': 'CellType'},
                        'predicate': {'description': 'Relation between entities x and '
                                                     'y and some process p where x is '
                                                     'the input to p and y is the '
                                                     'output of p and x is directly '
                                                     'involved in the creation of y.',
                                      'name': 'predicate',
                                      'subproperty_of': 'develops_from'},
                        'subject': {'description': 'A material entity of anatomical '
                                                   'origin (part of or deriving from '
                                                   'an organism) that has as its parts '
                                                   'a maximally connected cell '
                                                   'compartment surrounded by a plasma '
                                                   'membrane.',
                                    'name': 'subject',
                                    'range': 'CellType'}}})

    subject: Optional[CellType] = Field(default=None, description="""A material entity of anatomical origin (part of or deriving from an organism) that has as its parts a maximally connected cell compartment surrounded by a plasma membrane.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })
    predicate: Optional[str] = Field(default=None, description="""Relation between entities x and y and some process p where x is the input to p and y is the output of p and x is directly involved in the creation of y.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association'], 'subproperty_of': 'develops_from'} })
    object: Optional[CellType] = Field(default=None, description="""A material entity of anatomical origin (part of or deriving from an organism) that has as its parts a maximally connected cell compartment surrounded by a plasma membrane.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })


class CellTypeSubclassOfCellType(Association):
    """
    A relationship between a cell type whose instances are also instances of another cell type.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'defining_slots': ['subject', 'predicate', 'object'],
         'from_schema': 'https://w3id.org/nlm-ckn-schema',
         'slot_usage': {'object': {'description': 'A material entity of anatomical '
                                                  'origin (part of or deriving from an '
                                                  'organism) that has as its parts a '
                                                  'maximally connected cell '
                                                  'compartment surrounded by a plasma '
                                                  'membrane.',
                                   'name': 'object',
                                   'range': 'CellType'},
                        'predicate': {'description': 'Relation between x and y where '
                                                     'all instances of y are instances '
                                                     'of x.',
                                      'name': 'predicate',
                                      'subproperty_of': 'subclass_of'},
                        'subject': {'description': 'A material entity of anatomical '
                                                   'origin (part of or deriving from '
                                                   'an organism) that has as its parts '
                                                   'a maximally connected cell '
                                                   'compartment surrounded by a plasma '
                                                   'membrane.',
                                    'name': 'subject',
                                    'range': 'CellType'}}})

    subject: Optional[CellType] = Field(default=None, description="""A material entity of anatomical origin (part of or deriving from an organism) that has as its parts a maximally connected cell compartment surrounded by a plasma membrane.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })
    predicate: Optional[str] = Field(default=None, description="""Relation between x and y where all instances of y are instances of x.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association'], 'subproperty_of': 'subclass_of'} })
    object: Optional[CellType] = Field(default=None, description="""A material entity of anatomical origin (part of or deriving from an organism) that has as its parts a maximally connected cell compartment surrounded by a plasma membrane.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })


class CellTypeExpressesGene(Association):
    """
    A relationship between a cell type and a gene such that the gene is selectively expressed in that cell type and can be used as a marker.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'defining_slots': ['subject', 'predicate', 'object'],
         'from_schema': 'https://w3id.org/nlm-ckn-schema',
         'slot_usage': {'object': {'description': 'A region (or regions) that includes '
                                                  'all of the sequence elements '
                                                  'necessary to encode a functional '
                                                  'transcript. A gene may include '
                                                  'regulatory regions, transcribed '
                                                  'regions and/or other functional '
                                                  'sequence regions.',
                                   'name': 'object',
                                   'range': 'Gene'},
                        'predicate': {'description': 'A relation between a cell type '
                                                     'and a gene that is selectively '
                                                     'expressed in that cell type '
                                                     'relative to other cell types.',
                                      'name': 'predicate',
                                      'subproperty_of': 'selectively_expresses'},
                        'subject': {'description': 'A material entity of anatomical '
                                                   'origin (part of or deriving from '
                                                   'an organism) that has as its parts '
                                                   'a maximally connected cell '
                                                   'compartment surrounded by a plasma '
                                                   'membrane.',
                                    'name': 'subject',
                                    'range': 'CellType'}}})

    subject: Optional[CellType] = Field(default=None, description="""A material entity of anatomical origin (part of or deriving from an organism) that has as its parts a maximally connected cell compartment surrounded by a plasma membrane.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })
    predicate: Optional[str] = Field(default=None, description="""A relation between a cell type and a gene that is selectively expressed in that cell type relative to other cell types.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association'], 'subproperty_of': 'selectively_expresses'} })
    object: Optional[Gene] = Field(default=None, description="""A region (or regions) that includes all of the sequence elements necessary to encode a functional transcript. A gene may include regulatory regions, transcribed regions and/or other functional sequence regions.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })


class CellTypeHasPlasmaMembranePartProtein(Association):
    """
    A relationship between a cell type and a protein that is part of its plasma membrane.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'defining_slots': ['subject', 'predicate', 'object'],
         'from_schema': 'https://w3id.org/nlm-ckn-schema',
         'slot_usage': {'object': {'description': 'An amino acid chain that is '
                                                  'canonically produced de novo by '
                                                  'ribosome-mediated translation of a '
                                                  'genetically-encoded mRNA, and any '
                                                  'derivatives thereof',
                                   'name': 'object',
                                   'range': 'Protein'},
                        'predicate': {'description': 'A relation between a cell c and '
                                                     'a protein complex or protein p '
                                                     "that is part of the cell's "
                                                     'plasma membrane.',
                                      'name': 'predicate',
                                      'subproperty_of': 'has_plasma_membrane_part'},
                        'subject': {'description': 'A material entity of anatomical '
                                                   'origin (part of or deriving from '
                                                   'an organism) that has as its parts '
                                                   'a maximally connected cell '
                                                   'compartment surrounded by a plasma '
                                                   'membrane.',
                                    'name': 'subject',
                                    'range': 'CellType'}}})

    subject: Optional[CellType] = Field(default=None, description="""A material entity of anatomical origin (part of or deriving from an organism) that has as its parts a maximally connected cell compartment surrounded by a plasma membrane.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })
    predicate: Optional[str] = Field(default=None, description="""A relation between a cell c and a protein complex or protein p that is part of the cell's plasma membrane.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association'], 'subproperty_of': 'has_plasma_membrane_part'} })
    object: Optional[Protein] = Field(default=None, description="""An amino acid chain that is canonically produced de novo by ribosome-mediated translation of a genetically-encoded mRNA, and any derivatives thereof""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })


class CellTypeLacksPlasmaMembranePartProtein(Association):
    """
    A relationship between a cell type and a protein that is not part of its plasma membrane but is part of the plasma membrane of related cell types.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'defining_slots': ['subject', 'predicate', 'object'],
         'from_schema': 'https://w3id.org/nlm-ckn-schema',
         'slot_usage': {'object': {'description': 'An amino acid chain that is '
                                                  'canonically produced de novo by '
                                                  'ribosome-mediated translation of a '
                                                  'genetically-encoded mRNA, and any '
                                                  'derivatives thereof',
                                   'name': 'object',
                                   'range': 'Protein'},
                        'predicate': {'description': 'A relation that asserts the lack '
                                                     'of a presence of some cellular '
                                                     "component in a cell's plasma "
                                                     'membrane.',
                                      'name': 'predicate',
                                      'subproperty_of': 'lacks_plasma_membrane_part'},
                        'subject': {'description': 'A material entity of anatomical '
                                                   'origin (part of or deriving from '
                                                   'an organism) that has as its parts '
                                                   'a maximally connected cell '
                                                   'compartment surrounded by a plasma '
                                                   'membrane.',
                                    'name': 'subject',
                                    'range': 'CellType'}}})

    subject: Optional[CellType] = Field(default=None, description="""A material entity of anatomical origin (part of or deriving from an organism) that has as its parts a maximally connected cell compartment surrounded by a plasma membrane.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })
    predicate: Optional[str] = Field(default=None, description="""A relation that asserts the lack of a presence of some cellular component in a cell's plasma membrane.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association'], 'subproperty_of': 'lacks_plasma_membrane_part'} })
    object: Optional[Protein] = Field(default=None, description="""An amino acid chain that is canonically produced de novo by ribosome-mediated translation of a genetically-encoded mRNA, and any derivatives thereof""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })


class ProteinPartOfCellType(Association):
    """
    A relationship between a protein and a cell type that it is part of.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'defining_slots': ['subject', 'predicate', 'object'],
         'from_schema': 'https://w3id.org/nlm-ckn-schema',
         'slot_usage': {'object': {'description': 'A material entity of anatomical '
                                                  'origin (part of or deriving from an '
                                                  'organism) that has as its parts a '
                                                  'maximally connected cell '
                                                  'compartment surrounded by a plasma '
                                                  'membrane.',
                                   'name': 'object',
                                   'range': 'CellType'},
                        'predicate': {'description': 'A relation between a part and '
                                                     'some whole entity.',
                                      'name': 'predicate',
                                      'subproperty_of': 'part_of'},
                        'subject': {'description': 'An amino acid chain that is '
                                                   'canonically produced de novo by '
                                                   'ribosome-mediated translation of a '
                                                   'genetically-encoded mRNA, and any '
                                                   'derivatives thereof',
                                    'name': 'subject',
                                    'range': 'Protein'}}})

    subject: Optional[Protein] = Field(default=None, description="""An amino acid chain that is canonically produced de novo by ribosome-mediated translation of a genetically-encoded mRNA, and any derivatives thereof""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })
    predicate: Optional[str] = Field(default=None, description="""A relation between a part and some whole entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association'], 'subproperty_of': 'part_of'} })
    object: Optional[CellType] = Field(default=None, description="""A material entity of anatomical origin (part of or deriving from an organism) that has as its parts a maximally connected cell compartment surrounded by a plasma membrane.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })


class GeneProducesProtein(Association):
    """
    A relationship between a gene that is the input to a transcription process and the protein that is the output.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'defining_slots': ['subject', 'predicate', 'object'],
         'from_schema': 'https://w3id.org/nlm-ckn-schema',
         'slot_usage': {'object': {'description': 'An amino acid chain that is '
                                                  'canonically produced de novo by '
                                                  'ribosome-mediated translation of a '
                                                  'genetically-encoded mRNA, and any '
                                                  'derivatives thereof',
                                   'name': 'object',
                                   'range': 'Protein'},
                        'predicate': {'description': 'A relation between two material '
                                                     'entites wherein some process '
                                                     'that occurs in a has output b.',
                                      'name': 'predicate',
                                      'subproperty_of': 'produces'},
                        'subject': {'description': 'A region (or regions) that '
                                                   'includes all of the sequence '
                                                   'elements necessary to encode a '
                                                   'functional transcript. A gene may '
                                                   'include regulatory regions, '
                                                   'transcribed regions and/or other '
                                                   'functional sequence regions.',
                                    'name': 'subject',
                                    'range': 'Gene'}}})

    subject: Optional[Gene] = Field(default=None, description="""A region (or regions) that includes all of the sequence elements necessary to encode a functional transcript. A gene may include regulatory regions, transcribed regions and/or other functional sequence regions.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })
    predicate: Optional[str] = Field(default=None, description="""A relation between two material entites wherein some process that occurs in a has output b.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association'], 'subproperty_of': 'produces'} })
    object: Optional[Protein] = Field(default=None, description="""An amino acid chain that is canonically produced de novo by ribosome-mediated translation of a genetically-encoded mRNA, and any derivatives thereof""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })


class GeneIsGeneticBasisForDisease(Association):
    """
    A relationship between a gene and a disease it predisposes an organism to.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'defining_slots': ['subject', 'predicate', 'object'],
         'from_schema': 'https://w3id.org/nlm-ckn-schema',
         'slot_usage': {'object': {'description': 'A disposition to undergo '
                                                  'pathological processes that exists '
                                                  'in an organism because of one or '
                                                  'more disorders in that organism.',
                                   'name': 'object',
                                   'range': 'Disease'},
                        'predicate': {'description': 'A relation between a gene and a '
                                                     'disease or disorder in which it '
                                                     'is a causal input to.',
                                      'name': 'predicate',
                                      'subproperty_of': 'is_genetic_basis_for_condition'},
                        'subject': {'description': 'A region (or regions) that '
                                                   'includes all of the sequence '
                                                   'elements necessary to encode a '
                                                   'functional transcript. A gene may '
                                                   'include regulatory regions, '
                                                   'transcribed regions and/or other '
                                                   'functional sequence regions.',
                                    'name': 'subject',
                                    'range': 'Gene'}}})

    subject: Optional[Gene] = Field(default=None, description="""A region (or regions) that includes all of the sequence elements necessary to encode a functional transcript. A gene may include regulatory regions, transcribed regions and/or other functional sequence regions.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })
    predicate: Optional[str] = Field(default=None, description="""A relation between a gene and a disease or disorder in which it is a causal input to.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association'],
         'subproperty_of': 'is_genetic_basis_for_condition'} })
    object: Optional[Disease] = Field(default=None, description="""A disposition to undergo pathological processes that exists in an organism because of one or more disorders in that organism.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })


class GeneHasQualityMutation(Association):
    """
    A relationship between a gene and some alteration to its nucleic acid sequence.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'defining_slots': ['subject', 'predicate', 'object'],
         'from_schema': 'https://w3id.org/nlm-ckn-schema',
         'slot_usage': {'object': {'description': 'A sequence_alteration is a '
                                                  'sequence_feature whose extent is '
                                                  'the deviation from another '
                                                  'sequence.',
                                   'name': 'object',
                                   'range': 'Mutation'},
                        'predicate': {'description': 'A relation between an '
                                                     'independent continuant and a '
                                                     'quality that specifically '
                                                     'dependends on the independent '
                                                     'continuant.',
                                      'name': 'predicate',
                                      'subproperty_of': 'has_quality'},
                        'subject': {'description': 'A region (or regions) that '
                                                   'includes all of the sequence '
                                                   'elements necessary to encode a '
                                                   'functional transcript. A gene may '
                                                   'include regulatory regions, '
                                                   'transcribed regions and/or other '
                                                   'functional sequence regions.',
                                    'name': 'subject',
                                    'range': 'Gene'}}})

    subject: Optional[Gene] = Field(default=None, description="""A region (or regions) that includes all of the sequence elements necessary to encode a functional transcript. A gene may include regulatory regions, transcribed regions and/or other functional sequence regions.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })
    predicate: Optional[str] = Field(default=None, description="""A relation between an independent continuant and a quality that specifically dependends on the independent continuant.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association'], 'subproperty_of': 'has_quality'} })
    object: Optional[Mutation] = Field(default=None, description="""A sequence_alteration is a sequence_feature whose extent is the deviation from another sequence.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })


class MutationHasPharamcologicalEffectDrug(Association):
    """
    A relationship between a mutation and a drug such that the nucleic acid sequence alteration changes some effect of the drug.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'defining_slots': ['subject', 'predicate', 'object'],
         'from_schema': 'https://w3id.org/nlm-ckn-schema',
         'slot_usage': {'object': {'description': 'A drug product that is bearer of a '
                                                  'clinical drug role.',
                                   'name': 'object',
                                   'range': 'Drug'},
                        'predicate': {'description': 'A relation between a material '
                                                     'entity and a drug such that the '
                                                     'material entity changes some '
                                                     'effect of the drug.',
                                      'name': 'predicate',
                                      'subproperty_of': 'has_pharmacological_effect'},
                        'subject': {'description': 'A sequence_alteration is a '
                                                   'sequence_feature whose extent is '
                                                   'the deviation from another '
                                                   'sequence.',
                                    'name': 'subject',
                                    'range': 'Mutation'}}})

    subject: Optional[Mutation] = Field(default=None, description="""A sequence_alteration is a sequence_feature whose extent is the deviation from another sequence.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })
    predicate: Optional[str] = Field(default=None, description="""A relation between a material entity and a drug such that the material entity changes some effect of the drug.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association'], 'subproperty_of': 'has_pharmacological_effect'} })
    object: Optional[Drug] = Field(default=None, description="""A drug product that is bearer of a clinical drug role.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })


class DrugMolecularlyInteractsWithProtein(Association):
    """
    A relationship between a drug and a protein that it directly interacts with via binding or some modification to either.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'defining_slots': ['subject', 'predicate', 'object'],
         'from_schema': 'https://w3id.org/nlm-ckn-schema',
         'slot_usage': {'object': {'description': 'An amino acid chain that is '
                                                  'canonically produced de novo by '
                                                  'ribosome-mediated translation of a '
                                                  'genetically-encoded mRNA, and any '
                                                  'derivatives thereof',
                                   'name': 'object',
                                   'range': 'Protein'},
                        'predicate': {'description': 'Symmetric relation between two '
                                                     'molecular entities that directly '
                                                     'bind or modify the behavior of '
                                                     'the other.',
                                      'name': 'predicate',
                                      'subproperty_of': 'molecularly_interacts_with'},
                        'subject': {'description': 'A drug product that is bearer of a '
                                                   'clinical drug role.',
                                    'name': 'subject',
                                    'range': 'Drug'}}})

    subject: Optional[Drug] = Field(default=None, description="""A drug product that is bearer of a clinical drug role.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })
    predicate: Optional[str] = Field(default=None, description="""Symmetric relation between two molecular entities that directly bind or modify the behavior of the other.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association'], 'subproperty_of': 'molecularly_interacts_with'} })
    object: Optional[Protein] = Field(default=None, description="""An amino acid chain that is canonically produced de novo by ribosome-mediated translation of a genetically-encoded mRNA, and any derivatives thereof""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })


class DrugIsSubstanceThatTreatsDisease(Association):
    """
    A relationship between a drug and a disease that it has been shown in a phase III clinical trial to be safe and effective at treating.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'defining_slots': ['subject', 'predicate', 'object'],
         'from_schema': 'https://w3id.org/nlm-ckn-schema',
         'slot_usage': {'object': {'description': 'A disposition to undergo '
                                                  'pathological processes that exists '
                                                  'in an organism because of one or '
                                                  'more disorders in that organism.',
                                   'name': 'object',
                                   'range': 'Disease'},
                        'predicate': {'description': 'A relation between a material '
                                                     'entity and some condition, '
                                                     'pathological process, disease, '
                                                     'or phenotype that it treats.',
                                      'name': 'predicate',
                                      'subproperty_of': 'is_substance_that_treats'},
                        'subject': {'description': 'A drug product that is bearer of a '
                                                   'clinical drug role.',
                                    'name': 'subject',
                                    'range': 'Drug'}}})

    subject: Optional[Drug] = Field(default=None, description="""A drug product that is bearer of a clinical drug role.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })
    predicate: Optional[str] = Field(default=None, description="""A relation between a material entity and some condition, pathological process, disease, or phenotype that it treats.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association'], 'subproperty_of': 'is_substance_that_treats'} })
    object: Optional[Disease] = Field(default=None, description="""A disposition to undergo pathological processes that exists in an organism because of one or more disorders in that organism.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })


class CellTypeHasExemplarDataCellSetDataset(Association):
    """
    A relationship between a cell type and a dataset in which some of the data exemplify the cell type.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'defining_slots': ['subject', 'predicate', 'object'],
         'from_schema': 'https://w3id.org/nlm-ckn-schema',
         'slot_usage': {'object': {'description': 'A dataset that is about cells taken '
                                                  'from one or more tissue samples.',
                                   'name': 'object',
                                   'range': 'CellSetDataset'},
                        'predicate': {'description': 'A relation between an entity and '
                                                     'some data in which the data are '
                                                     'taken as exemplifying the '
                                                     'material entity.',
                                      'name': 'predicate',
                                      'subproperty_of': 'has_exemplar_data'},
                        'subject': {'description': 'A material entity of anatomical '
                                                   'origin (part of or deriving from '
                                                   'an organism) that has as its parts '
                                                   'a maximally connected cell '
                                                   'compartment surrounded by a plasma '
                                                   'membrane.',
                                    'name': 'subject',
                                    'range': 'CellType'}}})

    subject: Optional[CellType] = Field(default=None, description="""A material entity of anatomical origin (part of or deriving from an organism) that has as its parts a maximally connected cell compartment surrounded by a plasma membrane.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })
    predicate: Optional[str] = Field(default=None, description="""A relation between an entity and some data in which the data are taken as exemplifying the material entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association'], 'subproperty_of': 'has_exemplar_data'} })
    object: Optional[CellSetDataset] = Field(default=None, description="""A dataset that is about cells taken from one or more tissue samples.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })


class CellSetDerivesFromAnatomicalStructure(Association):
    """
    A relationship between a cell set and an anatomical structure it was extracted from for analysis.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'defining_slots': ['subject', 'predicate', 'object'],
         'from_schema': 'https://w3id.org/nlm-ckn-schema',
         'slot_usage': {'object': {'description': 'Material anatomical entity that is '
                                                  'a single connected structure with '
                                                  'inherent 3D shape generated by '
                                                  'coordinated expression of the '
                                                  "organism's own genome.",
                                   'name': 'object',
                                   'range': 'AnatomicalStructure'},
                        'predicate': {'description': 'A relation between two material '
                                                     'entities, the new entity and the '
                                                     'old entity, in which the new '
                                                     'entity begins to exist when the '
                                                     'old entity ceases to exist, and '
                                                     'the new entity inherits the '
                                                     'significant portion of the '
                                                     'matter of the old entity',
                                      'name': 'predicate',
                                      'subproperty_of': 'derives_from'},
                        'subject': {'description': 'A collection of cells that have '
                                                   'some common property.',
                                    'name': 'subject',
                                    'range': 'CellSet'}}})

    subject: Optional[CellSet] = Field(default=None, description="""A collection of cells that have some common property.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })
    predicate: Optional[str] = Field(default=None, description="""A relation between two material entities, the new entity and the old entity, in which the new entity begins to exist when the old entity ceases to exist, and the new entity inherits the significant portion of the matter of the old entity""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association'], 'subproperty_of': 'derives_from'} })
    object: Optional[AnatomicalStructure] = Field(default=None, description="""Material anatomical entity that is a single connected structure with inherent 3D shape generated by coordinated expression of the organism's own genome.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })


class CellSetHasSourceCellSetDataset(Association):
    """
    A relationship between a cell set and the dataset that contains data about it.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'defining_slots': ['subject', 'predicate', 'object'],
         'from_schema': 'https://w3id.org/nlm-ckn-schema',
         'slot_usage': {'object': {'description': 'A dataset that is about cells taken '
                                                  'from one or more tissue samples.',
                                   'name': 'object',
                                   'range': 'CellSetDataset'},
                        'predicate': {'description': 'A relation between some '
                                                     'information content entity and '
                                                     'the resource from which it '
                                                     'originated.',
                                      'name': 'predicate',
                                      'subproperty_of': 'source'},
                        'subject': {'description': 'A collection of cells that have '
                                                   'some common property.',
                                    'name': 'subject',
                                    'range': 'CellSet'}}})

    subject: Optional[CellSet] = Field(default=None, description="""A collection of cells that have some common property.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })
    predicate: Optional[str] = Field(default=None, description="""A relation between some information content entity and the resource from which it originated.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association'], 'subproperty_of': 'source'} })
    object: Optional[CellSetDataset] = Field(default=None, description="""A dataset that is about cells taken from one or more tissue samples.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })


class GenePartOfBiomarkerCombination(Association):
    """
    A relationship between a gene and a biomarker combination it is a member of.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'defining_slots': ['subject', 'predicate', 'object'],
         'from_schema': 'https://w3id.org/nlm-ckn-schema',
         'slot_usage': {'object': {'description': 'A cell type marker gene is a gene '
                                                  'that is selectively expressed in '
                                                  'cells of a given type and can be '
                                                  'reliably used alone or in '
                                                  'combination as a canonical '
                                                  'characteristic to optimally '
                                                  'classify them.',
                                   'name': 'object',
                                   'range': 'BiomarkerCombination'},
                        'predicate': {'description': 'A relation between a part and '
                                                     'some whole entity.',
                                      'name': 'predicate',
                                      'subproperty_of': 'part_of'},
                        'subject': {'description': 'A region (or regions) that '
                                                   'includes all of the sequence '
                                                   'elements necessary to encode a '
                                                   'functional transcript. A gene may '
                                                   'include regulatory regions, '
                                                   'transcribed regions and/or other '
                                                   'functional sequence regions.',
                                    'name': 'subject',
                                    'range': 'Gene'}}})

    subject: Optional[Gene] = Field(default=None, description="""A region (or regions) that includes all of the sequence elements necessary to encode a functional transcript. A gene may include regulatory regions, transcribed regions and/or other functional sequence regions.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })
    predicate: Optional[str] = Field(default=None, description="""A relation between a part and some whole entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association'], 'subproperty_of': 'part_of'} })
    object: Optional[BiomarkerCombination] = Field(default=None, description="""A cell type marker gene is a gene that is selectively expressed in cells of a given type and can be reliably used alone or in combination as a canonical characteristic to optimally classify them.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })


class CellSetHasCharacterizingMarkerSetBiomarkerCombination(Association):
    """
    A relationship between a cell set and a biomarker combination that can be used to uniquely identify it.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'defining_slots': ['subject', 'predicate', 'object'],
         'from_schema': 'https://w3id.org/nlm-ckn-schema',
         'slot_usage': {'object': {'description': 'A cell type marker gene is a gene '
                                                  'that is selectively expressed in '
                                                  'cells of a given type and can be '
                                                  'reliably used alone or in '
                                                  'combination as a canonical '
                                                  'characteristic to optimally '
                                                  'classify them.',
                                   'name': 'object',
                                   'range': 'BiomarkerCombination'},
                        'predicate': {'description': 'A relation that applies between '
                                                     'a set of markers and a cell type '
                                                     'that can be used to uniquely '
                                                     'identify that cell type.',
                                      'name': 'predicate',
                                      'subproperty_of': 'has_characterizing_marker_set'},
                        'subject': {'description': 'A collection of cells that have '
                                                   'some common property.',
                                    'name': 'subject',
                                    'range': 'CellSet'}}})

    subject: Optional[CellSet] = Field(default=None, description="""A collection of cells that have some common property.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })
    predicate: Optional[str] = Field(default=None, description="""A relation that applies between a set of markers and a cell type that can be used to uniquely identify that cell type.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association'],
         'subproperty_of': 'has_characterizing_marker_set'} })
    object: Optional[BiomarkerCombination] = Field(default=None, description="""A cell type marker gene is a gene that is selectively expressed in cells of a given type and can be reliably used alone or in combination as a canonical characteristic to optimally classify them.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })


class CellSetDatasetHasSourcePublication(Association):
    """
    A relationship between a cell set dataset and the publication that can be used as a reference for it.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'defining_slots': ['subject', 'predicate', 'object'],
         'from_schema': 'https://w3id.org/nlm-ckn-schema',
         'slot_usage': {'object': {'description': 'A document that is the output of a '
                                                  'publishing process.',
                                   'name': 'object',
                                   'range': 'Publication'},
                        'predicate': {'description': 'A relation between some '
                                                     'information content entity and '
                                                     'the resource from which it '
                                                     'originated.',
                                      'name': 'predicate',
                                      'subproperty_of': 'source'},
                        'subject': {'description': 'A dataset that is about cells '
                                                   'taken from one or more tissue '
                                                   'samples.',
                                    'name': 'subject',
                                    'range': 'CellSetDataset'}}})

    subject: Optional[CellSetDataset] = Field(default=None, description="""A dataset that is about cells taken from one or more tissue samples.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })
    predicate: Optional[str] = Field(default=None, description="""A relation between some information content entity and the resource from which it originated.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association'], 'subproperty_of': 'source'} })
    object: Optional[Publication] = Field(default=None, description="""A document that is the output of a publishing process.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })


class CellSetComposedPrimarilyOfCellType(Association):
    """
    A relationship between a cell set and a cell type that comprises most or all of the set.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'defining_slots': ['subject', 'predicate', 'object'],
         'from_schema': 'https://w3id.org/nlm-ckn-schema',
         'slot_usage': {'object': {'description': 'A material entity of anatomical '
                                                  'origin (part of or deriving from an '
                                                  'organism) that has as its parts a '
                                                  'maximally connected cell '
                                                  'compartment surrounded by a plasma '
                                                  'membrane.',
                                   'name': 'object',
                                   'range': 'CellType'},
                        'predicate': {'description': 'A relation between two material '
                                                     'entities in which more than half '
                                                     'of the mass of one is made from '
                                                     'the other or units of the same '
                                                     'type as the other material '
                                                     'entity.',
                                      'name': 'predicate',
                                      'subproperty_of': 'composed_primarily_of'},
                        'subject': {'description': 'A collection of cells that have '
                                                   'some common property.',
                                    'name': 'subject',
                                    'range': 'CellSet'}}})

    subject: Optional[CellSet] = Field(default=None, description="""A collection of cells that have some common property.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })
    predicate: Optional[str] = Field(default=None, description="""A relation between two material entities in which more than half of the mass of one is made from the other or units of the same type as the other material entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association'], 'subproperty_of': 'composed_primarily_of'} })
    object: Optional[CellType] = Field(default=None, description="""A material entity of anatomical origin (part of or deriving from an organism) that has as its parts a maximally connected cell compartment surrounded by a plasma membrane.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })


class DrugEvaluatedInClinicalTrial(Association):
    """
    A relationship between a drug and some clinical trial it was tested in.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'defining_slots': ['subject', 'predicate', 'object'],
         'from_schema': 'https://w3id.org/nlm-ckn-schema',
         'slot_usage': {'object': {'description': 'A clinical investigation that '
                                                  'involves an intervention.',
                                   'name': 'object',
                                   'range': 'ClinicalTrial'},
                        'predicate': {'description': 'A relation between a drug and '
                                                     'some clinical trial it was '
                                                     'tested in.',
                                      'name': 'predicate',
                                      'subproperty_of': 'evaluated_in'},
                        'subject': {'description': 'A drug product that is bearer of a '
                                                   'clinical drug role.',
                                    'name': 'subject',
                                    'range': 'Drug'}}})

    subject: Optional[Drug] = Field(default=None, description="""A drug product that is bearer of a clinical drug role.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })
    predicate: Optional[str] = Field(default=None, description="""A relation between a drug and some clinical trial it was tested in.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association'], 'subproperty_of': 'evaluated_in'} })
    object: Optional[ClinicalTrial] = Field(default=None, description="""A clinical investigation that involves an intervention.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })


class DrugMolecularlyInteractsWithGene(Association):
    """
    A relationship between a drug and some gene whose gene products directly interact with the drug. This is a symmetric relationship.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'defining_slots': ['subject', 'predicate', 'object'],
         'from_schema': 'https://w3id.org/nlm-ckn-schema',
         'slot_usage': {'object': {'description': 'A region (or regions) that includes '
                                                  'all of the sequence elements '
                                                  'necessary to encode a functional '
                                                  'transcript. A gene may include '
                                                  'regulatory regions, transcribed '
                                                  'regions and/or other functional '
                                                  'sequence regions.',
                                   'name': 'object',
                                   'range': 'Gene'},
                        'predicate': {'description': 'Symmetric relation between two '
                                                     'molecular entities that directly '
                                                     'bind or modify the behavior of '
                                                     'the other.',
                                      'name': 'predicate',
                                      'subproperty_of': 'molecularly_interacts_with'},
                        'subject': {'description': 'A drug product that is bearer of a '
                                                   'clinical drug role.',
                                    'name': 'subject',
                                    'range': 'Drug'}}})

    subject: Optional[Drug] = Field(default=None, description="""A drug product that is bearer of a clinical drug role.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })
    predicate: Optional[str] = Field(default=None, description="""Symmetric relation between two molecular entities that directly bind or modify the behavior of the other.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association'], 'subproperty_of': 'molecularly_interacts_with'} })
    object: Optional[Gene] = Field(default=None, description="""A region (or regions) that includes all of the sequence elements necessary to encode a functional transcript. A gene may include regulatory regions, transcribed regions and/or other functional sequence regions.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })


class GeneMolecularlyInteractsWithDrug(Association):
    """
    A relationship between a gene and a drug wherein a gene product of that gene binds with or modifies the behavior of the drug.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'defining_slots': ['subject', 'predicate', 'object'],
         'from_schema': 'https://w3id.org/nlm-ckn-schema',
         'slot_usage': {'object': {'description': 'A drug product that is bearer of a '
                                                  'clinical drug role.',
                                   'name': 'object',
                                   'range': 'Drug'},
                        'predicate': {'description': 'Symmetric relation between two '
                                                     'molecular entities that directly '
                                                     'bind or modify the behavior of '
                                                     'the other.',
                                      'name': 'predicate',
                                      'subproperty_of': 'molecularly_interacts_with'},
                        'subject': {'description': 'A region (or regions) that '
                                                   'includes all of the sequence '
                                                   'elements necessary to encode a '
                                                   'functional transcript. A gene may '
                                                   'include regulatory regions, '
                                                   'transcribed regions and/or other '
                                                   'functional sequence regions.',
                                    'name': 'subject',
                                    'range': 'Gene'}}})

    subject: Optional[Gene] = Field(default=None, description="""A region (or regions) that includes all of the sequence elements necessary to encode a functional transcript. A gene may include regulatory regions, transcribed regions and/or other functional sequence regions.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })
    predicate: Optional[str] = Field(default=None, description="""Symmetric relation between two molecular entities that directly bind or modify the behavior of the other.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association'], 'subproperty_of': 'molecularly_interacts_with'} })
    object: Optional[Drug] = Field(default=None, description="""A drug product that is bearer of a clinical drug role.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })


class GeneGeneticallyInteractsWithGene(Association):
    """
    A relationship between a gene and a second gene that it modifies the activity of.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'defining_slots': ['subject', 'predicate', 'object'],
         'from_schema': 'https://w3id.org/nlm-ckn-schema',
         'slot_usage': {'object': {'description': 'A region (or regions) that includes '
                                                  'all of the sequence elements '
                                                  'necessary to encode a functional '
                                                  'transcript. A gene may include '
                                                  'regulatory regions, transcribed '
                                                  'regions and/or other functional '
                                                  'sequence regions.',
                                   'name': 'object',
                                   'range': 'Gene'},
                        'predicate': {'description': 'Symmetric relation between two '
                                                     'genetic entities that interact '
                                                     'at the genetic level.',
                                      'name': 'predicate',
                                      'subproperty_of': 'genetically_interacts_with'},
                        'subject': {'description': 'A region (or regions) that '
                                                   'includes all of the sequence '
                                                   'elements necessary to encode a '
                                                   'functional transcript. A gene may '
                                                   'include regulatory regions, '
                                                   'transcribed regions and/or other '
                                                   'functional sequence regions.',
                                    'name': 'subject',
                                    'range': 'Gene'}}})

    subject: Optional[Gene] = Field(default=None, description="""A region (or regions) that includes all of the sequence elements necessary to encode a functional transcript. A gene may include regulatory regions, transcribed regions and/or other functional sequence regions.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })
    predicate: Optional[str] = Field(default=None, description="""Symmetric relation between two genetic entities that interact at the genetic level.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association'], 'subproperty_of': 'genetically_interacts_with'} })
    object: Optional[Gene] = Field(default=None, description="""A region (or regions) that includes all of the sequence elements necessary to encode a functional transcript. A gene may include regulatory regions, transcribed regions and/or other functional sequence regions.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })


class CellSetExactMatchCellSet(Association):
    """
    A relationship between two cell sets that are both instances of the same cell type that have been mapped to each other.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'defining_slots': ['subject', 'predicate', 'object'],
         'from_schema': 'https://w3id.org/nlm-ckn-schema',
         'slot_usage': {'object': {'description': 'A collection of cells that have '
                                                  'some common property.',
                                   'name': 'object',
                                   'range': 'CellSet'},
                        'predicate': {'description': 'A mapping relation between two '
                                                     'entities that are of the same '
                                                     'type.',
                                      'name': 'predicate',
                                      'subproperty_of': 'exact_match'},
                        'subject': {'description': 'A collection of cells that have '
                                                   'some common property.',
                                    'name': 'subject',
                                    'range': 'CellSet'}}})

    subject: Optional[CellSet] = Field(default=None, description="""A collection of cells that have some common property.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })
    predicate: Optional[str] = Field(default=None, description="""A mapping relation between two entities that are of the same type.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association'], 'subproperty_of': 'exact_match'} })
    object: Optional[CellSet] = Field(default=None, description="""A collection of cells that have some common property.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })


class BiomarkerCombinationSubclusterOfBinaryGeneSet(Association):
    """
    A relationship between a biomarker combination and a set of binary genes that its members are a member of.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'defining_slots': ['subject', 'predicate', 'object'],
         'from_schema': 'https://w3id.org/nlm-ckn-schema',
         'slot_usage': {'object': {'description': 'A collection of discontinuous '
                                                  'sequences.',
                                   'name': 'object',
                                   'range': 'BinaryGeneSet'},
                        'predicate': {'description': 'A relation between a group and '
                                                     'another group it is part of but '
                                                     'does not fully constitute.',
                                      'name': 'predicate',
                                      'subproperty_of': 'subcluster_of'},
                        'subject': {'description': 'A cell type marker gene is a gene '
                                                   'that is selectively expressed in '
                                                   'cells of a given type and can be '
                                                   'reliably used alone or in '
                                                   'combination as a canonical '
                                                   'characteristic to optimally '
                                                   'classify them.',
                                    'name': 'subject',
                                    'range': 'BiomarkerCombination'}}})

    subject: Optional[BiomarkerCombination] = Field(default=None, description="""A cell type marker gene is a gene that is selectively expressed in cells of a given type and can be reliably used alone or in combination as a canonical characteristic to optimally classify them.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })
    predicate: Optional[str] = Field(default=None, description="""A relation between a group and another group it is part of but does not fully constitute.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association'], 'subproperty_of': 'subcluster_of'} })
    object: Optional[BinaryGeneSet] = Field(default=None, description="""A collection of discontinuous sequences.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })


class CellSetExpressesBinaryGeneSet(Association):
    """
    A relationship between a cell set and a set of binary genes that it expresses.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'defining_slots': ['subject', 'predicate', 'object'],
         'from_schema': 'https://w3id.org/nlm-ckn-schema',
         'slot_usage': {'object': {'description': 'A collection of discontinuous '
                                                  'sequences.',
                                   'name': 'object',
                                   'range': 'BinaryGeneSet'},
                        'predicate': {'description': 'relation between some biological '
                                                     'entity and a gene that is the '
                                                     'input of some gene expression '
                                                     'process',
                                      'name': 'predicate',
                                      'subproperty_of': 'expresses'},
                        'subject': {'description': 'A collection of cells that have '
                                                   'some common property.',
                                    'name': 'subject',
                                    'range': 'CellSet'}}})

    subject: Optional[CellSet] = Field(default=None, description="""A collection of cells that have some common property.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })
    predicate: Optional[str] = Field(default=None, description="""relation between some biological entity and a gene that is the input of some gene expression process""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association'], 'subproperty_of': 'expresses'} })
    object: Optional[BinaryGeneSet] = Field(default=None, description="""A collection of discontinuous sequences.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })


class ProteinCapableOfMolecularFunction(Association):
    """
    A relationship between a protein and a molecular function that it is directly involved in carrying out.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'defining_slots': ['subject', 'predicate', 'object'],
         'from_schema': 'https://w3id.org/nlm-ckn-schema',
         'slot_usage': {'object': {'description': 'A molecular process that can be '
                                                  'carried out by the action of a '
                                                  'single macromolecular machine, '
                                                  'usually via direct physical '
                                                  'interactions with other molecular '
                                                  'entities. Function in this sense '
                                                  'denotes an action, or activity, '
                                                  'that a gene product (or a complex) '
                                                  'performs.',
                                   'name': 'object',
                                   'range': 'MolecularFunction'},
                        'predicate': {'description': 'A relation between a material '
                                                     'entity (such as a cell) and a '
                                                     'process, in which the material '
                                                     'entity has the ability to carry '
                                                     'out the process.',
                                      'name': 'predicate',
                                      'subproperty_of': 'capable_of'},
                        'subject': {'description': 'An amino acid chain that is '
                                                   'canonically produced de novo by '
                                                   'ribosome-mediated translation of a '
                                                   'genetically-encoded mRNA, and any '
                                                   'derivatives thereof',
                                    'name': 'subject',
                                    'range': 'Protein'}}})

    subject: Optional[Protein] = Field(default=None, description="""An amino acid chain that is canonically produced de novo by ribosome-mediated translation of a genetically-encoded mRNA, and any derivatives thereof""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })
    predicate: Optional[str] = Field(default=None, description="""A relation between a material entity (such as a cell) and a process, in which the material entity has the ability to carry out the process.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association'], 'subproperty_of': 'capable_of'} })
    object: Optional[MolecularFunction] = Field(default=None, description="""A molecular process that can be carried out by the action of a single macromolecular machine, usually via direct physical interactions with other molecular entities. Function in this sense denotes an action, or activity, that a gene product (or a complex) performs.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })


class ProteinInvolvedInBiologicalProcess(Association):
    """
    A relationship between a protein and a biological process that it is directly involved in carrying out.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'defining_slots': ['subject', 'predicate', 'object'],
         'from_schema': 'https://w3id.org/nlm-ckn-schema',
         'slot_usage': {'object': {'description': 'A biological process is the '
                                                  'execution of a genetically-encoded '
                                                  'biological module or program. It '
                                                  'consists of all the steps required '
                                                  'to achieve the specific biological '
                                                  'objective of the module. A '
                                                  'biological process is accomplished '
                                                  'by a particular set of molecular '
                                                  'functions carried out by specific '
                                                  'gene products (or macromolecular '
                                                  'complexes), often in a highly '
                                                  'regulated manner and in a '
                                                  'particular temporal sequence.',
                                   'name': 'object',
                                   'range': 'BiologicalProcess'},
                        'predicate': {'description': 'A relation between a material '
                                                     'entity and a process in which '
                                                     'the material entity enables some '
                                                     'subprocess that is part of the '
                                                     'larger process.',
                                      'name': 'predicate',
                                      'subproperty_of': 'involved_in'},
                        'subject': {'description': 'An amino acid chain that is '
                                                   'canonically produced de novo by '
                                                   'ribosome-mediated translation of a '
                                                   'genetically-encoded mRNA, and any '
                                                   'derivatives thereof',
                                    'name': 'subject',
                                    'range': 'Protein'}}})

    subject: Optional[Protein] = Field(default=None, description="""An amino acid chain that is canonically produced de novo by ribosome-mediated translation of a genetically-encoded mRNA, and any derivatives thereof""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })
    predicate: Optional[str] = Field(default=None, description="""A relation between a material entity and a process in which the material entity enables some subprocess that is part of the larger process.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association'], 'subproperty_of': 'involved_in'} })
    object: Optional[BiologicalProcess] = Field(default=None, description="""A biological process is the execution of a genetically-encoded biological module or program. It consists of all the steps required to achieve the specific biological objective of the module. A biological process is accomplished by a particular set of molecular functions carried out by specific gene products (or macromolecular complexes), often in a highly regulated manner and in a particular temporal sequence.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })


class ProteinLocatedInCellularComponent(Association):
    """
    A relationship between a protein and a cellular component that is a constituent part of it.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'defining_slots': ['subject', 'predicate', 'object'],
         'from_schema': 'https://w3id.org/nlm-ckn-schema',
         'slot_usage': {'object': {'description': 'A location, relative to cellular '
                                                  'compartments and structures, '
                                                  'occupied by a macromolecular '
                                                  'machine. There are three types of '
                                                  'cellular components described in '
                                                  'the gene ontology: (1) the cellular '
                                                  'anatomical entity where a gene '
                                                  'product carries out a molecular '
                                                  'function (e.g., plasma membrane, '
                                                  'cytoskeleton) or membrane-enclosed '
                                                  'compartments (e.g., mitochondrion); '
                                                  '(2)virion components, where viral '
                                                  'proteins act, and (3) the stable '
                                                  'macromolecular complexes of which '
                                                  'gene product are parts (e.g., the '
                                                  'clathrin complex).',
                                   'name': 'object',
                                   'range': 'CellularComponent'},
                        'predicate': {'description': 'A relation between two '
                                                     'independent continuants, the '
                                                     'target and the location, in '
                                                     'which the target is entirely '
                                                     'within the location',
                                      'name': 'predicate',
                                      'subproperty_of': 'located_in'},
                        'subject': {'description': 'An amino acid chain that is '
                                                   'canonically produced de novo by '
                                                   'ribosome-mediated translation of a '
                                                   'genetically-encoded mRNA, and any '
                                                   'derivatives thereof',
                                    'name': 'subject',
                                    'range': 'Protein'}}})

    source: Optional[str] = Field(default=None, description="""The resource from which some information, data, or knowledge originated.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Mutation', 'ProteinLocatedInCellularComponent'],
         'slot_uri': 'dc:source'} })
    subject: Optional[Protein] = Field(default=None, description="""An amino acid chain that is canonically produced de novo by ribosome-mediated translation of a genetically-encoded mRNA, and any derivatives thereof""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })
    predicate: Optional[str] = Field(default=None, description="""A relation between two independent continuants, the target and the location, in which the target is entirely within the location""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association'], 'subproperty_of': 'located_in'} })
    object: Optional[CellularComponent] = Field(default=None, description="""A location, relative to cellular compartments and structures, occupied by a macromolecular machine. There are three types of cellular components described in the gene ontology: (1) the cellular anatomical entity where a gene product carries out a molecular function (e.g., plasma membrane, cytoskeleton) or membrane-enclosed compartments (e.g., mitochondrion); (2)virion components, where viral proteins act, and (3) the stable macromolecular complexes of which gene product are parts (e.g., the clathrin complex).""", json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
Association.model_rebuild()
CellSet.model_rebuild()
CellType.model_rebuild()
Gene.model_rebuild()
Drug.model_rebuild()
AnatomicalStructure.model_rebuild()
Species.model_rebuild()
CellSetDataset.model_rebuild()
Publication.model_rebuild()
BiomarkerCombination.model_rebuild()
Protein.model_rebuild()
Disease.model_rebuild()
BinaryGeneSet.model_rebuild()
ClinicalTrial.model_rebuild()
BiologicalProcess.model_rebuild()
CellularComponent.model_rebuild()
MolecularFunction.model_rebuild()
LifeCycleStage.model_rebuild()
ChemicalEntity.model_rebuild()
OrganismTrait.model_rebuild()
Mutation.model_rebuild()
VariantConsequence.model_rebuild()
CellTypePartOfAnatomicalStructure.model_rebuild()
AnatomicalStructurePartOfAnatomicalStructure.model_rebuild()
CellTypeInteractsWithCellType.model_rebuild()
CellTypeDevelopsFromCellType.model_rebuild()
CellTypeSubclassOfCellType.model_rebuild()
CellTypeExpressesGene.model_rebuild()
CellTypeHasPlasmaMembranePartProtein.model_rebuild()
CellTypeLacksPlasmaMembranePartProtein.model_rebuild()
ProteinPartOfCellType.model_rebuild()
GeneProducesProtein.model_rebuild()
GeneIsGeneticBasisForDisease.model_rebuild()
GeneHasQualityMutation.model_rebuild()
MutationHasPharamcologicalEffectDrug.model_rebuild()
DrugMolecularlyInteractsWithProtein.model_rebuild()
DrugIsSubstanceThatTreatsDisease.model_rebuild()
CellTypeHasExemplarDataCellSetDataset.model_rebuild()
CellSetDerivesFromAnatomicalStructure.model_rebuild()
CellSetHasSourceCellSetDataset.model_rebuild()
GenePartOfBiomarkerCombination.model_rebuild()
CellSetHasCharacterizingMarkerSetBiomarkerCombination.model_rebuild()
CellSetDatasetHasSourcePublication.model_rebuild()
CellSetComposedPrimarilyOfCellType.model_rebuild()
DrugEvaluatedInClinicalTrial.model_rebuild()
DrugMolecularlyInteractsWithGene.model_rebuild()
GeneMolecularlyInteractsWithDrug.model_rebuild()
GeneGeneticallyInteractsWithGene.model_rebuild()
CellSetExactMatchCellSet.model_rebuild()
BiomarkerCombinationSubclusterOfBinaryGeneSet.model_rebuild()
CellSetExpressesBinaryGeneSet.model_rebuild()
ProteinCapableOfMolecularFunction.model_rebuild()
ProteinInvolvedInBiologicalProcess.model_rebuild()
ProteinLocatedInCellularComponent.model_rebuild()
