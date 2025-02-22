# AdapTrain

<p align="center">
  <img src="./docs/adaptrain-logo.webp" alt="AdapTrain logo" width="40%" height="40%">
</p>
<p align="center" style="font-size: 11px;">
  [This logo is generated using DALL.E 3 by OpenAI]
</p>

AdapTrain is a framework designed to optimize distributed training in heterogeneous environments. AdapTrain handles workload variations and cloud multi-tenancy effectively, achieving up to 8.2× faster convergence compared to existing methods.

The key features of AdapTrain are:
- **Dynamic Model Partitioning:** Automatically adjusts model partitioning based on each worker's computational capacity to optimize resource utilization.
- **Reduced Synchronization Overhead:** Minimizes delays by ensuring synchronized completion of training rounds across all workers.
- **Robust to Variations:** Performs reliably under workload variations, resource heterogeneity, and cloud multi-tenancy.
- **Accelerated Model Convergence:** Demonstrates up to 8.2× faster convergence compared to state-of-the-art distributed training methods.

<p align="center">
  <img src="./docs/adapTrain.svg" alt="AdapTrain logo" width="40%" height="40%">
</p>

## Setup

### Prerequisites
- A Kubernetes cluster up and running (can be local or cloud-based).
- `kubectl` configured to interact with your cluster.
- A machine with Docker installed for building the images.

### Directory Structure

To set up AdapTrain, ensure the following directory structure is provided:

```bash
.
├── dataset
│   ├── test_x.npy
│   ├── test_y.npy
│   ├── train_x.npy
│   └── train_y.npy
└── configs
    ├── m_config.json
    ├── p_config.json
    └── d_config.json
```

## Requirements

### Dataset
- The dataset must be compatible with `torch.utils.data.Dataset`.
- Ensure the `.npy` files are properly formatted and preprocessed as per the requirements of the model.

### Configuration Files
- Each configuration file must follow the specified JSON format in [Configuration Files](#). An example for each configuration file is provided below.

#### Model Configuration:
  ```json
  {
    "num_epochs": 100,
    "batch_size": 128,
    "learning_rate": 0.01,
    "input_channels": 1,
    "layers": [
        {
            "type": "linear",
            "in_features": 4096,
            "out_features": 4096
        },
        // ... other layers ...
        {
            "type": "activation",
            "activation": "log_softmax",
            "dim": 1
        }
    ]
  }
  ```

#### Partitioning Configuration
  ```json
  {
    "repartition_iter": 100,
    "log_interval": 25
  }
  ```
  
#### Deployment Configuration
  ```json
  {
    "num_workers": 4,
    "dist_backend": "gloo",
    "dist_url": "tcp://127.0.0.1:9000",
    "node_names": ["worker-1", "worker-2", "worker-3", "worker-4"],
    "namespace": "adaptrain"
  } 
  ```
 

## Deployment
AdapTrain is designed to be deployed on a Kubernetes cluster. The deployment process involves building both the worker and controller Docker images. Follow these steps to deploy it correctly.

### Build Docker Images

#### 1. Build the Worker Docker Image
First, build the worker Docker image. This image contains the necessary dependencies and code for the worker nodes in the distributed training setup. Run the following command in the root of the repository:
```bash
docker build -t adaptrain-worker -f ./docker/worker.Dockerfile .
```

#### 2. Push the Worker Docker Image
Once the worker image is built, push it to your desired Docker repository (e.g., Docker Hub):
```bash
docker push <your-repo>/adaptrain-worker:latest
```

#### 3. Update the Controller Deployment Configuration
Before building the controller image, you need to specify the worker image in the controller's deployment configuration file (`configs/d_config.json`). This ensures that the controller can reference the correct worker image.

Modify the `workers_image` field in `d_config.json` to the name of the worker image you pushed in step 2:

  ```json
  {
    "num_workers": 4,
    "dist_backend": "gloo",
    "dist_url": "tcp://127.0.0.1:9000",
    "node_names": ["worker-1", "worker-2", "worker-3", "worker-4"],
    "namespace": "adaptrain",
    "workers_image": "genericdockerhub/adaptrain-worker:latest" // updated
  } 
  ```

#### 4. Build the Controller Docker Image
Now that the controller configuration is set, you can build the controller Docker image. Run the following command:

```bash
docker build -t adaptrain-controller -f ./docker/controller.Dockerfile .
```

#### 5. Push the Controller Docker Image
Push the controller image to your repository (just like you did for the worker image):

```bash
docker push <your-repo>/adaptrain-controller:latest
```

### Deploy AdapTrain on Kubernetes
Once both images are built and pushed, follow these steps to deploy AdapTrain on your Kubernetes cluster.

#### 1. Create the Namespace
Create the namespace provided in the `d_config.json` file. The namespace should be defined under the namespace field in the deployment configuration file.

```bash
kubectl apply -f ./manifests/namespace.yaml
```

#### 2. Create the Service Account
Create a service account with the necessary permissions for the controller to be able to deploy the worker pods. You can define this service account using a Kubernetes YAML file or apply it directly using kubectl.

```bash
kubectl apply -f ./manifests/service-account.yaml
```

#### 3. Create the Role and RoleBinding
Next, create a **Role** to allow the controller to manage pods within the namespace and a **RoleBinding** to bind the service account to the role by applying the Role and RoleBinding YAMLs:

```bash
kubectl apply -f ./manifests/role.yaml
kubectl apply -f ./manifests/rolebinding.yaml
```

#### 4. Deploy the Controller
Deploy the controller on your Kubernetes cluster:

```bash
kubectl apply -f ./manifests/controller.yaml
```
Once the controller is deployed, it will automatically deploy the worker pods based on the configurations provided in `d_config.json`.

#### 5. Start Training
After deploying the controller, it will start the distributed training by automatically deploying the workers and managing the synchronization.
<!-- ## How to use? -->
<!-- Setting up controller using local machine.
Setting up workers using controller.
Saving the final trained model. -->