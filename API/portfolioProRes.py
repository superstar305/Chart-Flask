import graphene
from .utils import input_to_dictionary
from graphene_sqlalchemy import SQLAlchemyObjectType
from models import db, ProjectResource as ProResourceModel, PortfolioProjectResource as PortfolioProResModel
from graphene import relay, InputObjectType, Mutation

class PortfolioProResAttribute:
  PortfolioProjectId = graphene.Int()
  PortfolioResourceId = graphene.Int()
  AdjustDemand = graphene.String()

class PortfolioProRes(SQLAlchemyObjectType):

  class Meta:
    model = PortfolioProResModel
    interfaces = (relay.Node,)

class CreatePortfolioProResInput(InputObjectType, PortfolioProResAttribute):
  pass

class CreatePortfolioProRes(Mutation):
  portfolioProRes = graphene.Field(lambda: PortfolioProRes)

  class Arguments:
    input = CreatePortfolioProResInput(required=False)

  def mutate(self, info, input):
    data = input_to_dictionary(input)

    projectResource = db.session.query(ProResourceModel).filter_by(ProjectId = data['PortfolioProjectId'], ResourceId = data['PortfolioResourceId']).first()

    data['AdjustDemand'] = projectResource.BaselineDemand 

    new_portfolioProRes = PortfolioProResModel(**data)
    new_portfolioProRes.save()

    return CreatePortfolioProRes(portfolioProRes = new_portfolioProRes)

class SearchPortfolioProRes(InputObjectType, PortfolioProResAttribute):
  pass

class UpdatePortfolioProRes(Mutation):
  portfolioProRes = graphene.Field(lambda: PortfolioProRes)
  ok = graphene.Boolean()

  class Arguments:
    input = SearchPortfolioProRes(required=False)

  def mutate(self, info, input):
    data = input_to_dictionary(input)

    uportfolioProRes = db.session.query(PortfolioProResModel).filter_by(PortfolioProjectId = data['PortfolioProjectId'], PortfolioResourceId = data['PortfolioResourceId']).first()

    uportfolioProRes.AdjustDemand = data['AdjustDemand']

    db.session.commit()

    return UpdatePortfolioProRes(ok = True)

class DeletePortfolioProRes(Mutation):
  ok = graphene.Boolean()

  class Arguments:
    input = SearchPortfolioProRes(required=False)

  def mutate(self, info, input):
    data = input_to_dictionary(input)

    portfolioProRes = db.session.query(PortfolioProResModel).filter_by(PortfolioProjectId = data['PortfolioProjectId'], PortfolioResourceId = data['PortfolioResourceId']).first()

    if portfolioProRes:
      portfolioProRes.remove()
      return DeletePortfolioProRes(ok = True)

    return DeletePortfolioProRes(ok = False)
