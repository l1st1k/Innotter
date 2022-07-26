#!/bin/sh
echo "some stuff ---------------------------------------------------------------"
celery -A Innotter worker -l info
