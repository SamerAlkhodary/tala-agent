#!/usr/bin/env sh
if [ -z "$KEYS_LOCATION" ]; then
	echo "KEYS_LOCATION variable is not set. Please set it to the directory where you want to store the keys."
	exit 1
fi

namespace=analytics-ai

kubectl exec deploy/{{template-agent}} -n $namespace -c service-kit-sidecar -- cat /var/run/secrets/qlik.com/{{template-agent}}-keys/service-key.yaml >"$KEYS_LOCATION"/service-key.yaml
