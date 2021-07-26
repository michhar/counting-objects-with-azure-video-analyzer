# Edge Deployment, Redeployment and Reset

Use this information and folder if you wish to redeploy the edge modules of this solution or reset the edge modules to what comes with the Percept DK (mainly for degugging).

You may also change the ML model used to another - either [prebuilt (object detectors only)](https://github.com/microsoft/azure-percept-advanced-development#model-urls) or [custom built](https://github.com/microsoft/azure-percept-advanced-development/tree/main/machine-learning-notebooks/transfer-learning-custom-azureml).

## Contents of the `arm_templates` folder

The "Deploy to Azure" button uses these files under the hood.  It can be useful to understand what is happening when one clicks the button.

| File | Description |
| --- | --- |
| deploy-modules.sh | This script is used to deploy the IoT Edge modules to the IoT Edge device based off of the deployment manifest (general-sample-setup.modules.json) |
| form.json | custom deployment form used in Azure Portal |
| general-sample-setup-modules.json | Azure IoT Edge deployment manifest |
| iot-edge-setup.sh | Checks to see if an existing Edge device exist, if not it creates a new Edge device and captures the connection string. |
| iot.deploy.json | Deploys an IoT Hub |
| live-pipeline-set.json | Json payload to set the live pipeline |
| prepare-device.sh | Configures the IoT Edge device with the required user and folder structures. |
| start.deploy.json | Master template and controls the flow between the rest of the deployment templates |
| video-analyzer.deploy.json | Deploys storage, identities, and the Azure Video Analyzer resources. |

- [Original source](https://github.com/Azure/video-analyzer/tree/main/setup)

If wishing to deactivate the live pipeline with the Azure CLI, log in with the Azure CLI on the command line and run:

```
az iot hub invoke-module-method \
    -n "<IoT Hub name>" \
    -d "<device id/name>" \
    -m avaedge \
    --mn livePipelineDeactivate \
    --mp '{"@apiVersion": "1.0", "name": "CVR-Pipeline"}'
```

> Note, the video in the AVA resource may need to be deleted (can be done in Azure Portal) before it can be activated again.

To reactivate the live pipeline:

```
az iot hub invoke-module-method \
    -n "<IoT Hub name>" \
    -d "<device id/name>" \
    -m avaedge \
    --mn livePipelineActivate \
    --mp '{"@apiVersion": "1.0", "name": "CVR-Pipeline"}'
```

## Contents of `edge` folder

The contents of this folder are for debugging.

| File | Description |
| --- | --- |
| deployment.ava.percept.template.json | Deploy or redeploy the edge modules of this AVA solution |
| deployment.reset.percept.template.json | Reset the modules on the Percept DK to original "factory" experience; often useful to perform before you wish to redeploy the AVA solution modules |

If you wish to try a different ML model, either [prebuilt - object detectors only](https://github.com/microsoft/azure-percept-advanced-development#model-urls) or [custom built](https://github.com/microsoft/azure-percept-advanced-development/tree/main/machine-learning-notebooks/transfer-learning-custom-azureml)), change the `ModelZipUrl` in `deployment.ava.percept.template.json` as shown below.

```json
 "azureeyemodule": {
        "properties.desired": {
            "Logging": true,
            "ModelZipUrl": "<change this url to a different zipped model file url>",
            "RawStream": true,
            "ResultStream": true,
            "Running": true,
            "TelemetryInterval": 10
        }
    }
```

### Setup for edge

Note: if using a private ACR for the http simpleserver, look at `deployment.ava.percept.myacr.template.json` and fill in the following with the appropriate values for your ACR.

In the manifest (for private ACR):

```json
            "registryCredentials": {
              "$CONTAINER_REGISTRY_USERNAME_myacr": {
                "username": "$CONTAINER_REGISTRY_USERNAME_myacr",
                "password": "$CONTAINER_REGISTRY_PASSWORD_myacr",
                "address": "$CONTAINER_REGISTRY_USERNAME_myacr.azurecr.io"
              }
            }
```

In the `.env` you created (for private ACR):

```
CONTAINER_REGISTRY_USERNAME_myacr=<optional>
CONTAINER_REGISTRY_PASSWORD_myacr=<optional>
```

Then use `deployment.ava.percept.myacr.template.json` to deploy AVA solution.

### Using VSCode to deploy edge modules

Use VSCode as in [this section](https://docs.microsoft.com/en-us/azure/azure-video-analyzer/video-analyzer-docs/detect-motion-emit-events-quickstart?pivots=programming-language-python#generate-and-deploy-the-deployment-manifest) to deploy the modules to the Percept DK with the above files.

> Note: there are other ways to deploy edge modules such as with the Azure CLI

## Resources


