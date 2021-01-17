# TCO Multicloud

## Descrição
Aplicação feita para o PIBIT pelos integrante Geovany, Gilberto e Jonas com a orientação do Raphael.
O projeto consiste em uma ferramenta para Descoberta e Estimativa de Custo de
Infraestrutura usando Computação em Nuvem.

## Deploy em Produção
Estamos utilizando o Docker com o auxilio do gunicorn para rodar o projeto em produção.

Antes de realizar o deploy em produção altere o DEBUG no settings.py para False

Para realizar o deploy da imagem do Docker execute:
```
docker build -t tco_multicloud .
```
Para executar a imagem
```
docker run -d -p 80:80 -i -t tco_multicloud
```