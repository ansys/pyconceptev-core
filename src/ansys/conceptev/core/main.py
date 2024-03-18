"""A Simple API Client for ConceptEV."""
import datetime
from json import JSONDecodeError
import os
import time
from typing import Literal
import warnings

import dotenv
import httpx

dotenv.load_dotenv()

# Warning as this is not automated so changes to the API will cause changes here.
warnings.warn(
    "Warning: The API is in rapidly changing state and this may become " "out of date very quickly."
)

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
    """Get Token from OCM."""
    username = os.environ["CONCEPTEV_USERNAME"]
    password = os.environ["CONCEPTEV_PASSWORD"]
    ocm_url = os.environ["OCM_URL"]
    response = httpx.post(
        url=ocm_url + "/auth/login/", json={"emailAddress": username, "password": password}
    )
    if response.status_code != 200:
        raise Exception(f"Failed to get token {response.content}")
    return response.json()["accessToken"]


def get_http_client(token: str, design_instance_id: str | None = None) -> httpx.Client:
    """Get a http client.

    This http client creates and maintains the connection and is more performant than
    re-creating that connection for each call.
    """
    base_url = os.environ["CONCEPTEV_URL"]
    if design_instance_id:
        params = {"design_instance_id": design_instance_id}
    else:
        params = None
    return httpx.Client(headers={"Authorization": token}, params=params, base_url=base_url)


def processed_response(response) -> dict:
    """Process response.

    Check the return from the api and if it's not successful raise an error.
    """
    if response.status_code == 200 or response.status_code == 201:  # Success
        try:
            return response.json()
        except JSONDecodeError:
            return response.content
    raise Exception(f"Response Failed:{response.content}")


def get(
    client: httpx.Client, router: Router, id: str | None = None, params: dict | None = None
) -> dict:
    """Get/read from the client at the specific route.

    A http verb. Performs the get request adding the route to the base client.
    """
    if id:
        path = "/".join([router, id])
    else:
        path = router
    response = client.get(url=path, params=params)
    return processed_response(response)


def post(client: httpx.Client, router: Router, data: dict, params: dict = {}) -> dict:
    """Post/create from the client at the specific route.

    A http verb. Performs the post request adding the route to the base client.
    """
    response = client.post(url=router, json=data, params=params)
    return processed_response(response)


def delete(client: httpx.Client, router: Router, id: str) -> dict:
    """Delete from the client at the specific route.

    A http verb. Performs the delete request adding the route to the base client.
    """
    path = "/".join([router, id])
    response = client.delete(url=path)
    if response.status_code != 204:
        raise Exception(f"Failed to delete from {router} with id:{id}")


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
    if created_project.status_code != 200 and created_project.status_code != 204:
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

    if created_design.status_code != 200 and created_design.status_code != 204:
        raise Exception(f"Failed to create a design on OCM {created_design.content}")

    user_details = httpx.post(osm_url + "/user/details", headers={"Authorization": token})
    if user_details.status_code != 200 and user_details.status_code != 204:
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
    """Get Concept Ids."""
    concepts = get(client, "/concepts")
    return {concept["name"]: concept["id"] for concept in concepts}


def get_account_ids(token: str) -> dict:
    """Get account ids."""
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
    """Get default hpc id."""
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


def put(client: httpx.Client, router: Router, id: str, data: dict) -> dict:
    """Put/update from the client at the specific route.

    A http verb. Performs the put request adding the route to the base client.
    """
    path = "/".join([router, id])
    response = client.put(url=path, json=data)
    return processed_response(response)


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
    """Keep trying for results if the results aren't completed try again."""
    version_number = get(client, "/utilities:data_format_version")
    for i in range(0, no_of_tries):
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
    """Post/create from the client at the specific route with a file.

    A http verb. Performs the post request adding the route to the base client.
    Adds the file as a multipart form request.
    """
    path = "/components:upload"
    file_contents = read_file(filename)
    response = client.post(
        url=path, files={"file": file_contents}, params={"component_file_type": component_file_type}
    )
    return processed_response(response)


if __name__ == "__main__":
    token = get_token()

    with get_http_client(token) as client:  # Create a client to talk to the api
        health = get(client, "/health")  # Check the api is healthy
        print(health)
        concepts = get(client, "/concepts")  # Get a list of concepts
        print(concepts)
