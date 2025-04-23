from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
import os, weaviate

from weaviate.classes.init import Auth
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators
cllm = LLM(
            model="cerebras/llama3.1-8b",
            temperature=0.7,
            max_tokens=8192
        )

weaviate_url = os.environ["WEAVIATE_URL"]
weaviate_api_keyz = os.environ["WEAVIATE_API_KEY"]
'''
weaviate_tool = WeaviateVectorSearchTool(
    collection_name='awscluster',
    limit=3,
    weaviate_api_key = weaviate_api_keyz,
    weaviate_cluster_url = weaviate_url,
)

# Best practice: store your credentials in environment variables

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=weaviate_url,
    auth_credentials=Auth.api_key(weaviate_api_keyz),
)


resp = requests.get(
    "https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/jeopardy_tiny.json"
)
data = json.loads(resp.text)

questions = client.collections.get("Question")

with questions.batch.rate_limit(requests_per_minute=200) as batch:
    for d in data:
        batch.add_object(
            {
                "answer": d["Answer"],
                "question": d["Question"],
                "category": d["Category"],
            }
        )
        if batch.number_errors > 10:
            print("Batch import stopped due to excessive errors.")
            break

failed_objects = questions.batch.failed_objects
if failed_objects:
    print(f"Number of failed imports: {len(failed_objects)}")
    print(f"First failed object: {failed_objects[0]}")

client.close()  # Free up resources
'''

@CrewBase
class Mentalhealth():
    """Mentalhealth crew"""
      
    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def therapist_cbt(self) -> Agent:
        return Agent(
            config=self.agents_config['therapist_cbt'],
            verbose=True,
            llm=cllm,
        )
    
    @agent
    def therapist_humanistic(self) -> Agent:
        return Agent(
            config=self.agents_config['therapist_humanistic'],
            verbose=True,
            llm=cllm,
        )
    
    @agent
    def therapist_psychodynamic(self) -> Agent:
        return Agent(
            config=self.agents_config['therapist_psychodynamic'],
            verbose=True,
            llm=cllm,
        )
    
    @agent
    def therapy_summarizer(self) -> Agent:
        return Agent(
            config=self.agents_config['therapy_summarizer'],
            verbose=True,
            llm=cllm,
        )

    @agent
    def mood_rater(self) -> Agent:
        return Agent(
            config=self.agents_config['mood_rater'],
            verbose=True,
            llm=cllm,
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def cbt_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['cbt_analysis_task'],
            output_file='cbt_response.md'
        )
    
    @task
    def humanistic_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['humanistic_analysis_task'],
            output_file='humanistic_response.md'
        )
    
    @task
    def psychodynamic_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['psychodynamic_analysis_task'],
            output_file='psychodynamic_response.md'
        )
    
    @task
    def therapy_summary_task(self) -> Task:
        return Task(
            config=self.tasks_config['therapy_summary_task'],
            output_file='therapy_response.md'
        )

    @task
    def mood_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['mood_analysis_task'],
            output_file='mood_analysis.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Mentalhealth crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge
        
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
