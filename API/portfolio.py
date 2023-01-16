import graphene
import uuid
from .utils import input_to_dictionary
from graphene_sqlalchemy import SQLAlchemyObjectType
from models import db, Portfolio as PortfolioModel
from graphene import relay, InputObjectType, Mutation

class PortfolioAttribute:
  WorkspaceId = graphene.Int()
  Name = graphene.String()
  StatusDate = graphene.Date()
  CreatedByUserId = graphene.Int()

class Portfolio(SQLAlchemyObjectType):

  class Meta:
    model = PortfolioModel
    interfaces = (relay.Node,)
  
class CreatePortfolioInput(InputObjectType, PortfolioAttribute):
  pass

class CreatePortfolio(Mutation):
  portfolio = graphene.Field(lambda: Portfolio)

  class Arguments:
    input = CreatePortfolioInput(required=True)
  
  def mutate(self, info, input):
    data = input_to_dictionary(input)
    data['Id'] = uuid.uuid4()
    data['LastModifiedByUserId'] = data['CreatedByUserId']

    new_portfolio = PortfolioModel(**data)
    new_portfolio.save()

    return CreatePortfolio(portfolio=new_portfolio)

class UpdatePortfolioInput(InputObjectType, PortfolioAttribute):
  Id = graphene.String()
  LastModifiedByUserId = graphene.Int()

class UpdatePortfolio(Mutation):
  portfolio = graphene.Field(lambda: Portfolio)
  ok = graphene.Boolean()

  class Arguments:
    input = UpdatePortfolioInput(required=True)

  def mutate(self, info, input):
    data = input_to_dictionary(input)

    portfolio = db.session.query(PortfolioModel).filter_by(Id=data['Id']).first()
    
    portfolio.Name = data['Name']
    portfolio.WorkspaceId = data['WorkspaceId']
    portfolio.StatusDate = data['StatusDate']
    portfolio.CreatedByUserId =  data['CreatedByUserId']
    portfolio.LastModifiedByUserId = data['LastModifiedByUserId']

    db.session.commit()

    return CreatePortfolio(ok=True, portfolio=portfolio)

class DeletePortfolioInput(InputObjectType, PortfolioAttribute):
  Id = graphene.Int()

class DeletePortfolio(Mutation):
  portfolio = graphene.Field(lambda: Portfolio)
  ok = graphene.Boolean()

  class Arguments:
    input = DeletePortfolioInput(required=True)
  
  def mutate(self, info, input):
    data = input_to_dictionary(input)

    portfolio = db.session.query(PortfolioModel).filter_by(Id=data['Id']).first()

    if portfolio:
      portfolio.remove()
      return DeletePortfolio(ok=True)
      
    return DeletePortfolio(ok=False)

