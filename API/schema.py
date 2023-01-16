from graphene_sqlalchemy import SQLAlchemyConnectionField
from .workspace import Workspace, CreateWorkspace, UpdateWorkspace, DeleteWorkspace
from .project import Project, CreateProject, UpdateProject, DeleteProject
from .mresource import MResource, CreateResource, UpdateResource, DeleteResource
from .portfolio import Portfolio, CreatePortfolio, UpdatePortfolio, DeletePortfolio
from .portfolioProject import PortProject, CreatePortProject, UpdatePortProject, DeletePortProject
from .portfolioResource import PortResource, CreatePortResource, UpdatePortResource, DeletePortResource
from .projectResource import ProResource, CreateProResource, UpdateProResource, DeleteProResource
from .portfolioProRes import PortfolioProRes, CreatePortfolioProRes, UpdatePortfolioProRes, DeletePortfolioProRes

import graphene

class Query(graphene.ObjectType):
  """Nodes which can be queried by this API."""
  
  workspace = graphene.relay.Node.Field(Workspace)
  workspaceList = SQLAlchemyConnectionField(Workspace)

  project = graphene.relay.Node.Field(Project)
  projectList = SQLAlchemyConnectionField(Project)

  resource = graphene.relay.Node.Field(MResource)
  resourceList = SQLAlchemyConnectionField(MResource)

  portfolio = graphene.relay.Node.Field(Portfolio)
  portfolioList = SQLAlchemyConnectionField(Portfolio)

  portProject = graphene.relay.Node.Field(PortProject)
  portProjectList = SQLAlchemyConnectionField(PortProject)

  portResource = graphene.relay.Node.Field(PortResource)
  portResourceList = SQLAlchemyConnectionField(PortResource)

  proResource = graphene.relay.Node.Field(ProResource)
  proResourceList = SQLAlchemyConnectionField(ProResource)

  portfolioProRes = graphene.relay.Node.Field(PortfolioProRes)
  portfolioProResList = SQLAlchemyConnectionField(PortfolioProRes)


class Mutation(graphene.ObjectType):
  """Mutations which can be performed by this API."""
  
  createWorkspace = CreateWorkspace.Field()
  updateWorkspace = UpdateWorkspace.Field()
  deleteWorkspace = DeleteWorkspace.Field()

  createProject = CreateProject.Field()
  updateProject = UpdateProject.Field()
  deleteProject = DeleteProject.Field()

  createResource = CreateResource.Field()
  updateResource = UpdateResource.Field()
  deleteResource = DeleteResource.Field()

  createPortfolio  = CreatePortfolio .Field()
  updatePortfolio  = UpdatePortfolio .Field()
  deletePortfolio  = DeletePortfolio .Field()

  createPortProject = CreatePortProject.Field()
  updatePortProject = UpdatePortProject.Field()
  deletePortProject = DeletePortProject.Field()

  createPortResource = CreatePortResource.Field()
  updatePortResource = UpdatePortResource.Field()
  deletePortResource = DeletePortResource.Field()

  createProResource = CreateProResource.Field()
  updateProResource = UpdateProResource.Field()
  deleteProResource = DeleteProResource.Field()

  createPortfolioProRes = CreatePortfolioProRes.Field()
  updatePortfolioProRes = UpdatePortfolioProRes.Field()
  deletePortfolioProRes = DeletePortfolioProRes.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)