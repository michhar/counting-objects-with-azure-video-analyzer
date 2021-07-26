# Object Counting on the Percept DK with Azure Video Analyzer

The goal of this project is to be able to recognize objects found on the edge with the Percept DK device and Vision SoM camera using Azure Video Anlyzer (AVA) as the platform.  Additionally, video is saved to the cloud with AVA when invoking methods that directly communicate with the edge device for continuous recording (default when using the "Deploy to Azure" button below).

This repo is under rapid iterations and will be updating often.  Currently it offers:

* Process to deploy Azure Video Analyzer (and Azure resources), plus edge modules, to the Percept DK and initiate cloud recording
* [Optional] Python console app in the `ava_app` folder (for debugging) to be run on dev/local machine that starts and stops video recording to the cloud
* [Optional] Deployment manifests in the `deploy/edge` folder to reset the Percept DK to original modules or redeploy the AVA pipeline (for debugging)

Work in progress:

* Cloud web app/dashboard to view video and object counts (plus control AVA)

## Prerequisites

- Percept DK ([Purchase](https://www.microsoft.com/en-us/store/build/azure-percept/8v2qxmzbz9vc))
- Azure Subscription - [Free trial account](https://azure.microsoft.com/en-us/free/)
- [Optional - for debugging] Python 3.6+ (preferably an [Anaconda](https://docs.anaconda.com/anaconda/index.html) release)

## Device setup

1. Follow [Quickstart: unbox and assemble your Azure Percept DK components](https://docs.microsoft.com/en-us/azure/azure-percept/quickstart-percept-dk-unboxing) and the next steps.

## Deploy Azure resources and begin streaming video

> Important: The following "Deploy to Azure" button will provision the Azure resources listed below and you will begin incurring costs associated with your network and Azure resources immediately as this solution faciliates continuous video recording to the cloud.  To calculate the potential costs, you may wish to use the [pricing calculator](https://azure.microsoft.com/en-us/pricing/calculator/) before you begin and/or have a plan to test in a single resource group that may be deleted after the testing is over.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fmichhar%2Fcounting-objects-with-azure-video-analyzer%2Fmain%2Fdeploy%2Farm_templates%2Fstart.deploy.json/createUIDefinitionUri/https%3A%2F%2Fraw.githubusercontent.com%2Fmichhar%2Fcounting-objects-with-azure-video-analyzer%2Fmain%2Fdeploy%2Farm_templates%2Fform.json)

After the script finishes you will have the following Azure resources in a new Resource Group in addition to your existing IoT Hub you specified:

- [Storage Account](https://docs.microsoft.com/azure/storage/common/storage-account-overview) 
- [Azure Video Analyzer](https://docs.microsoft.com/azure/azure-video-analyzer/overview)
  - With an active pipeline for video recording running
- [Container Registry](https://docs.microsoft.com/en-us/azure/container-registry/)
- [Managed Identities](https://docs.microsoft.com/azure/active-directory/managed-identities-azure-resources/overview)

> **IMPORTANT**:  To be able to redeploy the AVA modules, you should keep the AVA Provisioning Token for your records (this can not be found after redeploying with alternative deployment manifests).  After deployment, go to the specified IoT Hub (probably in a different resource group) --> IoT Edge --> your device name --> avaedge Module --> Module Identity Twin --> in "properties" --> "desired" --> copy and save "ProvisioningToken".

View the videos by going to the [Azure Portal](https://portal.azure.com) --> select your AVA resource group --> select Video Analyzer --> go to Videos --> select "sample-http-extension" and wait for the live stream to appear.  It may take 1-2 minutes for a live video stream to appear in the Azure Portal under AVA Videos after the deployment is complete.

## Optional steps (WIP)

After deploying the resources in Azure as done above (by using the "Deploy to Azure" button), refer to the next steps as follows.

### Python setup

1. If using Anaconda Python (recommended) [setup a conda environment](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html), otherwise, [use `venv`](https://docs.python.org/3/library/venv.html) to create a nuclear environment for this solution.
2. Install the Python dependencies as follows.

```
pip install -r requirements.txt
```

3.  Follow [AVA cloud to device sample console app](ava_app/) instructions.

### Edge reset or redeploy

For debugging and understanding futher, to deploy or redeploy from a manifest or get more information on the deployment process, go to the following folder.
* [Edge Deployment, Redeployment and Reset](deploy/)

## Data

Example output from Percept DK (coming soon).

```json

```

## Troubleshooting

* See the [Azure Video Analyzer Troubleshooting page](https://docs.microsoft.com/en-us/azure/azure-video-analyzer/video-analyzer-docs/troubleshoot).

* _The module cannot access the path /var/lib/videoanalyzer/AmsApplicationData specified in the 'applicationDataDirectory' desired property._ This may occur due to previous deployments of AVA where the application data directory was populated with files.  To refresh this directory you will need to stop the iotedge daemon, delete and then recreate the directory as follows.

```
sudo systemctl stop iotedge
sudo rm -fr /var/lib/videoanalyzer/AmsApplicationData
sudo mkdir /var/lib/videoanalyzer/AmsApplicationData
sudo chown -R 1010:1010 /var/lib/videoanalyzer/
sudo systemctl start iotedge
```

> Note:  for newer iotedge daemons you may need to replace `iotedge` with `aziot-edged`.

## Credits and references

- [Plotly sample app](https://github.com/plotly/dash-sample-apps/tree/master/apps/dash-object-detection)
- [Azure Video Analyzer deployment](https://github.com/Azure/video-analyzer/tree/main/setup)
- [AVA Python sample app](https://github.com/Azure-Samples/video-analyzer-iot-edge-python)
- [Azure Percept documentation](https://docs.microsoft.com/en-us/azure/azure-percept/)
- [Azure Video Analyzer documentation](https://docs.microsoft.com/en-us/azure/azure-video-analyzer/video-analyzer-docs/)

## Additional notes

The Vision SoM on the Percept DK returns json in the format:

```json
{
  "NEURAL_NETWORK": [
    {
      "bbox": [0.404, 0.369, 0.676, 0.984],
      "label": "person",
      "confidence": "0.984375",
      "timestamp": "1626991877400034126"
    }
  ]
}
```

Here, with the simple http server, we sync it in the correct format for AVA.