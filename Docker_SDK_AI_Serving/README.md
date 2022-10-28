## Docker 기반 AI Serving Service 상태 관리 - POC 

### 목적 및 주요 기능
- Job(서빙 된 AI Model 사용 요청) 정보 수신 (Routing Service)을 통한 추론 요청 처리 (Inference Service)
- Docker-py를 통한 Code Level 상태 관리
- Routing Service Container 내에서 추가 Container 생성 (Docker in Docker 활용)

## Process
1. FE, BE에서 Job 정보 및 추론 요청 API 들어옴
2. Routing Service : Job_id로 Mongo DB에 저장된 현재 추론 서버에 대한 정보를 가져옴 
- API 요청시 Container 내부에서 Container 상태 관리 (Docker in Docker)
- (고려사항) 추론 서버 번호 numbering, 가용 상태 체크 등 

3. Routing Servic에서 각 Inference 서버 생성 및 운영
- Deploy(Create, Load) : on 메모리
- UnDeploy (Unload) : out 메모리
- Terminate : 삭제
- Temp : 1회용 서비스


## Directory Structure

```
root
├─routing_service
│  ├── app/Routing_Service.py
│  └── Dockerfile
├─inference_service
│  ├── app/Inference_Service.py
│  └── Dockerfile
```

## Usage

### 1. Add alias in .bashrc

```
#### docker alias
alias ps_rm_all='docker rm -f `docker ps -a -q`'
alias psa='docker ps -a'
alias ps_watch='watch -n 0.05 docker ps -a'

### build (args image-name)
build_img(){ docker build -t $1 ./;}
alias b_img=build_img
----
source .bashrc
```

### 2. Build 'rou_service, inf_service' image

```
$ cd routing_service/
$ b_img rou_service

$ cd inference_service/
$ b_img inf_service

≒ docker build -t rou_service ./
≒ docker build -t inf_service ./
```
    
### 3. Create Network

```
$ docker network create -d bridge tmp_network
```

### 4. Run 'rou_service'

```
$ docker run -it -p 81:8001 -v /var/run/docker.sock:/var/run/docker.sock --network=tmp_network rou_service
```

### 5. Test Run
```
# 1-1. Create
curl -X 'POST' \
  'http://0.0.0.0:81/inference_router/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "job_id": "a1",
  "model": "m-131",
  "dataset": "ds-550",
  "operation_type": "DEPLOY_CREATE",
  "container_id": "aa"
}'

## Create에서 생성된 컨테이너를 찾아서 container_id 변경해주어야함.
## 원래는 mongo db에서 자동으로 찾아줘야 함
# 1-2. Load
curl -X 'POST' \
  'http://0.0.0.0:81/inference_router/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "job_id": "a1",
  "model": "m-131",
  "dataset": "ds-550",
  "operation_type": "DEPLOY_LOAD",
  "container_id": "1cfed7648adeede57eab851409fc8eae139888c7594b0c80831d4d3041261a15"
}'

# 1-3. UnLoad
curl -X 'POST' \
  'http://0.0.0.0:81/inference_router/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "job_id": "a1",
  "model": "m-131",
  "dataset": "ds-550",
  "operation_type": "DEPLOY_UNLOAD",
  "container_id": "1cfed7648adeede57eab851409fc8eae139888c7594b0c80831d4d3041261a15"
}'


# 1-4. Terminate
curl -X 'POST' \
  'http://0.0.0.0:81/inference_router/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "job_id": "a1",
  "model": "m-131",
  "dataset": "ds-550",
  "operation_type": "TERMINATE",
  "container_id": "1cfed7648adeede57eab851409fc8eae139888c7594b0c80831d4d3041261a15"
}'

# 1-5. TEMP
curl -X 'POST' \
  'http://0.0.0.0:81/inference_router/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "job_id": "a1",
  "model": "m-131",
  "dataset": "ds-550",
  "operation_type": "TEMP",
  "container_id": "ASDF"
}'
```

## Issue
- volume 공유가 잘 안되는 문제?
- Docker in Docker 활용시의 내부 속도 차이 문제 같기도 함.
- reload() 로 기능 작동은 가능하나 안정성이 현재 떨어짐 => K8S로 이동
      
## TODO
- Docker-compose 파일 작성
- Docker-py 모듈 Debugging, 병목 지점 디버깅

## 참고문헌
- https://docker-py.readthedocs.io/en/stable/containers.html
- https://docker-py.readthedocs.io/en/1.10.0/api/
- https://github.com/docker/docker-py
