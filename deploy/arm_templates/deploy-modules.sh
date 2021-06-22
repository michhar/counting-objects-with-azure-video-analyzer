#!/usr/bin/env bash

#######################################################################################################
# This script is designed for use as a deployment script in a template
# https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/deployment-script-template
#
# It expects the following environment variables
# $DEPLOYMENT_MANIFEST_TEMPLATE_URL - the location of a template of an IoT Edge deployment manifest
# $PROVISIONING_TOKEN               - the token used for provisioing the edge module
# $HUB_NAME                         - the name of the IoT Hub where the edge device is registered
# $DEVICE_ID                        - the name of the edge device on the IoT Hub
# $DEVICE_IP                        - the local IP address of the edge device (Percept DK)
# $VIDEO_OUTPUT_FOLDER_ON_DEVICE    - the folder where the file sink will store clips
# $VIDEO_INPUT_FOLDER_ON_DEVICE     - the folder where where rtspsim will look for sample clips
# $APPDATA_FOLDER_ON_DEVICE         - the folder where Video Analyzer module will store state
# $AZURE_STORAGE_ACCOUNT            - the storage where the deployment manifest will be stored
# $AZ_SCRIPTS_OUTPUT_PATH           - file to write output (provided by the deployment script runtime) 
# $RESOURCE_GROUP                   - the resouce group that you are deploying in to
# $REGESTRY_PASSWORD                - the password for the container registry
# $REGISTRY_USER_NAME               - the user name for the container registry
# $IOT_HUB_CONNECTION_STRING        - the IoT Hub connection string
# $IOT_EDGE_MODULE_NAME             - the IoT avaedge module name
#
#######################################################################################################

# automatically install any extensions
az config set extension.use_dynamic_install=yes_without_prompt

# download the deployment manifest file
printf "downloading $DEPLOYMENT_MANIFEST_TEMPLATE_URL\n"
curl -s $DEPLOYMENT_MANIFEST_TEMPLATE_URL > deployment.json

# update the values in the manifest
printf "replacing value in manifest\n"
sed -i "s@\$AVA_PROVISIONING_TOKEN@${PROVISIONING_TOKEN}@g" deployment.json
sed -i "s@\$VIDEO_OUTPUT_FOLDER_ON_DEVICE@${VIDEO_OUTPUT_FOLDER_ON_DEVICE}@g" deployment.json
sed -i "s@\$VIDEO_INPUT_FOLDER_ON_DEVICE@${VIDEO_INPUT_FOLDER_ON_DEVICE}@g" deployment.json
sed -i "s@\$APPDATA_FOLDER_ON_DEVICE@${APPDATA_FOLDER_ON_DEVICE}@g" deployment.json

# Add a file to build env.txt file from
>env.txt
echo "SUBSCRIPTION_ID=$SUBSCRIPTION_ID" >> env.txt
echo "RESOUCE_GROUP=$RESOURCE_GROUP" >> env.txt
echo "AVA_PROVISIONING_TOKEN=$PROVISIONING_TOKEN">> env.txt
echo "VIDEO_INPUT_FOLDER_ON_DEVICE=$VIDEO_INPUT_FOLDER_ON_DEVICE">> env.txt
echo "VIDEO_OUTPUT_FOLDER_ON_DEVICE=$VIDEO_OUTPUT_FOLDER_ON_DEVICE" >> env.txt
echo "APPDATA_FOLDER_ON_DEVICE=$APPDATA_FOLDER_ON_DEVICE" >> env.txt
echo "CONTAINER_REGISTRY_PASSWORD_myacr=$REGISTRY_PASSWORD" >> env.txt
echo "CONTAINER_REGISTRY_USERNAME_myacr=$REGISTRY_USER_NAME" >> env.txt
>appsettings.json
echo "{" >> appsettings.json
echo "\"IoThubConnectionString\": \"$IOT_HUB_CONNECTION_STRING\"," >> appsettings.json
echo "\"deviceId\": \"$DEVICE_ID\"," >> appsettings.json
echo "\"moduleId\": \"$IOT_EDGE_MODULE_NAME\"" >> appsettings.json
echo "}" >> appsettings.json


# deploy the manifest to the iot hub
printf "deploying manifest to $DEVICE_ID on $HUB_NAME\n"
az iot edge set-modules --device-id $DEVICE_ID --hub-name $HUB_NAME --content deployment.json --only-show-error -o table

# store the manifest for later reference
printf "storing manifest for reference\n"
az storage share create --name deployment-output --account-name $AZURE_STORAGE_ACCOUNT
az storage file upload --share-name deployment-output --source deployment.json --account-name $AZURE_STORAGE_ACCOUNT
az storage file upload --share-name deployment-output --source env.txt --account-name $AZURE_STORAGE_ACCOUNT
az storage file upload --share-name deployment-output --source appsettings.json --account-name $AZURE_STORAGE_ACCOUNT

# set the CVR pipeline topology
printf "set the CVR topology pipeline\n"

wget https://raw.githubusercontent.com/Azure/video-analyzer/main/pipelines/live/topologies/cvr-video-sink/topology.json
wget https://raw.githubusercontent.com/michhar/counting-objects-with-azure-video-analyzer/main/deploy/arm_templates/operations.json
PIPELINE_TOPOLOGY="topology.json"
LIVE_PIPELINE_NAME="CVR-Pipeline"
PIPELINE_TOPOLOGY_NAME="CVRToVideoSink"

az iot hub invoke-module-method \
    -n "$HUB_NAME" \
    -d "$DEVICE_NAME" \
    -m avaedge \
    --mn pipelineTopologySet \
    --mp '{"@apiVersion": "1.0", "name": "'"$PIPELINE_TOPOLOGY"'", "properties": {}' \
	--timeout 120

# building rtsp url from DEVICE_IP var (input to script)
RTSP_URL="rtsp://$DEVICE_IP:8554/h264raw"

# shellcheck disable=2016
GRAPH_INSTANCE=$(< operations.json jq --arg replace_value "$RTSP_URL" '.properties.parameters[0].value = $replace_value' )

# set the CVR live pipeline
az iot hub invoke-module-method \
    -n "$HUB_NAME" \
    -d "$DEVICE_NAME" \
    -m avaedge \
    --mn livePipelineSet \
    --mp '{"@apiVersion": "1.0", "name": "'"$LIVE_PIPELINE_NAME"'", "properties": {}' \
    --timeout 120

# activate the CVR live pipeline
printf "activating AVA live pipeline"
INSTANCE_RESPONSE=$(az iot hub invoke-module-method \
    -n "$HUB_NAME" \
    -d "$DEVICE_NAME" \
    -m avaedge \
    --mn livePipelineActivate \
    --mp '{"@apiVersion" : "1.0", "name" : "'"$LIVE_PIPELINE_NAME"'"}')