from fastapi import FastAPI, Request
from pydantic import BaseModel
from starlette.responses import JSONResponse
import docker
import time

app = FastAPI()

## Routing_Service.py 역할
# 1. POST로 받은 데이터 파싱
# 2. Redis나 Mongo DB로부터 Container_id 가져오기 (현재는 정적 정의)
# 3. Docker Container 기반 Inference Service 시작
# 4. 요청이 Load일시 -> (1) Create 체크 후 (2) Load
# 5. 요청이 Temp일시 -> (1) Create (2) Load (3) 자동 remove
# 6. 요청에 따른 신규 컨테이너 생성 및 운영

#command = 'curl -X GET http://0.0.0.0:82/inference_result'
command = 'curl -X GET http://0.0.0.0:82/inference_result -H accept:application/json'
# command = 'curl -X GET http://0.0.0.0:8002/inference_result -H accept:application/json'

# curl -X 'POST' \
#         'http://0.0.0.0:81/inference_router/' \
#         -H 'accept: application/json' \
#            -H 'Content-Type: application/json' \
#               -d '{
# "job_id": "a1",
# "model": "m-131",
# "dataset": "ds-550",
# "operation_type": "DEPLOY",
# "container_id": "c3d"
# }'
# infererence container list, status
_routing_keys = [
    dict({
        'inference_service' : '1',
        'server_is_running' : True,
        'service_url': 'inference_service1'
    }),
    dict({
        'inference_service' : '2',
        'server_is_running' : False,
        'service_url': 'inference_service2'
    }),
    dict({
        'inference_service' : '3',
        'server_is_running' : True,
        'service_url': 'inference_service3'
    })]
# change job_Id key -> container_key
_job_container_keys = dict({
  'a1': 'c34',
})

class inference_info(BaseModel):
    job_id:str
    model:str
    dataset:str
    operation_type:str
    container_id:str
    #  Container_id는 원래 Redis로 부터 Detect 해와야 함.
    # 시연 편의성 때문에 1.FE_BE 로부터 받음

# 2. Redis나 Mongo DB로부터 Container_id 가져오기 (현재는 정적 정의)
@app.post("/inference_router/")
def rounting_inference(inf_info : inference_info):
    # job_data = {
    #     "job_id": "a1",
    #     "model": "m-131",
    #     "dataset": "ds-550",
    #     "operation_type" :'LOAD'
    #     "container_id" :c3d~
    # }
    print('==== Inference_router data received')

    dicted_item = dict(inf_info)
    print('==== Redis(or MongoDB) Empty Server detect completed')
    dicted_item.update()
    print('==== Redis(or MongoDB) added Container_id by job_id')
    print(dicted_item)

    is_assign = False
    for i, keys in enumerate(_routing_keys):
        # 빈 inference 서버 있으면 전송
        if keys['server_is_running']== False:
            keys.update(dicted_item) # dictionary merge
            print('==== Empty Server Detected and dictionary merged', keys)
            docker_inference_service(keys)
            is_assign=True
            #print('==== Empty server is existed, send successed ')

    # 빈 서버 없는 경우 - 전송 실패
    if is_assign == False:
        dicted_item['posted'] = False
        print('==== Not empty server, send failed')
        #return JSONResponse(dicted_item)


# 3. Docker Container 기반 Inference Service 시작
def docker_inference_service(inference_data):
    # inference_data = {
    #     "job_id": "a1",
    #     "model": "m-131",
    #     "dataset": "ds-550",
    #     "operation_type":'LOAD'
    #     "container_id" :c3d~
    #     "inference_service" : '3',
    #     "server_is_running" : True,
    #     "service_url": 'inference_service3'
    # }
    print('==== Inference Service data received')
    print(inference_data)

    print('==== docker launched~ go ')
    dok = docker.from_env()
    docker_launched(dok, inference_data)

# 4. 요청이 DEPLOY 일시 -> (1) Create 체크 후 (2) Load
# 5. 요청이 TEMP 일시 -> (1) Create (2) Load (3) 자동 remove
# 6. 요청에 따른 신규 컨테이너 생성 및 운영
# 7. Deploy(Create, Load), Undeploy(Unload, Stop), Terminate, Temp 기능(remove)

def docker_launched(dok, inference_data):
    # 운영되는 Docker 에 대한 environment
    ct_id = inference_data['container_id']
    container_id_list = dok.containers.list()
    print('==== 현재 실행되고 있는 도커 Container list 갯수는 :', len(container_id_list))
    print('==== 찾고 있는 도커 Container ID', ct_id)
    print('==== 현재 실행되고 있는 도커 Container ID', container_id_list)

    # 4. 요청이 DEPLOY
    # (1) create (Load인데 실행중인 컨테이너가(id기반) 없을 때)
    if inference_data['operation_type']=='DEPLOY_CREATE':
        print('==== Container Create-Flow')
        start = time.time()
        client = dok.containers.run(image='inf_service',  # inference image
                                    # name='inference' + str(len(container_id_list)+1),  # container name
                                    ports = {'8002/tcp': 82}, # -port ('82/tcp':8002(integer여야 됨))
                                    volumes={'/home/ubuntu/volumes/': {'bind':'/var/tmp/', 'mode': 'rw'}}, # host - containers
                                    network='tmp_network',
                                    detach=True, # -d
                                    )
        client.reload() # reload 해야 동작함
        print('==== Container Reload 완료')
        client.exec_run(command)
        print('==== Container Created. Id : ', client.attrs['Id'])
        print('==== Container Created 소요시간:', round(time.time() - start, 2), '초')

    # (2) Load (Load인데 실행중인 컨테이너가(id기반) 있을 때)
    elif inference_data['operation_type']=='DEPLOY_LOAD':
        print('==== Container Load-Flow')
        start = time.time()
        client = dok.containers.get(ct_id) # get container object
        client.start()
        client.exec_run(command)
        print('==== Container Load. Id : ', client.attrs['Id'])
        print('==== Container Load 소요시간:', round(time.time() - start, 2), '초')

    # 6. 요청이 UNLOAD - stop()
    elif inference_data['operation_type']=='DEPLOY_UNLOAD':
        print('==== Container UNLOAD-Flow')
        start = time.time()
        client = dok.containers.get(ct_id)
        client.stop()
        print('==== Container UNLOAD - Stop. Id : ', client.attrs['Id'])
        print('==== Container UNLOAD 소요시간:', round(time.time() - start, 2), '초')

    # 5. 요청이 Temp (무조건 Create 후 삭제)
    elif inference_data['operation_type']=='TEMP':
        print('==== Container Temp-Flow')
        start = time.time()
        client = dok.containers.run(image='inf_service',  # inference image
                                    # name='inference' + str(len(container_id_list)+100-2),  # container name
                                    command = command,
                                    ports = {'8002/tcp':82},
                                    volumes={'/home/ubuntu/volumes/': {'bind':'/var/tmp/', 'mode': 'rw'}}, # host - containers
                                    network='tmp_network',
                                    detach = True,
                                    remove = True,
                                    #auto_remove=True, # auto remove
                                    )
        #client.reload() # reload 해야 동작함
        #print('==== Container Reload 완료')
        #client.exec_run(command)
        print('==== Container Temped. Id : ', client.attrs['Id'])
        print('==== Container Temped 소요시간:', round(time.time() - start, 2), '초')

    # 삭제 - 메모리 해제
    elif inference_data['operation_type']=='TERMINATE':
        print('==== Container UNLOAD-Flow')
        start = time.time()
        client = dok.containers.get(ct_id)
        client.remove(force=True)
        print('==== Container Terminate - Remove. Id : ', client.attrs['Id'])
        print('==== Container Terminate 소요시간:', round(time.time() - start, 2), '초')
    after_container_id_list = dok.containers.list()
    print('==== 현재 실행되고 있는 도커 Container list 갯수는 :', len(after_container_id_list))
    print('==== 현재 실행되고 있는 도커 Container ID', after_container_id_list)