from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

load_dotenv()

@CrewBase
class T():
    """T crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools

    llm = ChatGroq(
        model="groq/llama3-70b-8192",
        groq_api_key=os.getenv("GROQ_API_KEY"),
    )


    @agent
    def input_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['input_agent'],
            verbose=False,
            llm=self.llm  # Add this to ensure the model is properly set

        )
    
    @agent
    def parser_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['parser_agent'],
            verbose=False,
            llm=self.llm
        )
    
    @agent
    def validator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['validator_agent'],
            verbose=False,
            llm=self.llm
        )
    
    @agent
    def formatter_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['formatter_agent'],
            verbose=False,
            llm=self.llm
        )
    
    @agent
    def writer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['writer_agent'],
            verbose=False,
            llm=self.llm
        )


    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def Intake_Radiology_Notes_Task(self) -> Task:
        return Task(
            config=self.tasks_config['Intake_Radiology_Notes_Task'],
        )

    #@task
    #def Transcribe_Audio_Input_Task(self) -> Task:
        #return Task(
            #config=self.tasks_config['Transcribe_Audio_Input_Task'],
        #)
    
    @task
    def Parse_Clinical_Sections_Task(self) -> Task:
        return Task(
            config=self.tasks_config['Parse_Clinical_Sections_Task'],
        )
    
    @task
    def Validate_Medical_Consistency_Task(self) -> Task:
        return Task(
            config=self.tasks_config['Validate_Medical_Consistency_Task'],
        )
    
    @task
    def Format_Report_to_Template_Task(self) -> Task:
        return Task(
            config=self.tasks_config['Format_Report_to_Template_Task'],
        )
    
    @task
    def Generate_Final_Report_Task(self) -> Task:
        return Task(
            config=self.tasks_config['Generate_Final_Report_Task'],
            output_file='report_final.docx',
            output_format='docx'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the T crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            llm=self.llm,

            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
