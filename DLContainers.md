
##References
[PyTorch docker image](https://hub.docker.com/r/pytorch/pytorch)

**docker: Pull an image from Docker Hub**
singularity pull tensorflow.sif docker://tensorflow/tensorflow:latest
singularity run docker://tensorflow/tensorflow:latest

[with Nvidia](https://developer.nvidia.com/blog/how-to-run-ngc-deep-learning-containers-with-singularity/)
singularity pull tensorflow-19.11-tf1-py3.sif docker://nvcr.io/nvidia/tensorflow:19.11-tf1-py3
[GPU support](https://sylabs.io/guides/3.5/user-guide/gpu.html)
singularity pull docker://tensorflow/tensorflow:latest-gpu
singularity run --nv tensorflow_latest-gpu.sif
verify: print(device_lib.list_local_devices())


---
**other links**
singularity:
https://sylabs.io/guides/3.2/user-guide/cli/singularity_pull.html
https://sylabs.io/guides/3.2/user-guide/cli/singularity_remote_status.html


transition:
https://www.nas.nasa.gov/hecc/support/kb/converting-docker-images-to-singularity-for-use-on-pleiades_643.html
https://singularity.lbl.gov/archive/docs/v2-3/docs-docker

docker:
https://docs.docker.com/engine/reference/commandline/run/
https://docs.docker.com/language/python/build-images/
https://www.docker.com/blog/containerized-python-development-part-1/
https://stackoverflow.com/questions/56920535/why-does-the-pytorch-docker-image-not-come-with-torch
https://code.visualstudio.com/docs/containers/quickstart-python
https://www.tensorflow.org/install/docker
AWS SageMaker:
https://docs.aws.amazon.com/sagemaker/latest/dg/pre-built-containers-frameworks-deep-learning.html

tensorflow:
https://github.com/drorlab/tf-singularity
https://www.tensorflow.org/install/source#gpu
https://developer.nvidia.com/blog/how-to-run-ngc-deep-learning-containers-with-singularity/
https://ngc.nvidia.com/catalog/containers/nvidia:tensorflow

pytorch:
https://github.com/ylugithub/pytorch_gpu_singularity