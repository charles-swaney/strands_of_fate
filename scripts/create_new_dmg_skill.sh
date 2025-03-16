#!/bin/bash

SKILL_NAME=$1
CLASS_TYPE=$2
SUBDIR=$3

SKILL_NAME=$(echo "$SKILL_NAME" | sed -E 's/(^|_)([a-z])/\U\2/g' | sed -E 's/([A-Z])_([A-Z])/\1\2/g')
LOWERCASE_SKILL_NAME=$(echo "$SKILL_NAME" | tr '[:upper:]' '[:lower:]')

OUTPUT_FILE="src/combat/skills/$CLASS_TYPE/$SUBDIR/${LOWERCASE_SKILL_NAME}.py"

cat <<EOF > "$OUTPUT_FILE"
from actions.skill import Skill


class $SKILL_NAME(Skill):
    def __init__(self):
        """
        Describe the $SKILL_NAME skill.
        """
        super().__init__(
            name="TODO",
            cost_type="mp",
            base_cost=TODO,
            cost_scaling=TODO,
            cooldown=TODO,
            magnitude=TODO,
            element="TODO",
            skill_type="damage"
        )
        self.target_type="single"
EOF
