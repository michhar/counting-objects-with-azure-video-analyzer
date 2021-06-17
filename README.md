# Object Counting on the Percept DK with Azure Video Analyzer

## Prerequisites

- Python 3.6+ (preferably an Anaconda release)

## What gets deployed

- Azure Video Analyzer account and dependent services (Storage, Media Services, etc.)
- App Service (for web app)
- IoT Hub

### Set up Azure resources

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

## Data

Example output from Percept DK:

```json

```

## Credits and References

- [Plotly sample app](https://github.com/plotly/dash-sample-apps/tree/master/apps/dash-object-detection)
- [Azure Video Analyzer deployment](https://github.com/Azure/video-analyzer/tree/main/setup)
