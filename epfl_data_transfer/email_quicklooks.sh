#!/bin/bash

umask 002

# a script to email quicklooks from ltesrv5 to Alexis
# see the file email_quicklooks_setup.txt for information on how this works


# === Configuration ===
SUBJECT="AWACA quicklooks - $(date -d "yesterday" +%Y-%m-%d)"
BODY="Hello,

Please find attached the AWACA quicklooks for $(date -d "yesterday" +%Y-%m-%d). If a file is missing, it was not found on ltesrv5.

"

RECIPIENTS=("heather.corden@epfl.ch" "alexis.berne@epfl.ch")


YESTERDAY=$(date -d "yesterday" +%Y%m%d)
YEAR="${YESTERDAY:0:4}"
MONTH="${YESTERDAY:4:2}"
DAY="${YESTERDAY:6:2}"


# === Expected file patterns ===
CANDIDATE_FILES=(
    "/awaca/ddu/wprof/quicklooks/${YEAR}/${MONTH}/WProf_quicklook_${YESTERDAY}.png"
    "/awaca/ddu/stxpol/quicklooks/${YEAR}/${MONTH}/${DAY}/${YESTERDAY}_stxpol_zenith_day_DBZHC.png"
    "/awaca/ddu/mrr/quicklooks/${YEAR}/${MONTH}/${DAY}/${YESTERDAY}_mrr_zenith_day_ddu_Z.png"
    "/awaca/raid/d17/mira/quicklooks/${YEAR}/${MONTH}/${DAY}/${YESTERDAY}_mira_zenith_day_d17_Zg.png"
    "/awaca/raid/d17/mrr/quicklooks/${YEAR}/${MONTH}/${DAY}/${YESTERDAY}_mrr_zenith_day_d17_Z.png"
    "/awaca/raid/d47/mira/quicklooks/${YEAR}/${MONTH}/${DAY}/${YESTERDAY}_mira_zenith_day_d47_Zg.png"
    "/awaca/raid/d47/mrr/quicklooks/${YEAR}/${MONTH}/${DAY}/${YESTERDAY}_mrr_zenith_day_d47_Z.png"
    "/awaca/raid/d85/mrr/quicklooks/${YEAR}/${MONTH}/${DAY}/${YESTERDAY}_mrr_zenith_day_d85_Z.png"
    "/awaca/raid/dmc/mira/quicklooks/${YEAR}/${MONTH}/${DAY}/${YESTERDAY}_mira_zenith_day_dmc_Zg.png"
    "/awaca/raid/dmc/mrr/quicklooks/${YEAR}/${MONTH}/${DAY}/${YESTERDAY}_mrr_zenith_day_dmc_Z.png"   
)

# === Check which files exist ===
ATTACHMENTS=()
for FILE in "${CANDIDATE_FILES[@]}"; do
    echo $FILE
    if [[ -f "$FILE" ]]; then
        ATTACHMENTS+=("$FILE")
    fi
done

# Error if no attachments found
if [ ${#ATTACHMENTS[@]} -eq 0 ]; then
    echo "No files found for $YESTERDAY."
fi

# === Build mutt command ===
CMD=(mutt -s "$SUBJECT")
for ATTACH in "${ATTACHMENTS[@]}"; do
    CMD+=(-a "$ATTACH")
done
CMD+=(-- "${RECIPIENTS[@]}")

# === Send the email ===
"${CMD[@]}" <<< "$BODY"

