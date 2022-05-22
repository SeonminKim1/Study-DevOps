
## Process
1. FE, BE에서 Job에 대한 정보가 Restful API 로 전달됨
2. Routing Service에서 Job_id로 Mongo DB에 저장된 현재 추론 서버에 대한 정보를 가져옴 
    - (예상) 추론 서버 번호, 가용 상태 등 

3. 추론 가능 서버로 FastAPI, Restful 을 이용해 정보 전달 
    - (예상) Job 정보 + 추론 서버 정보

4. 각 Inference 서버에서 Docker-py를 이용하여 Container들 생성 및 운영, curl command 전달하여 동작
- Deploy(Create, Load) : on 메모리
- UnDeploy (Unload) : out 메모리
- Terminate : 삭제
- Temp : 1회용 서비스

5. 추론 결과 저장 및 MongoDB 이용 데이터 Stateless 하게 저장

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

### 5. Test
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
- container run시 command 실행 
    - 됬다가 안됬다가 함. 
    - run후 exec_run으로 현재 진행 중
- volume 공유가 잘 안되는 문제?
    - 내부 속도 차이 문제 같기도 함.
    - reload() 로 현재 진행 중
      
## TODO
- Docker-compose로 자동화
- Docker-py 자동 테스트

## 참고문헌
- https://docker-py.readthedocs.io/en/stable/containers.html
- https://docker-py.readthedocs.io/en/1.10.0/api/
- https://github.com/docker/docker-py