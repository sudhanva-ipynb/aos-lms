# LMS SERVER

The server for the grpc enabled system. 

## Functions :
    1. Store Resources (Materials /Assignments)
    2. Provide Authentication/Authorization
    3. Manage (create/fetch) resorces

## Steps to run :
### Step 1: Create a virtual environment
```shell
python -m venv venv
```

### Step 2: Install all requirements
```shell
pip install -r requirements.txt
```
    
### Step 3: Generate grpc python code
```shell

python -m grpc_tools.protoc -I.  --python_out=. --pyi_out=. --grpc_python_out=. ./protos/Lms.proto
```
    
### Step 4: Run the source file
```shell
python main.py
```
    
