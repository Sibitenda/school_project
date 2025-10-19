#!/bin/bash
echo " Running all Django + Cloud + Email tests..."
pytest -v --disable-warnings --maxfail=1
