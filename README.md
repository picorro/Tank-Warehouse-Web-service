# WebServisai
 
URL = localhost:5000/api<br />

**Usage**<br />

**GET All**
localhost:5000/api/vehicles
Response: returns all vehicles in an array if successful

**GET by vehicleId**
localhost:5000/api/vehicles/<int: vehicleId>
Response: returns object if successful

**POST**
localhost:5000/api/vehicles + JSON body
example body:
```
{
    "model": "T34",
    "year": 1945,
    "origin": USSR
}
```
New vehicle will be created with automatically incremented id if successful
An error message will be returned on failure
Status on success: ```201```
Status on failure: ```400```

**PUT by vehicleId**
localhost:5000/api/vehicles/<int: vehicleId> + JSON body
example body (requires at least one parameter of a vehicle object):
```
{
    "model": "KV-1"
}
```
Edited object will be returned upon success
Otherwise an error message will be returned
Status on success: ```200```
Status on failure: ```404```

**DELETE by vehicleId**
localhost:5000/api/vehicles/<int: vehicleId> + JSON body
Object with the corresponding id will be deleted upon success
An error message will be returned on failure
Status on success: ```200```
Status on failure: ```404```
