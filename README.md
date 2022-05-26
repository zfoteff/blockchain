Block Chain Demo
==========
![Python3](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)

# About the Project
This project is intended to create a simplified blockchain that can be manipulated and deployed in a docker image. An
additional goal of this project is to make the project collaborative using GitHub's project and collaboration features.

Used Adetu Ridwan's [blockchain tutorial](https://www.section.io/engineering-education/how-to-create-a-blockchain-in-python/) as inspiration

# Contributors:
* Zac Foteff: zfoteff@protonmail.com

# Build:
Install pip packages
```bash
pip install -r requirements.txt
```

# Docker
## Build Docker Image
Build Docker Image
```bash
docker build -t blockchain-image .
```

Run Docker Image
```bash
docker run -d --name blockchain-container -p 8000:8000 blockchain-image
```

# Run: 
```bash
python server.py
```
or
```
uvicorn server:app
```

## Format Files
In root directory
```commandline
python -m black
```