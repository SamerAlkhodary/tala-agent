#!/usr/bin/env sh
SOLACE_IP=$(kubectl get svc solace-pubsubplus -o jsonpath='{.spec.clusterIP}')
GSK_SIDECAR_IMAGE=ghcr.io/qlik-trial/gsk-sidecar:28.13.0
CONTAINER_NAME=analytics-psk-sidecar

echo "$SOLACE_IP"
echo "$KEYS_LOCATION"
docker pull $GSK_SIDECAR_IMAGE

if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
	docker rm -f "$CONTAINER_NAME"
fi

docker create \
	--name $CONTAINER_NAME \
	-e SIDECAR_DISABLE_AUTH=true \
	-e SOLACE_MESSAGE_VPN=QcsPrimary \
	-e SOLACE_SKIP_CERT_VALIDATION=true \
	-e SOLACE_URI="tcps://$SOLACE_IP:55443" \
	-v "$KEYS_LOCATION"/:/var/run/secrets/qlik.com/{{template-agent}}-keys \
	-p 50051:50051 \
	-p 50151:50151 \
	-p 50152:50152 \
	-p 50251:50251 \
	-p 50252:50252 \
	-p 50351:50351 \
	-p 50352:50352 \
	-p 50451:50451 \
	-p 50452:50452 \
	$GSK_SIDECAR_IMAGE
