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

# # Simple workflow
#
# This example shows how to use PyConcentEV to perform basic operations.

# ## Perform required imports
#
# Perform required imports.

# +
import datetime
import os
from pathlib import Path

import plotly.graph_objects as go

from ansys.conceptev.core import app

# -

# ## Set up environment variables

# Set up required environment variables.

# +
os.environ["CONCEPTEV_URL"] = "https://conceptev.ansys.com/api/"
os.environ["OCM_URL"] = "https://prod.portal.onscale.com/api"

# Set environment variables for ConceptEV username and password if they don't exist!
if os.environ.get("CONCEPTEV_USERNAME") is None:
    os.environ["CONCEPTEV_USERNAME"] = "joe.blogs@my_work.com"
if os.environ.get("CONCEPTEV_PASSWORD") is None:
    os.environ["CONCEPTEV_PASSWORD"] = "sup3r_s3cr3t_passw0rd"
# -

# +
# Uncomment the following lines of code if you want to use a local ``.env`` file.
#
# import dotenv
# dotenv.load_dotenv()
# -

# ## Define example data
#
# You can obtain example data from the schema sections of the API documentation.

# +
MOTOR_FILE_NAME = Path("resources") / "e9.lab"

AERO_1 = {
    "name": "New Aero Config",
    "drag_coefficient": 0.3,
    "cross_sectional_area": 2,
    "config_type": "aero",
}

AERO_2 = {
    "name": "Second Aero Configuration",
    "drag_coefficient": 0.6,
    "cross_sectional_area": 3,
    "config_type": "aero",
}

MASS = {
    "name": "New Mass Config",
    "mass": 3000,
    "config_type": "mass",
}

WHEEL = {
    "name": "New Wheel Config",
    "rolling_radius": 0.3,
    "config_type": "wheel",
}

TRANSMISSION = {
    "gear_ratios": [5],
    "headline_efficiencies": [0.95],
    "max_torque": 500,
    "max_speed": 2000,
    "static_drags": [0.5],
    "friction_ratios": [60],
    "windage_ratios": [40],
    "component_type": "TransmissionLossCoefficients",
}

BATTERY = {
    "capacity": 86400000,
    "charge_acceptance_limit": 0,
    "component_type": "BatteryFixedVoltages",
    "internal_resistance": 0.1,
    "name": "New Battery",
    "voltage_max": 400,
    "voltage_mid": 350,
    "voltage_min": 300,
}

motor_data = {"name": "e9", "component_type": "MotorLabID", "inverter_losses_included": False}
# -

# ## Use API client for the Ansys ConceptEV service

# ### Get a token from OCM

token = app.get_token()

# ### Create a project

with app.get_http_client(token) as client:
    health = app.get(client, "/health")
    print(f"API is healthy: {health}\n")

    concepts = app.get(client, "/concepts")
    print(f"List of concepts: {concepts}\n")

    accounts = app.get_account_ids(token)
    # Uncomment to print accounts IDs
    # print(f"Account IDs: {accounts}\n")

    account_id = accounts[os.environ["CONCEPTEV_USERNAME"]]
    hpc_id = app.get_default_hpc(token, account_id)
    # Uncomment to print HPC ID
    # print(f"HPC ID: {hpc_id}\n")

    project = app.create_new_project(
        client, account_id, hpc_id, f"New Project +{datetime.datetime.now()}"
    )
    print(f"ID of the created project: {project['id']}")

# ### Perform basic operations
#
# Perform basic operations on the design instance associated with the new project.

# +
design_instance_id = project["design_instance_id"]

with app.get_http_client(token, design_instance_id) as client:

    # Create configurations
    created_aero = app.post(client, "/configurations", data=AERO_1)
    created_aero2 = app.post(client, "/configurations", data=AERO_2)
    created_mass = app.post(client, "/configurations", data=MASS)
    created_wheel = app.post(client, "/configurations", data=WHEEL)

    # Read all aero configurations
    configurations = app.get(client, "/configurations", params={"config_type": "aero"})
    # Uncomment to print configurations
    # print(f"List of configurations: {configurations}\n")

    # Get a specific aero configuration
    aero = app.get(client, "/configurations", id=created_aero["id"])
    print(f"First created areo configuration: {aero}\n")

    # Create component
    created_transmission = app.post(client, "/components", data=TRANSMISSION)

    # Create component from file
    motor_loss_map = app.post_component_file(client, MOTOR_FILE_NAME, "motor_lab_file")
    motor_data["data_id"] = motor_loss_map[0]
    motor_data["max_speed"] = motor_loss_map[1]

    created_motor = app.post(client, "/components", data=motor_data)
    print(f"Created motor: {created_motor}\n")

    # Extend client timeout to get loss map from the motor
    client.timeout = 2000
    motor_loss_map = app.post(
        client,
        "/components:get_display_data",
        data={},
        params={"component_id": created_motor["id"]},
    )

    # Show a figure of the loss map from the motor in you browser
    x = motor_loss_map["currents"]
    y = motor_loss_map["phase_advances"]
    z = motor_loss_map["losses_total"]
    fig = go.Figure(data=go.Contour(x=x, y=y, z=z))
    fig.show()

    created_battery = app.post(client, "/components", data=BATTERY)

    # Create an architecture
    architecture = {
        "number_of_front_wheels": 1,
        "number_of_front_motors": 1,
        "front_transmission_id": created_transmission["id"],
        "front_motor_id": created_motor["id"],
        "number_of_rear_wheels": 0,
        "number_of_rear_motors": 0,
        "battery_id": created_battery["id"],
    }
    created_arch = app.post(client, "/architectures", data=architecture)
    print(f"Created architecture: {created_arch}\n")

    # Create a requirement
    requirement = {
        "speed": 10,
        "acceleration": 1,
        "aero_id": created_aero["id"],
        "mass_id": created_mass["id"],
        "wheel_id": created_wheel["id"],
        "state_of_charge": 0.9,
        "requirement_type": "static_acceleration",
        "name": "Static Requirement 1",
    }
    created_requirement = app.post(client, "requirements", data=requirement)
    print(f"Created requirement: {created_requirement}")
# -

# Submit a job and show the result.

with app.get_http_client(token, design_instance_id) as client:

    # Create and submit a job
    concept = app.get(client, "/concepts", id=design_instance_id, params={"populated": True})
    job_info = app.create_submit_job(client, concept, account_id, hpc_id)

    # Read the results and show the result in your browser
    results = app.read_results(client, job_info, calculate_units=False)
    x = results[0]["capability_curve"]["speeds"]
    y = results[0]["capability_curve"]["torques"]

    fig = go.Figure(data=go.Scatter(x=x, y=y))
    fig.show()
