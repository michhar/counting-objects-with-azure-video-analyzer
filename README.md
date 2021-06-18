# Object Counting on the Percept DK with Azure Video Analyzer

The goal of this project is to be able to recognize objects found on the edge with the Percept DK device and Vision SoM camera.  Additionally, video is saved to the cloud with Azure Video Analyzer when invoking methods that directly communicate with the edge device for continuous recording.

This repo is under rapid iterations and will be updating often.  Currently it offers:

* Process to deploy Azure Video Analyzer (and Azure resources), plus edge modules, to the Percept DK
* Python console app to be run on dev/local machine that starts and stops video recording to the cloud

Work in progress:

* Cloud web app/dashboard to view video and object counts (plus control AVA)

## Prerequisites

- Python 3.6+ (preferably an [Anaconda](https://docs.anaconda.com/anaconda/index.html) release)
- Percept DK ([Purchase](https://www.microsoft.com/en-us/store/build/azure-percept/8v2qxmzbz9vc))

## Device setup

1. Follow [Quickstart: unbox and assemble your Azure Percept DK components](https://docs.microsoft.com/en-us/azure/azure-percept/quickstart-percept-dk-unboxing) and the next steps.

## Deploy Azure resources

> NOTE: Things like VM availability in the selected region will cause the deployment to fail.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fmichhar%2Fcounting-objects-with-azure-video-analyzer%2Fmain%2Fdeploy%2Farm_templates%2Fstart.deploy.json/createUIDefinitionUri/https%3A%2F%2Fraw.githubusercontent.com%2Fmichhar%2Fcounting-objects-with-azure-video-analyzer%2Fmain%2Fdeploy%2Farm_templates%2Fform.json)

After the script finishes you will have the following Azure resources:

- [IoT Hub](https://docs.microsoft.com/azure/iot-hub/about-iot-hub)
- [Virtual Machine (virtual Edge device)](https://docs.microsoft.com/azure/virtual-machines/)
  - [Network interface](https://docs.microsoft.com/rest/api/virtualnetwork/networkinterfaces)
  - [Disk](https://docs.microsoft.com/azure/virtual-machines/managed-disks-overview)
  - [Network security group](https://docs.microsoft.com/azure/virtual-network/network-security-groups-overview)
  - [Public IP address (if the Bastion option was not set)](https://docs.microsoft.com/azure/virtual-network/public-ip-addresses)
- [Virtual network](https://docs.microsoft.com/azure/virtual-network/virtual-networks-overview)
- [Storage account](https://docs.microsoft.com/azure/storage/common/storage-account-overview) 
- [Azure Video Analyzer](https://docs.microsoft.com/azure/azure-video-analyzer/overview)
- [Managed Identities](https://docs.microsoft.com/azure/active-directory/managed-identities-azure-resources/overview)
- [Bastion Host (if the Bastion option was set)](https://docs.microsoft.com/azure/bastion/)

## Python setup

1. If using Anaconda Python (recommended) [setup a conda environment](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html), otherwise, [use `venv`](https://docs.python.org/3/library/venv.html) to create a nuclear environment for this solution.
2. Install the Python dependencies as follows.

```
pip install -r requirements.txt
```

## Getting started

After deploying the resources in Azure as done above (by using the "Deploy to Azure" button), refer to the next steps as follows.

* [AVA cloud to device sample console app](ava_app/)

And if needing to deploy or redeploy from a manifest or get more information on the deployment process, go to the following folder.
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
