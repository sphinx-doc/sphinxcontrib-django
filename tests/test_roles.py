import pytest


@pytest.mark.sphinx("html", testroot="docstrings")
def test_setup_with_conflicting_extension(app_with_conflicting_extension, caplog):
    setup_records = caplog.get_records("setup")
    assert len(setup_records) == 1
    assert setup_records[0].name == "sphinxcontrib_django2.roles"
    assert "Unable to register cross-reference type: " in setup_records[0].msg
