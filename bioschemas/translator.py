import logging

import bioschemas

logger = logging.getLogger(__name__)


def create_solr_json_with_mandatory_properties(schema, jsonld):
    """
    Create JSON we can put into Solr from the Bioschemas JsonLD

    :param schema:
    :param jsonld:
    :return:
    """

    # print('Inspecting schema %s with jsonld size %d' % (schema, len(jsonld)))
    solr_json = {}

    if schema in bioschemas.MANDATORY_PROPERTIES:
        for prop_name in bioschemas.MANDATORY_PROPERTIES[schema]:
            if prop_name in bioschemas.JSONLD_TO_SOLR_MAP:
                solr_prop_name = bioschemas.JSONLD_TO_SOLR_MAP[prop_name]
            else:
                solr_prop_name = prop_name

            logger.debug(
                'Adding key "%s" -> "%s" for %s, value "%s"',
                prop_name, solr_prop_name, jsonld[prop_name], schema)

            solr_json[solr_prop_name] = jsonld[prop_name]

    parent_schema = bioschemas.SCHEMA_INHERITANCE_GRAPH[schema]
    if parent_schema is not None:
        solr_json.update(create_solr_json_with_mandatory_properties(parent_schema, jsonld))

    return solr_json
