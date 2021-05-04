# Tank Warehouse
 **Building in docker**<br />
Clone the project<br />
Navigate to the directory on command line<br />
```docker-compose build```<br />
```docker-compose up -d```<br />

URL = localhost:5000/api<br />

**Usage**<br />

**GET All**<br />
localhost:5000/api/vehicles<br />
Response: returns all vehicles in an array if successful<br />

**GET All Including Phone Data**<br />
localhost:5000/api/vehicles<br />
Response: returns all vehicles in an array that contains full information about the phone if successful<br />

**GET All Phones**<br />
localhost:5000/api/phones<br />
Response: returns all phones in an array if successful<br />

**GET by vehicleId**<br />
localhost:5000/api/vehicles/<int: vehicleId><br />
Response: returns vehicle if successful<br />
Return on failure: ```404```<br />

**GET Phone by vehicleId**<br />
localhost:5000/api/vehicles/<int: vehicleId>/phone<br />
Response: returns phone if successful<br />
Return on failure: ```404```<br />

**GET Vehicle with Phone by vehicleId**<br />
localhost:5000/api/all/<int: vehicleId>/phone<br />
Response: returns vehicle with full phone information if successful<br />
Return on failure: ```404```<br />

**POST**<br />
localhost:5000/api/vehicles + JSON body<br />
example body:<br />
```
{
    "model": "T34",
    "year": 1945,
    "origin": USSR
}
```
**POST with a Phone**<br />
localhost:5000/api/all + JSON body<br />
example body:<br />
```
{
    "model": "KV-1",
    "origin": "USSR",
    "phone": {
        "brand": "dddd",
        "model": "X",
        "price": "1300 yen"
    },
    "year": "1939"
}
```
A new phone will be created
If sucessful a New vehicle will be created with automatically incremented id and will contain a newly created phone<br />
An error message will be returned on failure<br />
Status on success: ```201```<br />
Status on failure: ```400```<br />

**PATCH by vehicleId**<br />
localhost:5000/api/vehicles/<int: vehicleId> + JSON body<br />
example body (requires at least one parameter of a vehicle object):<br />
```
{
    "model": "KV-1"
}
```
Edited object will be returned upon success<br />
Otherwise an error message will be returned<br />
Status on success: ```200```<br />
Status on failure: ```404```<br />

**PATCH with Phone by vehicleId**<br />
localhost:5000/api/all/<int: vehicleId> + JSON body<br />
example body (requires at least one parameter of a vehicle object):<br />
```
{
    "model": "KV-1"
}
```
If phone is contained in json, an attempt to patch the phone with data in json will be made
Edited object will be returned upon success<br />
Otherwise an error message will be returned<br />
Status on success: ```200```<br />
Status on failure: ```404```<br />

**PUT by vehicleId**<br />
localhost:5000/api/vehicles/<int: vehicleId> + JSON body<br />
example body (requires all parameters of a vehicle object):<br />
```
{
    "model": "KV-1"
    "year": 1943,
    "origin": "USSR"
}
```
Replaced object will be returned upon success<br />
Otherwise an error message will be returned<br />
Status on success: ```200```<br />
Status on failure: ```404```<br />

**PUT with Phone by vehicleId**<br />
localhost:5000/api/all/<int: vehicleId> + JSON body<br />
example body (requires all parameters of a vehicle object):<br />
```
{
    "model": "KV-1"
    "year": 1943,
    "origin": "USSR"
}
```
If phone is contained in json, an attempt to put the phone with data in json will be made
Replaced object will be returned upon success<br />
Otherwise an error message will be returned<br />
Status on success: ```200```<br />
Status on failure: ```404```<br />

**DELETE by vehicleId**<br />
localhost:5000/api/vehicles/<int: vehicleId><br />
Object with the corresponding id will be deleted upon success<br />
An error message will be returned on failure<br />
Status on success: ```200```<br />
Status on failure: ```404```<br />
