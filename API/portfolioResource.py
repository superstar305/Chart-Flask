import graphene
from .utils import input_to_dictionary
from graphene_sqlalchemy import SQLAlchemyObjectType
from models import db, Resource as ResourceModel, PortfolioResource as PortResourceModel
from graphene import relay, InputObjectType, Mutation

class PortResourceAttribute:
  PortfolioId = graphene.String()
  ResourceId = graphene.Int()
  AdjustedCapacity = graphene.String()

class PortResource(SQLAlchemyObjectType):

  class Meta:
    model = PortResourceModel
    interfaces = (relay.Node,)
  
class CreatePortResourceInput(InputObjectType, PortResourceAttribute):
  pass

class CreatePortResource(Mutation):
  portResource = graphene.Field(lambda: PortResource)

  class Arguments:
    input = CreatePortResourceInput(required=False)
  
  def mutate(self, info, input):
    data = input_to_dictionary(input)

    resource = db.session.query(ResourceModel).filter_by(Id=data['ResourceId']).first()
    data['AdjustedCapacity'] = resource.BaselineCapacity

    new_portResource = PortResourceModel(**data)
    new_portResource.save()

    return CreatePortResource(portResource=new_portResource)

class UpdatePortResourceInput(InputObjectType, PortResourceAttribute):
  Id = graphene.Int()

class UpdatePortResource(Mutation):
  portResource = graphene.Field(lambda: PortResource)
  ok = graphene.Boolean()

  class Arguments:
    input = UpdatePortResourceInput(required=True)

  def mutate(self, info, input):
    data = input_to_dictionary(input)

    portResource = db.session.query(PortResourceModel).filter_by(Id=data['Id']).first()
    
    portResource.PortfolioId = data['PortfolioId']
    portResource.ResourceId = data['ResourceId']
    portResource.AdjustedCapacity = data['AdjustedCapacity']

    db.session.commit()

    return UpdatePortResource(ok=True, portResource=portResource)

class DeletePortResourceInput(InputObjectType, PortResourceAttribute):
  Id = graphene.Int()

class DeletePortResource(Mutation):
  portResource = graphene.Field(lambda: PortResource)
  ok = graphene.Boolean()

  class Arguments:
    input = DeletePortResourceInput(required=True)
  
  def mutate(self, info, input):
    data = input_to_dictionary(input)

    portResource = db.session.query(PortResourceModel).filter_by(Id=data['Id']).first()
    db.session.delete(portResource)
    db.session.commit()

    return DeletePortResource(ok=True)

