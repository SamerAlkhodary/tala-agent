  #!/bin/bash

  if [ -z "$USER_ID" ]; then
    read -p "Enter USER_ID: " USER_ID
    export USER_ID
  fi
  if [ -z "$TENANT_ID" ]; then
    read -p "Enter TENANT_ID: " TENANT_ID
    export TENANT_ID
  fi
  if [ -z "$APP_ID" ]; then
    read -p "Enter APP_ID: " APP_ID
    export APP_ID
  fi
  echo "USER_ID: $USER_ID"
  echo "TENANT_ID: $TENANT_ID"
  echo "APP_ID: $APP_ID"
  docker restart analytics-psk-sidecar
  set -o allexport && source .env && set +o allexport
  python -m interactive
