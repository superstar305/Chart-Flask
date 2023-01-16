import graphene
from .utils import input_to_dictionary
from graphene_sqlalchemy import SQLAlchemyObjectType
from models import db, Workspace as WorkspaceModel
from graphene import relay, InputObjectType, Mutation
from datetime import datetime

class WorkspaceAttribute:
  TenantId = graphene.Int()
  Name = graphene.String()
  StatusDate = graphene.Date()
  Description = graphene.String()
  CreatedByUserId = graphene.Int()
  SharedUsers = graphene.String()

class Workspace(SQLAlchemyObjectType):

  class Meta:
    model = WorkspaceModel
    interfaces = (relay.Node,)
  
class CreateWorkspaceInput(InputObjectType, WorkspaceAttribute):
  pass

class CreateWorkspace(Mutation):
  workspace = graphene.Field(lambda: Workspace)

  class Arguments:
    input = CreateWorkspaceInput(required=True)
  
  def mutate(self, info, input):
    data = input_to_dictionary(input)
    
    new_workspace = WorkspaceModel(**data)
    new_workspace.save()

    return CreateWorkspace(workspace=new_workspace)

class UpdateWorkspaceInput(InputObjectType, WorkspaceAttribute):
  Id = graphene.Int()

class UpdateWorkspace(Mutation):
  workspace = graphene.Field(lambda: Workspace)

  class Arguments:
    input = UpdateWorkspaceInput(required=True)

  def mutate(self, info, input):
    data = input_to_dictionary(input)

    uworkspace = db.session.query(WorkspaceModel).filter_by(Id=data['Id']).first()

    uworkspace.Name = data['Name']
    uworkspace.TenantId = data['TenantId']
    uworkspace.StatusDate = data['StatusDate']
    uworkspace.Descritption = data['Description']
    uworkspace.CreatedByUserId = data['CreatedByUserId']
    uworkspace.SharedUsers = data['SharedUsers']

    db.session.commit()

    return UpdateWorkspace(workspace=uworkspace)

class DeleteWorkspaceInput(InputObjectType, WorkspaceAttribute):
  Id = graphene.Int()

class DeleteWorkspace(Mutation):
  workspace = graphene.Field(lambda: Workspace)

  class Arguments:
    input = DeleteWorkspaceInput(required=True)
  
  def mutate(self, info, input):
    data = input_to_dictionary(input)

    dworkspace = db.session.query(WorkspaceModel).filter_by(Id=data['Id']).first()
    dworkspace.remove()

    return DeleteWorkspace(workspace=dworkspace)

