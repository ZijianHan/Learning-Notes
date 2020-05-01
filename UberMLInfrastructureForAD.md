title: Uber ATG's ML Infrastructure and Version Control Platform Architecture
original post link: https://eng.uber.com/machine-learning-model-life-cycle-version-control/
Chinese version: https://mp.weixin.qq.com/s/yJzW3-RLC0d05vW2EqjY0w
Uber ATG: Advanced Technologies Group, developing self-driving vehicles technology.

General introduction of contents: ML components, development life cycle, automating tool (VerCD - Ver continuous delivery)

## Self-driving vehicle ML model components
Software components (tasks) that contains one or more ML models
- Perception: Object identification (types: vehicle, pedestrian, bicycle, etc.) and 3D localization.
- Prediction: Combine object detection results (type + localization) with HD maps, to perform object trajectory prediction in future n seconds in a given scene. The Prediction component allows the self-driving vehicle to anticipate where actors will most likely be located at various points in the future.
- Motion Planning:
  - Input:
    - self-driving vehicle’s destination
    - the predicted trajectories of all actors in the scene
    - the high definition map
    - other mechanisms
  - Output: plan the path of the vehicle.
- Control: Path following for motion planned path by controlling steering, brakes and accelerator.

## ML model life cycle.
Training data source: sensor-equipped vehicles(Lidar, cameras, radar) in a wide variety of traffic situations.
Labeling work: location, shape, other attributes like object type, etc.
Model training: sufficient labeled training data + HD map
ML Model different layers: highest layer: ML applications, middle layer: common ML libraries such as TF and PyTorch, GPU acceleration.
Five-step life cycle for training and deployment of ML models:
[ATG_ML_platform_figure-lifecycle.png]

### Data ingestion
Data ingestion process: Select the logs intended to use and extract data from them.

1. Data log selection and dividing: 75% training data, 15% testing data, 10% validation data. The pipeline used to select logs and split the data into 3 groups based on geographical location: GeoSplit.

2. Data extraction from logs (Using Petastorm, Uber ATG's open source data accesss library for DL):
Data contents:
- Images from the vehicle’s cameras
- LiDAR 3D point information
- Radar information
- The state of the vehicle, including location, speed, acceleration and heading
- Map information, such as the vehicle’s route and lanes it used
- Ground truth labels
Extraction process:
- extract data from multiple logs in parallel using Apache Spark (this way keeps the data in an optimized format by storing all info needed in GPUs memory after load from HDFS, so the training is efficient)
- save data log-by-log on HDFS
[ATG_ML_platform_figure-extraction.png] shows the extraction process running on CPU cluster.
(We use extracted data (including the images pictured here, along with other sensor data) to run distributed training using Horovod on the GPU cluster and save the data to HDFS.)

### Data validation
1. Run queries to pull: 1) the number of frames in a scene 2) the number of occurrences of the different label types.
2. Compare results to previous data sets to see how conditions have changed. Further analysis needed if not as expected.

### Model training
Distributed ML training system used: Horovod!
1. Spread the training process on different GPUs with data parallelism as shown in figure below (same model trained on different GPUs with different parts of data). Each process performs forward and backword propagation independently.
[ATG_ML_platform_figure-modeltraining.png]
2. Combine the parallel-trained model(knowledge distributing as I understand): using Horovod's ring-allreduce algorithm to average gradients and disperse them to all work nodes without requiring a parameter server.
3. Training verification: through TensorBoard, leveraging ML frameworks like TensorFlow and PyTorch.

ML computing with hybrid approach: both in on-premise data centers powered by GPU and CPU clusters as well as in the cloud.
- on-premise data center: orchestrate training jobs using Peloton (https://eng.uber.com/resource-scheduler-cluster-management-peloton/), to scales jobs to GPUs and CPUs.
- cloud-based training: using Kubernetes (https://kubernetes.io/) to deploy and scale application containers across clusters.

### Model evaluation
Evaluate the performance on model itself (with model-specific metrics) and on entire system (with system metrics). Also use hardware metrics to evaluate the model running speed on hardware.
1. Model-specific metrics
For example, Perception model: precision(correct detection rate) and recall(the proportion of the ground truth objects that model identified correctly).
For not performing well metrics, we adjust data pipeline by including similar cases(https://eng.uber.com/searchable-ground-truth-atg/) (data augmentation). But prevent overfitting.
2. System metrics
Mainly safety and comfort measurement on overall vehicle motion, with large test set. Performed after model-specific metrics are well enough. Due to ML model dependencies, the system evaluation will give a comprehensive overview between components.
3. Hardware metrics
Using ATG's internal benchmarking system to profile a certain part of software, and evaluate how quick it will run on vehicle hardware.

### Model serving
Deploy the model on an inference engine in vehicle with continuous iteration, focusing on the part need to be improved learnt from model evaluation part.

## Accelerating ML research with CI and CD
Continuous integration and delivery (VerCD platform) will wrap and automate the 5-step ML model developing process to an end-to-end workflow, reduce errors and boost the speed.

The VerCD platform is such a system that tracks dependencies between code, datasets and models throughout the workflow, starts with the dataset extraction stage, cover model training, and conclude with computing metrics.

Why developed Uber's own platform:
1. DL models have deep dependencies and development complexity. Although open source tools like Kubeflow and TensorFlow Extended provide high-level orchestration to build dataset and train models, they are not well integrated, and do not fully enable CD and CI
2. Traditional versioning and CD/CD tools like Git and Jenkins do not operate over ML artifacts.

### The need for agile development in ML workflows
The standard agile development process (https://en.wikipedia.org/wiki/Agile_software_development) in application for ML workflows (what do they mean for ML):
- version controlling:
  allows the analysis of impact of a change on some part towards downstream dependencies, independently from one developer to another.
- dependency tracking
  Dependency between data and results: adjustments to labels and raw data changes the nature of the dataset, which in turn affects training results. Moreover, the way of data extraction and model training code and configuration also affects the results. So the dependency tracking should tell that correct order: data extraction first then model building.
- continuous integration and continuous delivery:
  the ML workflow involves code, data and models, of which only the first is handled by traditional software tools. Following figure illustrates some differences in workflow, and next figure shows the scope and complexity of system required to build a final ML artifact.
[ATG_ML_platform_figure-mlworkflow.png] The traditional continuous delivery cycle differs from that used for ML in that, instead of just building code and testing it, ML developers must also construct data sets, train models, and compute model metrics.
[ATG_ML_platform_figure-mlrequirementsforsystem.png] The final result of ML workflows is just a tiny artifact compared to all of the supporting systems and code (such as configuration, data collection, feature extraction, data verification, machine resource management, analysis tools, process management tools, serving infrastructure, and monitoring). (Source: Hidden Technical Debt in Machine Learning Systems. Used with permission.)

### Deep dependency graphs in the self-driving domain
The deep dependency graph is a result of the layered architecture of self-driving software stack, where each layer provides a different ML function, shown in figure below. The dependency graph for an object detection model, shown on the left, and two other ML models, shown on the right, depicts code and configurations that are handled by version control systems (in green) and items that are not handled by version control (in grey).
[ATG_ML_platform_figure-dependencygraph.png]
3 ML layers:
- an object detection model whose input is raw sensor data,
- a path prediction model whose input is the set of objects detected by the object detection model,
- a planning model whose inputs are the outputs of the path prediction model.
Each layer shows on left involves generating 3 artifacts:
1. A data set, composed of raw source data, bounding boxes around different objects in the source image data (i.e. labels), and the data set generation code.
2. A trained model, which requires as input the data set artifact, the model training code, and configuration files governing model training.
3. A metrics report, which requires as input the trained model artifact, the data set, and the metrics generation code.

Such deep dependencies brings particular challenge for CD.

## VerCD for Uber ATG
