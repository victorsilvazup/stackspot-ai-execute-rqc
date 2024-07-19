import os
import base64
import requests


def file_to_base64(file_path):
    with open(file_path, "rb") as file:
        file_content = file.read()
        base64_encoded = base64.b64encode(file_content).decode("utf-8")
    return base64_encoded


def save_output(name: str, value: str):
    with open(os.environ["GITHUB_OUTPUT"], "a") as output_file:
        print(f"{name}={value}", file=output_file)


def get_access_token(account_slug, client_id, client_key):
    url = f"https://idm.stackspot.com/{account_slug}/oidc/oauth/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "client_id": client_id,
        "grant_type": "client_credentials",
        "client_secret": client_key,
    }
    response = requests.post(url, headers=headers, data=data)
    response_data = response.json()
    return response_data["access_token"]


def create_rqc_execution(qc_slug, access_token, changed_files):
    for file_path in changed_files.split():
        base64_string = file_to_base64(file_path.strip())
        url = f"https://genai-code-buddy-api.stackspot.com/v1/quick-commands/create-execution/{qc_slug}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
        data = {"input_data": {"json": {"file": base64_string}}}

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            decoded_content = response.content.decode("utf-8")
            extracted_value = decoded_content.strip('"')
            response_data = extracted_value
            with open("execution_info.txt", "a") as f:
                f.write(f"{response_data},{file_path}\n")
        else:
            print(response.status_code)
            print(response.content)


def get_execution_status(file_path, access_token):
    result_final = []
    with open(file_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            execution_id, file_name = line.strip().split(",")
            print(f"Checking status for ID: {execution_id} and file: {file_name}")

            url = f"https://genai-code-buddy-api.stackspot.com/v1/quick-commands/callback/{execution_id}"
            headers = {"Authorization": f"Bearer {access_token}"}
            command_status = "RUNNING"
            while command_status == "RUNNING":
                response = requests.get(url, headers=headers)
                response_data = response.json()

                status = response_data["progress"]["status"]
                command_status = status

            if command_status == "COMPLETED":
                result = response_data["result"]
                if result.strip().startswith("```json"):
                    result = result[8:-4].strip()
                result_final.append({"file": file_name, "result": result})

            if command_status == "FAILED":
                result_final = response_data

    return result_final

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_KEY = os.getenv("CLIENT_KEY")
ACCOUNT_SLUG = os.getenv("CLIENT_REALM")
QC_SLUG = os.getenv("QC_SLUG")
CHANGED_FILES = os.getenv("CHANGED_FILES")

access_token = get_access_token(ACCOUNT_SLUG, CLIENT_ID, CLIENT_KEY)
execution_id = create_rqc_execution(QC_SLUG, access_token, CHANGED_FILES)
result_final = get_execution_status("execution_info.txt", access_token)

save_output("result", result_final)

print("\n\033[36mOutput saved successfully!\033[0m")
