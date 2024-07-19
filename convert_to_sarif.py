import os
import json

def convert_to_sarif(input_json, output_file):
    for item in input_json:
        item['result'] = item['result'].replace("\\n", '')
        
    json_array = json.loads(json.dumps(input_json))
    print(f'input = {json_array}')
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

    for result in json_array:
        print(f'result = {result}')
        file = result["file"]
        item = result["result"]
        item_json = json.loads(item)
        sarif_result = {
            "ruleId": item_json["rule_id"],
            "message": {"text": item_json["message"]},
            "locations": [
                {
                    "physicalLocation": {
                        "artifactLocation": {"uri": file},
                        "region": {"startLine": item_json["line"]},
                    }
                }
            ],
        }
        sarif["runs"][0]["results"].append(sarif_result)

    with open(output_file, "w") as f:
        json.dump(sarif, f, indent=2)
        
INPUT_JSON = os.getenv("INPUT_JSON")
convert_to_sarif(INPUT_JSON, "results.sarif")