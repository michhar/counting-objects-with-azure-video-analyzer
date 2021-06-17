# AVA cloud to device sample console app

This directory contains a Python sample app that would enable you to invoke AVA on IoT Edge Direct Methods in a sequence and with parameters, defined by you in a JSON file (operations.json)

## Contents

| File/folder             | Description                                                   |
|-------------------------|---------------------------------------------------------------|
| `readme.md`             | This README file.                                             |
| `operations.json`       | JSON file defining the sequence of operations to execute upon.|
| `main.py`               | The main program file                                         |
| `requirements.txt`      | List of all dependent Python libraries                        |


## Setup

Create a file named `appsettings.json` in this folder. Add the following text and provide values for all parameters.

```JSON
{
    "IoThubConnectionString" : "<your iothub connection string>",
    "deviceId" : "<device ID>",
    "moduleId" : "avaedge"
}
```

* **IoThubConnectionString** - Refers to the connection string of your IoT hub. This should have registry write and service connect access.
* **deviceId** - Refers to your IoT Edge device ID (registered with your IoT hub)
* **moduleId** - Refers to the module id of Azure Video Analyzer edge module (when deployed to the IoT Edge device)




## Running the sample from Visual Studio Code

Detailed instructions for running the sample can be found in the tutorials for AVA on IoT Edge. Below is a summary of key steps. Make sure you have installed the required prerequisites.

* Open your local clone of this git repository in Visual Studio Code, have the [Azure Iot Tools](https://marketplace.visualstudio.com/items?itemName=vsciot-vscode.azure-iot-tools) extension installed. 
* Right click on src/edge/deployment.template.json and select **“Generate Iot Edge deployment manifest”**. This will create an IoT Edge deployment manifest file in src/edge/config folder named deployment.amd64.json.
* Right click on src/edge/config /deployment.amd64.json and select **"Create Deployment for single device"** and select the name of your edge device. This will trigger the deployment of the IoT Edge modules to your Edge device. You can view the status of the deployment in the Azure IoT Hub extension (expand 'Devices' and then 'Modules' under your IoT Edge device).
* Right click on your edge device in Azure IoT Hub extension and select **"Start Monitoring Built-in Event Endpoint"**.
* Install python dependencies from `requirements.txt`. This can be done by running `pip install -r requirements.txt`.
* Select the "Cloud to Device - Console App" configuration in the run tab and start a debugging session (hit F5). You will start seeing some messages printed in the TERMINAL window. In the OUTPUT window, you will see messages that are being sent to the IoT Hub, by the AVAEdge module.

❗**Note:** *When running the debugger with the app project, the default launch.json creates a configuration with the parameter "console": "internalConsole". This does not work since internalConsole does not allow keyboard input. Changing the parameter to "console" : "integratedTerminal" fixes the problem.*

## Troubleshooting

See the [Azure Video Analyzer Troubleshooting page](https://docs.microsoft.com/azure/azure-video-analyzer/video-analyzer-docs/troubleshoot.md).

## Next steps

Experiment with different [pipeline topologies](https://docs.microsoft.com/azure/azure-video-analyzer/video-analyzer-docs/pipeline) by modifying `pipelineTopologyUrl` in operations.json.
