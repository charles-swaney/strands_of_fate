#!/bin/bash

MONSTER_SPECIES=$1
SUBDIR=$2

MONSTER_NAME=$(echo "$MONSTER_SPECIES" | sed -E 's/(^|_)([a-z])/\U\2/g')
LOWERCASE_MONSTER_NAME=$(echo "$MONSTER_SPECIES" | tr '[:upper:]' '[:lower:]')

OUTPUT_FILE="src/jobs/$SUBDIR/${LOWERCASE_JOB_NAME}.py"