import os
import json

def convert_to_sarif(input_json, output_file):
    print(f'input_json = {input_json}')
    sarif = {
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "StackSpot AI",
                        "informationUri": "https://ai.stackspot.com/docs/pt-br/quick-commands/create-remote-qc",
                        "rules": [],
                    }
                },
                "results": [],
            }
        ],
    }

    for result in input_json:
        print(f'result = {result}')
        file = result["file"]
        item = result["result"]
        sarif_result = {
            "ruleId": item["rule_id"],
            "message": {"text": item["correction"]},
            "locations": [
                {
                    "physicalLocation": {
                        "artifactLocation": {"uri": file},
                        "region": {"startLine": item["line"]},
                    }
                }
            ],
        }
        sarif["runs"][0]["results"].append(sarif_result)

    with open(output_file, "w") as f:
        json.dump(sarif, f, indent=2)
        
INPUT_JSON = os.getenv("INPUT_JSON")
convert_to_sarif(INPUT_JSON, "results.sarif")