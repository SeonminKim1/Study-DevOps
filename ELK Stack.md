## 1. ELK Stack

### 1.1 ElasticSearch
- ElaticSearch 는 Lucene 기반으로 개발한 검색 및 분산 검색엔진으로, LogStash 를 통해 수신된 데이터를 저장소에 저장하는 역할을 담당

![elasticsearch](_img/elasticsearch.png)

### 1.2 LogStash
- 수집할 로그를 선정해서, 지정된 대상 서버(Elasticsearch)에 인덱싱해서 전송하는 역할을 담당하는 소프트웨어 (다양한 플러그인 제공을 여러 유형의 로그 수집 및 인덱싱이 가능함)

![logstash](_img/logstash.png)

### 1.3 Kibana
- 사용자에게 무언가를 보여주기 위한 목적, <b>Visualization</b> 을 담당하는 HTML + Javascript 엔진이라고 보면 됨
- Kibana를 사용하면 Elasticsearch에서 차트와 그래프로 데이터를 시각화 할 수 있습니다

![kibana](_img/kibana.png)


<hr>


## 2. Beat
![beats](_img/beats.png)

- 단일 목적의 데이터 수집기 플랫폼인 Beats는 수백 수천 개의 장비와 시스템으로부터 Logstash나 Elasticsearch에 데이터를 전송

![beats_to_kibana](_img/beats_to_kibana.png)

- 1. 1개 이상의 Client( 수집할 Data 발생 서버 )에서 beats가 특정 트리거에 의해 logstash로 Data를 전송 (각 Client마다 Beats 존재)
- 2. logstash로 전달 된 Data를 커스터마이징이 가능한 필터를 통해 가공하여 Elasticsearch로 전달
- 3, Elasticsearch로 전달 받은 데이터를 서버(Elasticsearch)에 저장
- 4. kibana에서 연동되있는 Elasticsearch에 저장된 데이터 셋을 토대로 시각화를 제공