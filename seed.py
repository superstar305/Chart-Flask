from app import app, bcrypt
from models import Tenant, User, Workspace, Project, Resource, ProjectResource, Portfolio, PortfolioResource, PortfolioProject,PortfolioProjectResource
from models import db

import re
import json
import random
from datetime import datetime

def password(password_plaintext):
    if not re.match('^(?=.*\W)(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{5,20}$', password_plaintext):
      raise AssertionError('Password must contain 1 capital, 1 number, one symbol and be between 5 and 20 charetars long.')
    return bcrypt.generate_password_hash(password_plaintext).decode('utf-8')

with app.app_context():

  db.drop_all()
  db.create_all()
  # Add a new Tenant
  developer = Tenant( Name='Developer' )
  developer.save()

  # Add a new User to that Tenant
  user = User( 
    Name='Dan Hickman',
    Email = 'numeric0900@gmail.com',
    Password = password('QWE@#$asd234'),
    TenantId = 1,
    AccountTypeId = ''
  )
  user.save()

  # Add a new Workspace to the Tenant

  workspace = Workspace(
    TenantId = 1,
    Name = 'team',
    StatusDate = datetime.strptime('2025-05-01', '%Y-%m-%d').date(),
    Description = 'chart to manage team member',
    CreatedByUserId = 1
  )
  workspace.save()

  # Add 3 Resources to that Workspace
  Resources = ['Developers', 'QA', 'Business Analyist']
  dev = []
  BaselineCapacity = []
  for i in range(3):
    y = []
    for j in range(24):
      y.append(random.randrange(5, 30))
    BaselineCapacity.append(y)
    dev.append(
      Resource(
        WorkspaceId = 1,
        Name = Resources[i],
        BaselineCapacity = json.dumps(BaselineCapacity[i]),
        StartAt = datetime.strptime('2023-01-01', '%Y-%m-%d').date(),
        Tags = ''
      )
    )

  db.session.add_all(dev)
  db.session.commit()
  print('Resources Created!')

  # Add 10 Projects to that Workspace
  BaselineStartDate = ['2023-01-01', '2023-02-01', '2023-03-01', '2023-04-01', '2023-05-01', '2023-06-01', '2023-07-01', '2023-08-01', '2023-09-01', '2023-10-01']
  Name = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
  Projects = []
  Priority = []
  for i in range(10):
    Priority.append(random.randrange(1, 30))
    Projects.append(
      Project(
        WorkspaceId = 1,
        Name = Name[i],
        BaselineStartDate = datetime.strptime(BaselineStartDate[i], '%Y-%m-%d').date(),
        BaselinePriority = Priority[i]
      )
    )

  db.session.add_all(Projects)
  print('Projects Created!')

  ProjectResources = []
  BaselineDemand = []
  for i in range(10):
    for j in range(3):
      x = []
      for y in range(15):
        x.append(random.randrange(2, 15))
      BaselineDemand.append(x)
      ProjectResources.append(
        ProjectResource(
          ProjectId = (i + 1),
          ResourceId = (j + 1),
          BaselineDemand = json.dumps(BaselineDemand[i])
        )
      )      

  db.session.add_all(ProjectResources)
  db.session.commit()
  print('ProjectResources Created!')

  # Create a Portfolio in that Workspace
  Port = Portfolio(
    Id = '2ca64e7b-7d3e-4337-86cf-f3a4e0b783d4',
    WorkspaceId = 1,
    Name = 'Developer',
    StatusDate = datetime.strptime('2023-01-01', '%Y-%m-%d').date(),
    CreatedByUserId = 1,
    LastModifiedByUserId = 1
  )

  db.session.add(Port)
  db.session.commit()
  print('Portfolio Created!')

  # For the 3 resources, create a PortfolioResource row

  PortfolioResources = []
  for i in range(3):
    PortfolioResources.append(
      PortfolioResource(
        PortfolioId = '2ca64e7b-7d3e-4337-86cf-f3a4e0b783d4',
        ResourceId = (i + 1),
        AdjustedCapacity = json.dumps(BaselineCapacity[i])
      )
    )
  
  db.session.add_all(PortfolioResources)
  db.session.commit()
  print('PortfolioResources Created!')

  # For the 10 projects, create a PortfolioProject row in the db.

  PortfolioProjects = []
  for i in range(10):
    PortfolioProjects.append(
      PortfolioProject(
        PortfolioId = '2ca64e7b-7d3e-4337-86cf-f3a4e0b783d4',
        ProjectId = (i+1),
        AdjustedStartDate = BaselineStartDate[i],
        AdjustedPriority = Priority[i],
        IsSelected = 0,
      )
    )

  db.session.add_all(PortfolioProjects)
  db.session.commit()
  print('PortfolioProjects Created!')

  # Create a PortfolioProjectResource for each of the 3 

  PortfolioProjectResources = []
  for i in range(10):
    for j in range(3):
      PortfolioProjectResources.append(
        PortfolioProjectResource(
          PortfolioProjectId = (i + 1),
          PortfolioResourceId = (j + 1),
          AdjustDemand = json.dumps(BaselineDemand[i])
        )
      )

  db.session.add_all(PortfolioProjectResources)
  print('PortfolioProjectResources Created!')

  db.session.commit()

  print('Adding to database...')

  print('Everything works!')
  
