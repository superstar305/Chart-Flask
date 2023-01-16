import json

from flask import Blueprint, request

with open('Database/data.json') as file:
    file_contents = file.read()

router = Blueprint('api', __name__)

@router.route('/projectportfoliodemand/<string:id>', methods=['GET'])
def getProjectDemand(id):
    data = json.loads(file_contents)
    return { 'project': data['Project'], 'portfolio': data['Portfolio'][id] }, 200

@router.route('/resourceportfoliocapacity', methods=['POST'])
def getResourceCapacity():
    req = request.get_json()
    content = json.loads(file_contents)
    resources = content['Resources']
    return { 'data': resources[req['portfolio']][req['resource']]}, 200