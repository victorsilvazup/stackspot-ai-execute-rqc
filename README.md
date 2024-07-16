# stackspot-ai-execute-rqc

StackSpot AI Remote Quick Command Action

This action identifies all the files changed in some extension `FILE_EXTENSION` and pass to a [StackSpot AI remote quick command](https://ai.stackspot.com/docs/pt-br/quick-commands/create-remote-qc) and returns a JSON as answer (github action output) to be manipulated in future steps for customizable operations.

For this action to work, be sure you configured your [Remote Quick Command prompt on StackSpot AI](https://ai.stackspot.com/docs/pt-br/quick-commands/create-remote-qc) with a JSON object as output.

## 📚 Usage

```yaml
steps:
    - uses: actions/checkout@v4
      with: 
          fetch-depth: 2 # mandatory to detect changes in files

    - uses: victorsilvazup/stackspot-ai-execute-rqc@v1
      id: rqc
      with:
        CLIENT_ID: ${{ secrets.CLIENT_ID }}
        CLIENT_KEY: ${{ secrets.CLIENT_KEY }}
        CLIENT_REALM: ${{ secrets.CLIENT_REALM }}
        QC_SLUG: YOUR_REMOTE_QUICK_COMMAND_SLUG
        FILE_EXTENSION: YOUR_FILE_EXTENSION

    - name: Check Remote Quick Command answer
      run: echo ${{ toJSON(steps.rqc.outputs.rqc_result) }}
```

## ▶️ Action Inputs

Field | Mandatory | Default Value | Observation
------------ | ------------  | ------------- | -------------
**CLIENT_ID** | YES | N/A | [StackSpot](https://stackspot.com/en/settings/access-token) Client ID.
**CLIENT_KEY** | YES | N/A |[StackSpot](https://stackspot.com/en/settings/access-token) Client KEY.
**CLIENT_REALM** | YES | N/A |[StackSpot](https://stackspot.com/en/settings/access-token) Client Realm.
**QC_SLUG** | YES | N/A | [StackSpot Remote Quick Command reference](https://ai.stackspot.com/docs/pt-br/quick-commands/create-remote-qc)
**FILE_EXTENSION** | YES | N/A | The file extension you want to be detected changes and send to a Remote Quick Command

## ▶️ Action Output

Field | Observation
------------  | -------------
**rqc_result** | Can be accessed by using `${{ toJSON(steps.rqc.outputs.rqc_result) }}`

## 🏅 Licensed

☞ This repository uses the [Apache License 2.0](https://github.com/victorsilvazup/stackspot-ai-execute-rqc/blob/main/LICENSE)