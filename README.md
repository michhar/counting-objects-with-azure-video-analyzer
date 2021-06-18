# Object Counting on the Percept DK with Azure Video Analyzer

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

## Data

Example output from Percept DK:

```json

```

## Troubleshooting

* _The module cannot access the path /var/lib/videoanalyzer/AmsApplicationData specified in the 'applicationDataDirectory' desired property._ This may occur due to previous deployments of AVA where the application data directory was populated with files.  To refresh this directory you will need to stop the iotedge daemon, delete and then recreate the directory as follows.

```
sudo systemctl stop iotedge
sudo rm -fr /var/lib/videoanalyzer/AmsApplicationData
sudo mkdir /var/lib/videoanalyzer/AmsApplicationData
sudo chown -R 1010:1010 /var/lib/videoanalyzer/
sudo systemctl start iotedge
```

> Note:  for newer iotedge daemons you may need to replace `iotedge` with `aziot-edged`.

## Credits and References

- [Plotly sample app](https://github.com/plotly/dash-sample-apps/tree/master/apps/dash-object-detection)
- [Azure Video Analyzer deployment](https://github.com/Azure/video-analyzer/tree/main/setup)
- [Azure Percept documentation](https://docs.microsoft.com/en-us/azure/azure-percept/)
- [Azure Video Analyzer documentation](https://docs.microsoft.com/en-us/azure/azure-video-analyzer/video-analyzer-docs/)
