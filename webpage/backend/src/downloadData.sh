#!/bin/bash
export $(grep -v '^#' .env | xargs)
curl -s -H "Authorization: token $TOKEN" \
    "https://api.github.com/repos/$REPO/actions/runs/$RUN_ID/artifacts" \
    | jq -r ".artifacts[] | select(.name == \"$ARTIFACT_NAME\") | .archive_download_url" > download_url.txt

DOWNLOAD_URL=$(cat download_url.txt)
if [ -n "$DOWNLOAD_URL" ]; then
    curl -L -H "Authorization: token $TOKEN" "$DOWNLOAD_URL" -o "$OUTPUT_FILE"
    echo "Archivo descargado como $OUTPUT_FILE"
rm "predicho.txt"
unzip "$OUTPUT_FILE"
rm "$OUTPUT_FILE" "download_url.txt"
else
    echo "No se encontró el artefacto $ARTIFACT_NAME"
fi
