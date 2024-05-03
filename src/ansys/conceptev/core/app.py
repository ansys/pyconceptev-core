# Copyright (C) 2023 - 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""A Simple API Client for ConceptEV."""

import datetime
from json import JSONDecodeError
import os
import time
from typing import Literal, Optional

import dotenv
import httpx

dotenv.load_dotenv()

Router = Literal[
    "/architectures",
    "/components",
    "/components:from_file",
    "/components:calculate_loss_map",
    "/configurations",
    "/configurations:calculate_forces",
    "/requirements",
    "/requirements:calculate_examples",
    "/jobs",
    "/jobs:start",
    "/jobs:status",
    "/jobs:result",
    "/concepts",
    "/drive_cycles",
    "/drive_cycles:from_file",
    "/health",
    "/utilities:data_format_version",
]


def get_token() -> str:
    """Get token from OCM."""
    username = os.environ["CONCEPTEV_USERNAME"]
    password = os.environ["CONCEPTEV_PASSWORD"]
    ocm_url = os.environ["OCM_URL"]
    response = httpx.post(
        url=ocm_url + "/auth/login/", json={"emailAddress": username, "password": password}
    )
    if response.status_code != 200:
        raise Exception(f"Failed to get token {response.content}")
    return response.json()["accessToken"]


def get_http_client(token: str, design_instance_id: Optional[str] = None) -> httpx.Client:
    """Get a HTTP client.

    This HTTP client creates and maintains the connection with the server.
    Using this client is more performant than re-creating the connection for each call.
    """
    base_url = os.environ["CONCEPTEV_URL"]
    params = None
    if design_instance_id:
        params = {"design_instance_id": design_instance_id}
    return httpx.Client(headers={"Authorization": token}, params=params, base_url=base_url)


def process_response(response) -> dict:
    """Process a response.

    Check the return from the API and raise an error if it is not successful.
    """
    if response.status_code == 200 or response.status_code == 201:  # Success
        try:
            return response.json()
        except JSONDecodeError:
            return response.content
    raise Exception(f"Response Failed:{response.content}")


def get(
    client: httpx.Client, router: Router, id: Optional[str] = None, params: Optional[dict] = None
) -> dict:
    """Send a GET request to the base client.

    Perform a GET request to the API endpoint associated with the provided router.
    """
    if id:
        path = "/".join([router, id])
    else:
        path = router
    response = client.get(url=path, params=params)
    return process_response(response)


def post(client: httpx.Client, router: Router, data: dict, params: dict = {}) -> dict:
    """Send a POST request to the base client.

    Perform a POST request to the API endpoint associated with the provided router.
    """
    response = client.post(url=router, json=data, params=params)
    return process_response(response)


def delete(client: httpx.Client, router: Router, id: str) -> dict:
    """Send a DELETE request to the base client.

    Perform a DELETE request to the API endpoint associated with the provided router.
    """
    path = "/".join([router, id])
    response = client.delete(url=path)
    if response.status_code != 204:
        raise Exception(f"Failed to delete from {router} with id: {id}")


def put(client: httpx.Client, router: Router, id: str, data: dict) -> dict:
    """Send a PUT request to the base client.

    Perform a PUT request to the API endpoint associated with the provided router.
    """
    path = "/".join([router, id])
    response = client.put(url=path, json=data)
    return process_response(response)


def create_new_project(
    client: httpx.Client,
    account_id: str,
    hpc_id: str,
    title: str,
    project_goal: str = "Created from the CLI",
):
    """Create a new project."""
    osm_url = os.environ["OCM_URL"]
    token = client.headers["Authorization"]
    project_data = {
        "accountId": account_id,
        "hpcId": hpc_id,
        "projectTitle": title,
        "projectGoal": project_goal,
    }
    created_project = httpx.post(
        osm_url + "/project/create", headers={"Authorization": token}, json=project_data
    )
    if created_project.status_code not in (200, 204):
        raise Exception(f"Failed to create a project on OCM {created_project}")

    product_ids = httpx.get(osm_url + "/product/list", headers={"Authorization": token})
    product_id = [
        product["productId"]
        for product in product_ids.json()
        if product["productName"] == "CONCEPTEV"
    ][0]

    design_data = {
        "projectId": created_project.json()["projectId"],
        "productId": product_id,
        "designTitle": "Branch 1",
    }
    created_design = httpx.post(
        osm_url + "/design/create", headers={"Authorization": token}, json=design_data
    )

    if created_design.status_code not in (200, 204):
        raise Exception(f"Failed to create a design on OCM {created_design.content}")

    user_details = httpx.post(osm_url + "/user/details", headers={"Authorization": token})
    if user_details.status_code not in (200, 204):
        raise Exception(f"Failed to get a user details on OCM {user_details}")

    concept_data = {
        "capabilities_ids": [],
        "components_ids": [],
        "configurations_ids": [],
        "design_id": created_design.json()["designId"],
        "design_instance_id": created_design.json()["designInstanceList"][0]["designInstanceId"],
        "drive_cycles_ids": [],
        "jobs_ids": [],
        "name": "Branch 1",
        "project_id": created_project.json()["projectId"],
        "requirements_ids": [],
        "user_id": user_details.json()["userId"],
    }

    created_concept = post(client, "/concepts", data=concept_data)
    return created_concept


def get_concept_ids(client: httpx.Client):
    """Get concept IDs."""
    concepts = get(client, "/concepts")
    return {concept["name"]: concept["id"] for concept in concepts}


def get_account_ids(token: str) -> dict:
    """Get account IDs."""
    ocm_url = os.environ["OCM_URL"]
    response = httpx.post(url=ocm_url + "/account/list", headers={"authorization": token})
    if response.status_code != 200:
        raise Exception(f"Failed to get accounts {response}")
    accounts = {
        account["account"]["accountName"]: account["account"]["accountId"]
        for account in response.json()
    }
    return accounts


def get_default_hpc(token: str, account_id: str):
    """Get default HPC ID."""
    ocm_url = os.environ["OCM_URL"]
    response = httpx.post(
        url=ocm_url + "/account/hpc/default",
        json={"accountId": account_id},
        headers={"authorization": token},
    )
    if response.status_code != 200:
        raise Exception(f"Failed to get accounts {response}")
    return response.json()["hpcId"]


def create_submit_job(
    client,
    concept: dict,
    account_id: str,
    hpc_id: str,
    job_name: str = "cli_job: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
):
    """Create and then submit a job."""
    job_input = {
        "job_name": job_name,
        "requirement_ids": concept["requirements_ids"],
        "architecture_id": concept["architecture_id"],
        "concept_id": concept["id"],
        "design_instance_id": concept["design_instance_id"],
    }
    job, uploaded_file = post(client, "/jobs", data=job_input)
    job_start = {
        "job": job,
        "uploaded_file": uploaded_file,
        "account_id": account_id,
        "hpc_id": hpc_id,
    }
    job_info = post(client, "/jobs:start", data=job_start)
    return job_info


def read_file(filename: str) -> str:
    """Read file."""
    with open(filename) as f:
        content = f.read()
    return content


def read_results(
    client,
    job_info: dict,
    calculate_units: bool = True,
    no_of_tries: int = 200,
    rate_limit: float = 0.3,
) -> dict:
    """Read job results.

    Continuously request job results until a valid response is received or a limit of tries is
    reached.
    """
    version_number = get(client, "/utilities:data_format_version")
    for _ in range(0, no_of_tries):
        response = client.post(
            url="/jobs:result",
            json=job_info,
            params={
                "results_file_name": f"output_file_v{version_number}.json",
                "calculate_units": calculate_units,
            },
        )
        time.sleep(rate_limit)
        if response.status_code == 200:
            return response.json()

    raise Exception(f"To many request: {response}")


def post_component_file(client: httpx.Client, filename: str, component_file_type: str) -> dict:
    """Send a POST request to the base client with a file.

    Perform a POST request to add a file.
    """
    path = "/components:upload"
    file_contents = read_file(filename)
    response = client.post(
        url=path, files={"file": file_contents}, params={"component_file_type": component_file_type}
    )
    return process_response(response)


if __name__ == "__main__":
    token = get_token()

    with get_http_client(token) as client:  # Create a client to talk to the api
        health = get(client, "/health")  # Check that the api is healthy
        print(health)
        concepts = get(client, "/concepts")  # Get a list of concepts
        print(concepts)
