# demty2025-dynamo-cine-gen-lambda

Lambda function to generate items for a DynamoDB table about movie schedules in a cinema.

## Requirements

The following elements are required before being able to execute this lambda function in your AWS environment:

#### DynamoDB table

The following table should already exists:

```python
nombre_tabla = "Peliculas_S3D2_xideral"

table = dynamodb.create_table(
    TableName=nombre_tabla,
    KeySchema=[
        {'AttributeName': 'pelicula_id', 'KeyType': 'HASH'}, # Clave de partición
        {'AttributeName': 'fecha_hora', 'KeyType': 'RANGE'} # Clave de ordenamiento
    ],
    AttributeDefinitions=[
        {'AttributeName': 'pelicula_id', 'AttributeType': 'S'},
        {'AttributeName': 'fecha_hora', 'AttributeType': 'S'}
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)
```

As you might have been able to see, the structure is pretty basic, with only `pelicula_id` and `fecha_hora` acting as a composed partition key; the reason being 
to be able to get `peliculas_id` between dates from `fecha_hora`.

#### Lambda Function

Copy and paste the contents of `lambda_function.py` in a newly created lambda function with a runtime of Python 3.11, though newly versions are expected to work as well.


##### General Configuration

You are free to tweak the configuration values to fit your requirements, though the only recommendations is to have a `Timeout` greater than 3 secs.

##### Permissions

The lambda's assigned role must have assigned the `dynamodb:BatchWriteItem` inline policy to be able to insert new records.

##### Environemt Variables

Only 2 env variables are required and must be configured inside the lambda function:

- **REGION**: Specify your DynamoDB region. Example `us-east-1`.

- **TARGET_TABLE_NAME**: Specify your DynamoDB table name. Example `Peliculas_S3D2_xideral`.

##### Tests (Events)

The lambda is designed to work only when triggered by events, hence the expected value for the paramater `value` is a list of dictionaries with at least the following format:

```json
{
    "pelicula_id": "1",
    "fecha_hora": "2025-01-02 10:30:00"
}
```

- **pelicula_id**: Partition key for the DynamoDB table
- **fecha_hora**: Should follow the ISO 8601.


Again, except for the 2 above keys, the dictionaries can have any amount of fields, though the following format is recommended:

```json
{
    "pelicula_id": "6",
    "fecha_hora": "2025-01-02 10:30:00",
    "nombre": "Vecinos Invasores",
    "sala": 1,
    "duracion": "90",
    "clasificacion": "AA"
}
```

Finally, here's a working example:

```json
[
  {
    "pelicula_id": "6",
    "fecha_hora": "2025-01-02 10:30:00",
    "nombre": "Vecinos Invasores",
    "sala": 1,
    "duracion": "90",
    "clasificacion": "AA"
  },
  {
    "pelicula_id": "7",
    "fecha_hora": "2025-01-02 19:00:00",
    "nombre": "Eternal Sunshine Of The Spotless Mind",
    "sala": 20,
    "duracion": "122",
    "clasificacion": "C"
  },
  {
    "pelicula_id": "8",
    "fecha_hora": "2025-02-05 15:45:00",
    "nombre": "Training Day",
    "sala": 13,
    "duracion": "120",
    "clasificacion": "D"
  },
  {
    "pelicula_id": "9",
    "fecha_hora": "2025-01-25 17:15:00",
    "nombre": "Blood Diamond",
    "sala": 15,
    "duracion": "120",
    "clasificacion": "D"
  },
  {
    "pelicula_id": "10",
    "fecha_hora": "2025-01-15 20:00:00",
    "nombre": "Deadpool 3",
    "sala": 5,
    "duracion": "95",
    "clasificacion": "C"
  }
]
```


### Usage

After all the requirements are met, simply `Deploy` and run the configured `Tests`.

- **Sucessful response**
```json
{
  "statusCode": 200,
  "body": {
    "message": "Items inserted successfully",
    "items": [
      {
        "pelicula_id": "6",
        "fecha_hora": "2025-01-02 10:30:00",
        "nombre": "Vecinos Invasores",
        "sala": 1,
        "duracion": "90",
        "clasificacion": "AA"
      }
    ]
  }
}
```

- **Failed response**
```json
{
  "statusCode": 500,
  "body": {
        "message": "Error inserting items",
        "error": "An annoying error"
    }
}
```
