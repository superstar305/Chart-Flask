import graphene
from .utils import input_to_dictionary
from graphene_sqlalchemy import SQLAlchemyObjectType
from models import db, ProjectResource as ProResourceModel
from graphene import relay, InputObjectType, Mutation

class ProResourceAttribute:
  ProjectId = graphene.Int()
  ResourceId = graphene.Int()
  BaselineDemand = graphene.String()

class ProResource(SQLAlchemyObjectType):

  class Meta:
    model = ProResourceModel
    interfaces = (relay.Node,)

class CreateProResourceInput(InputObjectType, ProResourceAttribute):
  pass

class CreateProResource(Mutation):
  proResource = graphene.Field(lambda: ProResource)

  class Arguments:
    input = CreateProResourceInput(required=True)

  def mutate(self, info, input):
    data = input_to_dictionary(input)

    new_proResource = ProResourceModel(**data)
    new_proResource.save()

    return CreateProResource(proResource = new_proResource)

class SearchProResourceInput(InputObjectType, ProResourceAttribute):
  pass

class UpdateProResource(Mutation):
  proResource = graphene.Field(lambda: ProResource)
  ok = graphene.Boolean()

  class Arguments:
    input = SearchProResourceInput(required=False)

  def mutate(self, info, input):
    data = input_to_dictionary(input)

    uproResource = db.session.query(ProResourceModel).filter_by(ProjectId = data['ProjectId'], ResourceId = data['ResourceId']).first()

    uproResource.BaselineDemand = data['BaselineDemand']

    db.session.commit()

    return UpdateProResource(ok = True)

class DeleteProResource(Mutation):
  ok = graphene.Boolean()

  class Arguments:
    input = SearchProResourceInput(required=False)
  
  def mutate(self, info, input):
    data = input_to_dictionary(input)

    proResource = db.session.query(ProResourceModel).filter_by(ProjectId = data['ProjectId'], ResourceId = data['ResourceId']).first()
    
    if proResource:
      proResource.remove()
      return DeleteProResource(ok = True)

    return DeleteProResource(ok = False)