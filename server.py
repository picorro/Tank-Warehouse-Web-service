from flask import Flask, request, jsonify, abort, Response
import json
import requests

server = Flask(__name__)
port = 5000
childURL = "http://arnweb:5000/"

vehicles = [
    {
    "id" : 1,
     "model": "AMX 40",
     "year": "1983",
     "origin": "France",
     "phone": "1"
    },
    {"id" : 2,
    "model": "KV-1",
    "year": "1939",
    "origin": "USSR",
     "phone": "2"
    },
    {
    "id" : 3,
    "model": "Jagdpanzer 38",
    "year": "1944",
    "origin": "Nazi Germany",
     "phone": "3"
    }
]

currentId = 4

@server.route("/")
def home():
    return ("<h1>PC vehicles list</h1><a href='http://localhost:%d/api/vehicles'>All vehicles</a>" % port)


@server.route("/api/vehicles", methods = ["GET"])
def GetAllVehicles():
    return jsonify(vehicles)

@server.route("/api/vehicles", methods = ["POST"])
def PostAVehicle():
    data = request.get_json(force=True)
    if "model" in data and "year" in data and "origin" in data and "phone" in data:
        global currentId
        vehicle ={
            "id": currentId,
            "model": data["model"],
            "year": data["year"],
            "origin": data["origin"],
            "phone": data["phone"]
        }
        vehicles.append(vehicle)
        currentId += 1
        return Response(response=(json.dumps({"Success":"Vehicle added", "id" : str(currentId-1)})), status=201, headers={"location": "/api/vehicles/"+str(currentId-1) }, mimetype="application/json")
    else:
        error = "Missing "
        if "model" not in data:
            error += "model "
        if "year" not in data:
            error += "year "
        if "origin" not in data:
            error += "origin "
        if "phone" not in data:
            error += "phone "
        error +=  ".Please spefify in Body."
        return Response(json.dumps({"Failure" : error}),status=400,mimetype="application/json")


@server.route("/api/vehicles/<int:vehicleId>", methods = ["GET"])
def GetOneVehicle(vehicleId):
    for vehicle in vehicles:
        if vehicle["id"] == vehicleId:
            return jsonify(vehicles[vehicleId - 1])
    error = "There is no vehicle with such id! "
    return Response(json.dumps({"Failure" : error}),status=404, mimetype="application/json")

@server.route("/api/vehicles/<int:vehicleId>", methods = ["PATCH"])
def PatchAVehicle(vehicleId):
    data = request.get_json("force=True")
    if "model" not in data and "year" not in data and "origin" not in data and "phone" not in data:
        error = "Missing "
        if "model" not in data:
            error += "model "
        if "year" not in data:
            error += "year "
        if "origin" not in data:
            error += "origin "
        if "phone" not in data:
            error += "phone "
        error +=  ".Please spefify in Body."
        return Response(json.dumps({"Failure" : error}),status=404, mimetype="application/json")

    message = ""
    if "model" in data:
        vehicles[vehicleId]["model"] = data["model"]
        message += "model "
    if "year" in data:
        vehicles[vehicleId]["year"] = data["year"]
        message += "year "
    if "origin" in data:
        vehicles[vehicleId]["origin"] = data["origin"]
        message += "origin "
    if "phone" in data:
        vehicles[vehicleId]["phone"] = data["phone"]
        message += "phone "
    message += "have been changed"
    return Response(json.dumps(vehicles[vehicleId]),status=200, mimetype="application/json")

@server.route("/api/vehicles/<int:vehicleId>", methods = ["PUT"])
def PutAVehicle(vehicleId):
    data = request.get_json(force=True)
    if "model" not in data or "year" not in data or "origin" not in data:
        error = "Missing "
        if "model" not in data:
            error += "model "
        if "year" not in data:
            error += "year "
        if "origin" not in data:
            error += "origin "
        if "phone" not in data:
            error += "phone "
        error +=  ".Please spefify in Body."
        return Response(json.dumps({"Failure" : error}),status=404, mimetype="application/json")

    message = ""
    if "model" in data:
        vehicles[vehicleId]["model"] = data["model"]
        message += "model "
    if "year" in data:
        vehicles[vehicleId]["year"] = data["year"]
        message += "year "
    if "origin" in data:
        vehicles[vehicleId]["origin"] = data["origin"]
        message += "origin "
    if "phone" in data:
        vehicles[vehicleId]["phone"] = data["phone"]
        message += "phone "
    message += "have been changed"
    return Response(json.dumps(vehicles[vehicleId]),status=200, mimetype="application/json")

@server.route("/api/vehicles/<int:vehicleId>", methods = ["DELETE"])
def DeleteAVehicle(vehicleId):
    for vehicle in vehicles:
        if vehicle["id"] == vehicleId:
            vehicles.remove(vehicle)
            return Response(response=(json.dumps({"Success" : "Deleted"})), status=204, mimetype="application/json")
        error = "There is no such vehicle in vehicles"
        return Response(json.dumps({"Failure" : error}),status=400,mimetype="application/json")

@server.route("/api/phones", methods = ["GET"])
def GetAllPhones():
    try:
        phonesRequest = requests.get(childURL + "phones/")
    except requests.exceptions.RequestException as e:
        return Response(json.dumps({"Failure" : "Failed to connect to server"}),status="503",mimetype="application/json")
    if response.status_code == 400 or response.status_code == 404:
        return jsonify(phonesRequest.json())

@server.route("/api/phones", methods = ["POST"])
def PostAPhone():
    data = request.get_json(force=True)
    try:
        response = requests.post(childURL + "phones", json=data,)
    except requests.exceptions.RequestException as e:
        return Response(json.dumps({"Failure" : "Failed to connect to server"}),status="503",mimetype="application/json")
    if response.status_code == 400 or response.status_code == 404:
        return Response(json.dumps({"Failure" : response.text}),status=response.status_code,mimetype="application/json")
    return Response(json.dumps({"Success" : response.text}),status=response.status_code,mimetype="application/json")

@server.route("/api/vehicles/<int:vehicleId>/phone", methods = ["GET"])
def GetAPhoneFromVehicle(vehicleId):
    for vehicle in vehicles:
        if vehicle["id"] == vehicleId:
            response = requests.get(childURL + "phones/" + vehicle["phone"])
            return jsonify(response.json())
    error = "There is no vehicle with such id! "
    return Response(json.dumps({"Failure" : error}),status=404, mimetype="application/json")

@server.route("/api/all", methods = ["GET"])
def GetAllVehiclesWithPhones():
    tempVehicles = []
    for vehicle in vehicles:
        vehicleCopy = vehicle.copy()
        try:
            response = requests.get(childURL + "phones/" + vehicleCopy["phone"])
        except requests.exceptions.RequestException as e:
            return Response(json.dumps({"Failure" : "Failed to connect to server"}),status="503",mimetype="application/json")
        vehicleCopy["phone"] = response.json();
        tempVehicles.append(vehicleCopy)
    return jsonify(tempVehicles)

@server.route("/api/all", methods = ["POST"])
def PostAVehicleWithAPhone():
    data = request.get_json(force=True)
    try:
        response = requests.post(childURL + "phones/", json=data["phone"])
    except requests.exceptions.RequestException as e:
        return Response(json.dumps({"Failure" : "Failed to connect to server"}),status="503",mimetype="application/json")

    if response.status_code == 400 or response.status_code == 404:
        return Response(json.dumps({"Failure" : response.text}),status=response.status_code,mimetype="application/json")

    if "model" in data and "year" in data and "origin" in data and "phone" in data:
        global currentId
        vehicle ={
            "id": currentId,
            "model": data["model"],
            "year": data["year"],
            "origin": data["origin"],
            "phone": response.headers["id"]
        }
        vehicles.append(vehicle)
        currentId += 1
        return Response(response=(json.dumps({"Success":"Vehicle added", "id" : str(currentId-1)})), status=201, headers={"location": "/api/vehicles/"+str(currentId-1) }, mimetype="application/json")
    else:
        error = "Missing "
        if "model" not in data:
            error += "model "
        if "year" not in data:
            error += "year "
        if "origin" not in data:
            error += "origin "
        if "phone" not in data:
            error += "phone "
        error +=  ".Please spefify in Body."
        return Response(json.dumps({"Failure" : error}),status=400,mimetype="application/json")

@server.route("/api/all/<int:vehicleId>", methods = ["GET"])
def GetOneVehicleWithPhone(vehicleId):
    for vehicle in vehicles:
        if vehicle["id"] == vehicleId:
            vehicleCopy = vehicle.copy()
            try:
                response = requests.get(childURL + "phones/" + vehicle["phone"])
            except requests.exceptions.RequestException as e:
                return Response(json.dumps({"Failure" : "Failed to connect to server"}),status="503",mimetype="application/json")
            vehicleCopy["phone"] = response.json();
            return jsonify(vehicleCopy)
    error = "There is no vehicle with such id! "
    return Response(json.dumps({"Failure" : error}),status=404, mimetype="application/json")

@server.route("/api/all/<int:vehicleId>", methods = ["PATCH"])
def PatchAVehicleInAll(vehicleId):
    data = request.get_json(force=True)
    if "model" not in data and "year" not in data and "origin" not in data and "phone" not in data:
        error = "Missing "
        if "model" not in data:
            error += "model "
        if "year" not in data:
            error += "year "
        if "origin" not in data:
            error += "origin "
        if "phone" not in data:
            error += "phone "
        error +=  ".Please spefify in Body."
        return Response(json.dumps({"Failure" : error}),status=404, mimetype="application/json")

    message = ""
    if "model" in data:
        vehicles[vehicleId]["model"] = data["model"]
        message += "model "
    if "year" in data:
        vehicles[vehicleId]["year"] = data["year"]
        message += "year "
    if "origin" in data:
        vehicles[vehicleId]["origin"] = data["origin"]
        message += "origin "
    if "phone" in data:
        try:
            requests.patch(childURL + "phones/" + vehicles[vehicleId]["phone"], json = data["phone"])
        except requests.exceptions.RequestException as e:
            return Response(json.dumps({"Failure" : "Failed to connect to server"}),status="503",mimetype="application/json")
        message += "phone "
    message += "have been changed"
    return Response(json.dumps(vehicles[vehicleId]),status=200, mimetype="application/json")

@server.route("/api/all/<int:vehicleId>", methods = ["PUT"])
def PutAVehicleInAll(vehicleId):
    data = request.get_json(force=True)
    if "model" not in data and "year" not in data and "origin" not in data and "phone" not in data:
        error = "Missing "
        if "model" not in data:
            error += "model "
        if "year" not in data:
            error += "year "
        if "origin" not in data:
            error += "origin "
        if "phone" not in data:
            error += "phone "
        error +=  ".Please spefify in Body."
        return Response(json.dumps({"Failure" : error}),status=404, mimetype="application/json")

    message = ""
    if "model" in data:
        vehicles[vehicleId]["model"] = data["model"]
        message += "model "
    if "year" in data:
        vehicles[vehicleId]["year"] = data["year"]
        message += "year "
    if "origin" in data:
        vehicles[vehicleId]["origin"] = data["origin"]
        message += "origin "
    if "phone" in data:
        try:
            requests.put(childURL + "phones/" + vehicles[vehicleId]["phone"], json = data["phone"])
        except requests.exceptions.RequestException as e:
            return Response(json.dumps({"Failure" : "Failed to connect to server"}),status="503",mimetype="application/json")
        message += "phone "
    message += "have been changed"
    return Response(json.dumps(vehicles[vehicleId]),status=200, mimetype="application/json")

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000, debug=True)



