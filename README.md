# Docker_ELK
Docker &amp; ELK Stack &amp; Docker Compose &amp; Kubernetis

## Docker 란
- 도커는 ‘컨테이너 기반의 오픈소스 가상화 플랫폼’
- 컨테이너란 : 애플리케이션과 애플리케이션을 구동화는 환경을 격리한 공간

## ELK 란
- ElasticSearch : ElaticSearch 는 Lucene 기반으로 개발한 분산 검색엔진으로, LogStash 를 통해 수신된 데이터를 저장소에 저장하는 역할을 담당

- LogStash : 수집할 로그를 선정해서,  지정된 대상 서버(Elasticsearch)에 인덱싱해서 전송하는 역할을 담당하는 소프트웨어 (다양한 플러그인 제공을 여러 유형의 로그 수집 및 인덱싱이 가능함)

- Kibana : 사용자에게 무언가를 보여주기 위한 목적, <b>Visualization</b> 을 담당하는 HTML + Javascript 엔진이라고 보면 됨

