# Tesouro Direto

## Dependências
Foi utilizado Python 3.5 para o desenvolvimento deste projeto.

A instalação dos pacotes adicionais pode ser feita executando a linha de comando abaixo:

```
pip3 install -r requirements.txt
```

## Configuração

Após a instalação das dependências, execute os comandos abaixo no diretório raiz para a criação do banco de dados e importação da planilha de séries temporais:


```
python manage.py makemigrations tesouro_direto
python manage.py migrate
python manage.py importdata /path/para/planilha.xlsx
```

## Inicializa o servidor built-in:
```
python manage.py runserver
```


## Exemplo de Requisições

### Lista de vendas/resgates de títulos

```
GET /titulo_tesouro/
```

### Adicionar um valor monetário a um título

```
POST /titulo_tesouro/
```

Exemplo de request:

```
{
    "categoria_titulo": "LTN",
    "mes": 3,
    "ano": 2017,
    "acao": "venda",
    "valor": "1259.15"
}
```

### Remover um valor monetário de um título

```
DELETE /titulo_tesouro/{id}/
```

### Atualizar um valor monetário para um título específico

```
PUT /titulo_tesouro/{id}/
```


Exemplo de request:

```
{
    "categoria_titulo": "LTN",
    "mes": 3,
    "ano": 2017,
    "acao": "venda",
    "valor": "1259.15"
}
```

### Mostrar o histórico de um título específico

```
GET /titulo_tesouro/{id}/
```

### Comparar o histórico de dois ou mais títulos

Exemplo:

```
GET /titulo_tesouro/comparar/?ids=1,2,3
```

### Buscar valores de venda de um título em determinado período


```
GET /titulo_tesouro/venda/{id}/
```

### Buscar valores de resgate de um título em determinado período


```
GET /titulo_tesouro/resgate/{id}/
```
