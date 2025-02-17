import pytest

from demisto_sdk.commands.common.constants import DEFAULT_JOB_FROM_VERSION, JOB
from demisto_sdk.commands.format.format_module import run_format_on_file


@pytest.mark.parametrize('is_feed,all_feeds', ((True, True),
                                               (False, False)))
def test_infer_selected_feeds(repo, is_feed: bool, all_feeds: bool):
    """
    Given
            A Job object that should have selectedFeeds==[]
    When
            Calling format
    Then
            Ensure the selectedFeeds field is added, and is equal to []
    """
    pack = repo.create_pack()
    job = pack.create_job(is_feed)
    job_dict_before = job.read_json_as_dict()
    assert is_feed == job_dict_before['isFeed']
    assert is_feed == job_dict_before['isAllFeeds']
    assert job_dict_before['selectedFeeds'] == []

    job.remove('selectedFeeds')
    assert 'selectedFeeds' not in job.read_json_as_dict()

    run_format_on_file(job.path, JOB, DEFAULT_JOB_FROM_VERSION, interactive=True)

    job_dict_after = job.read_json_as_dict()
    assert 'selectedFeeds' in job_dict_after
    assert job_dict_after['selectedFeeds'] == []


@pytest.mark.parametrize('is_feed', (True, False))
def test_add_default_fromversion(repo, is_feed: bool):
    """
    Given
            A Job object that doesn't have fromVersion
    When
            Calling format
    Then
            Ensure the default value is added
    """
    pack = repo.create_pack()
    job = pack.create_job(is_feed)
    job_dict_before = job.read_json_as_dict()
    assert job_dict_before['fromVersion'] == DEFAULT_JOB_FROM_VERSION

    job.remove('fromVersion')
    assert 'fromVersion' not in job.read_json_as_dict()

    run_format_on_file(job.path, JOB, DEFAULT_JOB_FROM_VERSION, interactive=True)

    job_dict_after = job.read_json_as_dict()
    assert 'fromVersion' in job_dict_after
    assert job_dict_after['fromVersion'] == DEFAULT_JOB_FROM_VERSION


@pytest.mark.parametrize('is_feed', (True, False))
def test_update_id(repo, is_feed: bool):
    """
    Given
            A Job object, with a missing ID
    When
            Calling format
    Then
            Ensure the updated id is equal to the job's name
    """
    pack = repo.create_pack()
    job = pack.create_job(is_feed)
    job.remove('id')
    run_format_on_file(job.path, JOB, DEFAULT_JOB_FROM_VERSION, interactive=True)
    job_dict_after = job.read_json_as_dict()
    assert job_dict_after['id'] == job.pure_name
