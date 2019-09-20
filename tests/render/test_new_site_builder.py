import os
import pytest
import json
import re

from great_expectations.util import (
    gen_directory_tree_str
)
from great_expectations.data_context.util import (
    parse_string_to_data_context_resource_identifier
)
from great_expectations.render.renderer.new_site_builder import (
    SiteBuilder,
    DefaultSiteSectionBuilder,
    DefaultSiteIndexBuilder,
)
from great_expectations.data_context.types import (
    ValidationResultIdentifier,
    SiteSectionIdentifier,
)

def test_new_SiteBuilder(titanic_data_context, filesystem_csv_2):
    titanic_data_context.profile_datasource(titanic_data_context.list_datasources()[0]["name"])

    titanic_data_context.add_store(
        "local_site_html_store",
        {
            "module_name": "great_expectations.data_context.store",
            "class_name": "BasicInMemoryStore"
        }
    )

    my_site_builder = SiteBuilder(
        titanic_data_context,
        target_store_name= "local_site_html_store",
        site_index_builder= {
            "class_name": "DefaultSiteIndexBuilder",
        },
        site_section_builders = {
            "expectations" : {
                "class_name": "DefaultSiteSectionBuilder",
                "source_store_name": "expectations_store",
                "renderer" : {
                    "module_name": "great_expectations.render.renderer",
                    "class_name" : "ExpectationSuitePageRenderer",
                },
            }
        }
        # datasource_whitelist=[],
        # datasource_blacklist=[],
    )

    # FIXME : Re-up this
    # my_site_builder.build()

def test_SiteSectionBuilder(titanic_data_context, filesystem_csv_2):
    titanic_data_context.profile_datasource(titanic_data_context.list_datasources()[0]["name"])

    titanic_data_context.add_store(
        "local_site_html_store",
        {
            "module_name": "great_expectations.data_context.store",
            "class_name": "EvaluationParameterStore",
        }
    )

    my_site_section_builders = DefaultSiteSectionBuilder(
        "test_name",
        titanic_data_context,
        source_store_name="expectations_store",
        target_store_name="local_site_html_store",
        renderer = {
            "module_name": "great_expectations.render.renderer",
            "class_name" : "ExpectationSuitePageRenderer",
        },
    )

    my_site_section_builders.build()

    print(titanic_data_context.stores["local_site_html_store"].list_keys())
    assert len(titanic_data_context.stores["local_site_html_store"].list_keys()) == 1
    
    first_key = titanic_data_context.stores["local_site_html_store"].list_keys()[0]
    print(first_key)
    print(type(first_key))
    assert first_key == SiteSectionIdentifier(
        site_section_name="test_name",
        resource_identifier=parse_string_to_data_context_resource_identifier(
            "ExpectationSuiteIdentifier.mydatasource.mygenerator.Titanic.BasicDatasetProfiler"
        ),
    )

    content = titanic_data_context.stores["local_site_html_store"].get(first_key)
    assert len(re.findall("<div.*>", content)) > 20 # Ah! Then it MUST be HTML!


# def test_SiteIndexBuilder(titanic_data_context, filesystem_csv_2):
#     titanic_data_context.profile_datasource(titanic_data_context.list_datasources()[0]["name"])

#     titanic_data_context.add_store(
#         "local_site_html_store",
#         {
#             "module_name": "great_expectations.data_context.store",
#             "class_name": "EvaluationParameterStore",
#         }
#     )

#     my_site_section_builders = DefaultSiteIndexBuilder(
#         titanic_data_context,
#         target_store_name="local_site_html_store",
#         renderer = {
#             "module_name": "great_expectations.render.renderer",
#             "class_name" : "ExpectationSuitePageRenderer",
#         },
#     )

#     my_site_section_builders.build()

#     print(titanic_data_context.stores["local_site_html_store"].list_keys())
#     assert len(titanic_data_context.stores["local_site_html_store"].list_keys()) == 1
    
#     first_key = titanic_data_context.stores["local_site_html_store"].list_keys()[0]
#     assert first_key == "ExpectationSuiteIdentifier.mydatasource.mygenerator.Titanic.BasicDatasetProfiler"

#     content = titanic_data_context.stores["local_site_html_store"].get(first_key)
#     assert len(re.findall("<div.*>", content)) > 20 # Ah! Then it MUST be HTML!