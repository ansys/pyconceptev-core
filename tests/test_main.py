import os

import httpx
import pytest
from pytest_httpx import HTTPXMock

from ansys.conceptev.core import main

conceptev_url = os.environ["CONCEPTEV_URL"]
ocm_url = os.environ["OCM_URL"]


def test_get_token(httpx_mock: HTTPXMock):
    print(conceptev_url)
    print(ocm_url)

    fake_token = "value1"
    httpx_mock.add_response(
        url=f"{ocm_url}/auth/login/", method="post", json={"accessToken": fake_token}
    )
    token = main.get_token()
    assert token == fake_token


@pytest.fixture
def client():
    fake_token = "value1"
    design_instance_id = "123"
    client = main.get_http_client(fake_token, design_instance_id=design_instance_id)
    return client


def test_get_http_client():
    fake_token = "value1"
    design_instance_id = "123"
    client = main.get_http_client(fake_token, design_instance_id=design_instance_id)
    assert isinstance(client, httpx.Client)
    assert client.headers["authorization"] == fake_token
    assert str(client.base_url).strip("/") == os.environ["CONCEPTEV_URL"].strip("/")
    assert client.params["design_instance_id"] == design_instance_id


def test_processed_response():
    fake_response = httpx.Response(status_code=200, content='{"hello":"again"}')
    content = main.processed_response(fake_response)
    assert content == fake_response.json()
    fake_str_response = httpx.Response(status_code=200, content="hello")
    content = main.processed_response(fake_str_response)
    assert content == fake_str_response.content
    fake_failure = httpx.Response(status_code=400, content='{"hello":"again"}')
    with pytest.raises(Exception) as e:
        content = main.processed_response(fake_failure)
    assert e.value.args[0].startswith("Response Failed:")


def test_get(httpx_mock: HTTPXMock, client: httpx.Client):
    example_results = [{"name": "aero_mock_response"}, {"name": "aero_mock_response2"}]
    httpx_mock.add_response(
        url=f"{conceptev_url}/configurations?design_instance_id=123",
        method="get",
        json=example_results,
    )

    results = main.get(client, "/configurations")
    assert results == example_results


def test_post(httpx_mock: HTTPXMock, client: httpx.Client):
    example_aero = {"name": "aero_mock_response"}
    httpx_mock.add_response(
        url=f"{conceptev_url}/configurations?design_instance_id=123",
        method="post",
        match_json=example_aero,
        json=example_aero,
    )

    results = main.post(client, "/configurations", example_aero)
    assert results == example_aero


def test_delete(httpx_mock: HTTPXMock, client: httpx.Client):
    httpx_mock.add_response(
        url=f"{conceptev_url}/configurations/456?design_instance_id=123",
        method="delete",
        status_code=204,
    )
    httpx_mock.add_response(
        url=f"{conceptev_url}/configurations/489?design_instance_id=123",
        method="delete",
        status_code=404,
    )

    main.delete(client, "/configurations", "456")
    with pytest.raises(Exception) as e:
        main.delete(client, "/configurations", "489")
    assert e.value.args[0].startswith("Failed to delete from")


def test_create_new_project(httpx_mock: HTTPXMock, client: httpx.Client):
    client.params = []
    project_id = "project_id_123"
    design_id = "design_id_123"
    design_instance_id = "design_instance_123"
    account_id = "account_id_123"
    hpc_id = "hpc_id_123"
    user_id = "user_id_123"
    title = "Testing Title"
    mocked_concept = {"name": "new_mocked_concept"}
    mocked_project = {"projectId": project_id}
    mocked_design = {
        "designId": design_id,
        "designInstanceList": [{"designInstanceId": design_instance_id}],
        "projectId": project_id,
    }
    mocked_user = {"userId": user_id}
    project_data = {
        "accountId": account_id,
        "hpcId": hpc_id,
        "projectTitle": title,
        "projectGoal": "Created from the CLI",
    }

    httpx_mock.add_response(
        url=f"{ocm_url}/project/create", method="post", match_json=project_data, json=mocked_project
    )

    design_data = {
        "projectId": project_id,
        "productId": "ec987729-a125-4f9d-ae3f-c3a81ca75112",
        "designTitle": "Branch 1",
    }
    httpx_mock.add_response(
        url=f"{ocm_url}/design/create", method="post", match_json=design_data, json=mocked_design
    )
    httpx_mock.add_response(url=f"{ocm_url}/user/details", method="post", json=mocked_user)

    concept_data = {
        "capabilities_ids": [],
        "components_ids": [],
        "configurations_ids": [],
        "design_id": design_id,
        "design_instance_id": design_instance_id,
        "drive_cycles_ids": [],
        "jobs_ids": [],
        "name": "Branch 1",
        "project_id": project_id,
        "requirements_ids": [],
        "user_id": user_id,
    }
    httpx_mock.add_response(
        url=f"{conceptev_url}/concepts",
        method="post",
        match_json=concept_data,
        json=mocked_concept,
    )
    value = main.create_new_project(client, account_id, hpc_id, title)
    assert value == mocked_concept


def test_get_concept_ids(httpx_mock: HTTPXMock, client: httpx.Client):
    client.params = []
    mocked_concepts = [
        {"name": "start", "id": "1"},
        {"name": "pie", "id": "3.17"},
        {"name": "end", "id": "ragnorok"},
    ]
    httpx_mock.add_response(url=f"{conceptev_url}/concepts", method="get", json=mocked_concepts)
    returned_concepts = main.get_concept_ids(client)
    for concept in mocked_concepts:
        assert returned_concepts[concept["name"]] == concept["id"]


def test_get_account_ids(httpx_mock: HTTPXMock):
    token = "123"
    mocked_accounts = [
        {"account": {"accountName": "account 1", "accountId": "al;kjasdf"}},
        {"account": {"accountName": "account 2", "accountId": "asdhalkjh"}},
    ]
    httpx_mock.add_response(
        url=f"{ocm_url}/account/list",
        method="post",
        headers={"authorization": token},
        json=mocked_accounts,
        status_code=200,
    )
    returned_account = main.get_account_ids(token)
    for account in mocked_accounts:
        assert (
            returned_account[account["account"]["accountName"]] == account["account"]["accountId"]
        )


def test_get_default_hpc(httpx_mock: HTTPXMock):
    mocked_account = {"accountId": "567"}
    mocked_hpc = {"hpcId": "345"}
    token = "123"
    httpx_mock.add_response(
        url=f"{ocm_url}/account/hpc/default",
        method="post",
        headers={"authorization": token},
        match_json=mocked_account,
        json=mocked_hpc,
        status_code=200,
    )
    hpc_id = main.get_default_hpc(token, mocked_account["accountId"])
    assert hpc_id == mocked_hpc["hpcId"]


def test_create_submit_job(httpx_mock: HTTPXMock, client: httpx.Client):
    account_id = "123"
    hpc_id = "456"
    job_name = "789"
    concept = {
        "requirements_ids": "abc",
        "architecture_id": "def",
        "id": "ghi",
        "design_instance_id": "jkl",
    }
    job_input = {
        "job_name": job_name,
        "requirement_ids": concept["requirements_ids"],
        "architecture_id": concept["architecture_id"],
        "concept_id": concept["id"],
        "design_instance_id": concept["design_instance_id"],
    }
    mocked_job = ({"job": "data"}, {"stuff": "in file"})
    httpx_mock.add_response(
        url=f"{conceptev_url}/jobs?design_instance_id=123", match_json=job_input, json=mocked_job
    )
    mocked_info = "job info"
    mocked_job_start = {
        "job": mocked_job[0],
        "uploaded_file": mocked_job[1],
        "account_id": account_id,
        "hpc_id": hpc_id,
    }
    httpx_mock.add_response(
        url=f"{conceptev_url}/jobs:start?design_instance_id=123",
        match_json=mocked_job_start,
        json=mocked_info,
    )
    job_info = main.create_submit_job(client, concept, account_id, hpc_id, job_name)
    assert job_info == mocked_info


def test_put(httpx_mock: HTTPXMock, client: httpx.Client):
    example_aero = {"name": "aero_mock_response"}
    mocked_id = "345"
    httpx_mock.add_response(
        url=f"{conceptev_url}/configurations/{mocked_id}?design_instance_id=123",
        method="put",
        match_json=example_aero,
        json=example_aero,
    )

    results = main.put(client, "/configurations", mocked_id, example_aero)
    assert results == example_aero


def test_read_file(mocker):
    file_data = "Simple Data"
    mocked_file_data = mocker.mock_open(read_data=file_data)
    mocker.patch("builtins.open", mocked_file_data)
    results = main.read_file("filename")
    assert results == file_data


def test_read_results(httpx_mock: HTTPXMock, client: httpx.Client):
    example_job_info = {"job": "mocked_job"}
    example_results = {"results": "returned"}
    httpx_mock.add_response(
        url=f"{conceptev_url}/jobs:result?design_instance_id=123",
        method="post",
        match_json=example_job_info,
        json=example_results,
    )
    results = main.read_results(client, example_job_info)
    assert example_results == results


def test_post_file(mocker, httpx_mock: HTTPXMock, client: httpx.Client):
    file_data = "Simple Data"
    file_post_response_data = {"file": "read"}
    mocked_file_data = mocker.mock_open(read_data=file_data)
    mocker.patch("builtins.open", mocked_file_data)

    filename = "filename"
    params = {"param1": "one"}
    httpx_mock.add_response(
        url=f"{conceptev_url}/configurations:from_file?design_instance_id=123&param1=one",
        method="post",
        json=file_post_response_data,
    )

    result = main.post_component_file(client, "/configurations", filename, params)
    assert result == file_post_response_data
