#!/usr/bin/env bash

/start-data-processing-service.sh &
tail -F anything
