#!/usr/bin/env python3
# encoding: utf-8
#
# This file is part of ckanext-doi
# Created by the Natural History Museum in London, UK
from unittest.mock import MagicMock, patch

import pytest
from ckan.model import Session
from ckan.tests import factories
from datacite.errors import DataCiteNotFoundError

from ckanext.doi.model.doi import DOI


@pytest.mark.filterwarnings('ignore::sqlalchemy.exc.SADeprecationWarning')
@pytest.mark.ckan_config('ckan.plugins', 'doi')
@pytest.mark.ckan_config('ckanext.doi.prefix', 'testing')
@pytest.mark.usefixtures('with_doi_table', 'with_plugins')
@patch('ckanext.doi.lib.api.DataCiteMDSClient')
def test_doi_is_created_automatically(mock_client):
    # this test ensures that when a package is created, a DOI is created
    mock_client.return_value = MagicMock(
        metadata_get=MagicMock(side_effect=DataCiteNotFoundError())
    )
    package = factories.Dataset()
    found_record = Session.query(DOI).filter(DOI.package_id == package['id']).one()
    assert found_record is not None
