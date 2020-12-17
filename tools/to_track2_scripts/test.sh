#!/bin/bash

python codegen.py --output-version=9.0.0b1 \
    --base-path=/_ \
    --service-name="Data Migration" \
    --swagger-name=datamigration \
    --sdk-set-name=datamigration \
    --package-name=datamigration \
    --mode=single
