# K8S Cluster Setup

Setup Kubernetes Kubeadm Cluster On Remote Server

## Python3.10 and pip require

> https://www.python.org/downloads/

### Install dependency using Pipfile

```shell
python --version
python -m pip --version

python -m pip install -r ./requirements.txt

# OR

python -m pip install pipenv
pipenv shell

# Install Pipfile dependency
pipenv install
# pipenv install --ignore-pipfile     # Install dependency from Pipfile.lock
```

### Start Cluster Setup

```shell
python main.py
```
