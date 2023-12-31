import random
import pandas as pd
import matplotlib.pyplot as plt


# Define agent states
class AgentState:
    ALIVE = "Alive"
    INFECTED = "Infected"
    DEAD = "Dead"


# Define agent types
class AgentType:
    HUMAN = "Human"
    ZOMBIE = "Zombie"
    DOCTOR = "Doctor"
    DEAD = "Dead"


# Define the Agent class with inheritance
class Agent:
    id_counter = 0

    def __init__(self, agent_type, energy_range=(0, 100)):
        self.id = Agent.id_counter
        Agent.id_counter += 1
        self.agent_type = agent_type
        self.energy = random.randint(energy_range[0], energy_range[1])
        self.state = AgentState.ALIVE
        self.neighbors = []

    def __str__(self):
        return f"{self.agent_type} (ID: {self.id}, Energy: {self.energy}, State: {self.state})"

    def update(self):
        # Check if the agent is dead based on energy level
        if self.energy <= 0 and self.state != AgentState.DEAD:
            print(f"Agent {self.id} is dead. Energy: {self.energy}")
            self.state = AgentState.DEAD
        else:
            print(f"Agent {self.id} is alive. Energy: {self.energy}, State: {self.state}")


# Define subclasses for each agent type
class Human(Agent):
    def __init__(self, energy_range=(90, 100)):
        super().__init__(AgentType.HUMAN, energy_range)

    def update(self):
        self.energy -= 2
        if self.energy <= 0 and self.state != AgentState.DEAD:
            self.state = AgentState.DEAD


class Zombie(Agent):
    def __init__(self, energy_range=(0, 100)):
        super().__init__(AgentType.ZOMBIE, energy_range)

    def update(self):
        for neighbor in self.neighbors:
            if neighbor.agent_type == AgentType.HUMAN and neighbor.state == AgentState.ALIVE:
                if random.random() < 0.3:
                    neighbor.state = AgentState.INFECTED
                    neighbor.energy -= 20
                    self.energy += 10

                    if neighbor.energy <= 0:
                        neighbor.state = AgentState.DEAD
                        self.state = AgentState.DEAD
                    break


class Doctor(Agent):
    def __init__(self, energy_range=(0, 100)):
        super().__init__(AgentType.DOCTOR, energy_range)

    def update(self):
        if self.state == AgentState.INFECTED:
            if random.random() < 0.4:
                self.state = AgentState.ALIVE
                self.energy -= 30


# Create a simulation environment
class ZombieGame:

    def __init__(self, num_agents, num_steps, energy_range=(0, 100)):
        self.agents = []
        self.num_agents = num_agents
        self.num_steps = num_steps
        self.agent_statuses = []  # To store statuses over time

        # Initialize population_data dictionary with keys for each agent type
        # TODO
        #   This is ALIVE count.
        self.population_data = {
            AgentType.HUMAN: [],
            AgentType.ZOMBIE: [],
            AgentType.DOCTOR: [],
            AgentType.DEAD: []
        }

        agent_counts = {
            AgentType.HUMAN: 0,
            AgentType.ZOMBIE: 0,
            AgentType.DOCTOR: 0,
            AgentType.DEAD: 0
        }

        for _ in range(num_agents):
            agent_type = random.choice([AgentType.HUMAN, AgentType.ZOMBIE, AgentType.DOCTOR])
            agent = None
            if agent_type == AgentType.HUMAN:
                agent = Human(energy_range)
            elif agent_type == AgentType.ZOMBIE:
                agent = Zombie(energy_range)
            elif agent_type == AgentType.DOCTOR:
                agent = Doctor(energy_range)
            self.agents.append(agent)
            agent_counts[agent_type] += 1

        for agent_type in agent_counts:
            self.population_data[agent_type].append(agent_counts[agent_type])

    def run_simulation(self):
        for step in range(self.num_steps):
            for agent in self.agents:
                agent.update()


            self.agents = [agent for agent in self.agents if agent.state != AgentState.DEAD]

            self.agent_statuses.append([str(agent) for agent in self.agents])

            agent_counts_before = {
                AgentType.HUMAN: 0,
                AgentType.ZOMBIE: 0,
                AgentType.DOCTOR: 0,
                AgentType.DEAD: 0
            }

            for agent in self.agents:
                if agent.state == AgentState.DEAD:
                    agent_counts_before[AgentType.DEAD] += 1
                elif agent.state == AgentType.HUMAN:
                    agent_counts_before[AgentType.HUMAN] += 1
                elif agent.state == AgentType.ZOMBIE:
                    agent_counts_before[AgentType.ZOMBIE] += 1
                elif agent.state == AgentType.DOCTOR:
                    agent_counts_before[AgentType.DOCTOR] += 1

            for agent in self.agents:
                agent.update()

            agent_counts_after = {
                AgentType.HUMAN: 0,
                AgentType.ZOMBIE: 0,
                AgentType.DOCTOR: 0,
                AgentType.DEAD: 0
            }

            for agent in self.agents:
                if agent.state == AgentState.DEAD:
                    agent_counts_after[AgentType.DEAD] += 1
                elif agent.state == AgentType.HUMAN:
                    agent_counts_after[AgentType.HUMAN] += 1
                elif agent.state == AgentType.ZOMBIE:
                    agent_counts_after[AgentType.ZOMBIE] += 1
                elif agent.state == AgentType.DOCTOR:
                    agent_counts_after[AgentType.DOCTOR] += 1

            # Summarize counts for each state after agents are updated
            self.population_data[AgentType.HUMAN].append(agent_counts_after[AgentType.HUMAN])
            self.population_data[AgentType.DOCTOR].append(agent_counts_after[AgentType.DOCTOR])
            self.population_data[AgentType.ZOMBIE].append(agent_counts_after[AgentType.ZOMBIE])
            self.population_data[AgentType.DEAD].append(agent_counts_after[AgentType.DEAD])

            self.agent_statuses.append([str(agent) for agent in self.agents])

        self.save_simulation_data()
        self.plot_simulation_results()

    def save_simulation_data(self):
        # Create an empty list to store step-wise data
        step_data = []

        for step in range(self.num_steps):
            # Each step contains a list of agent statuses
            step_data.append([f"Step_{step}"] + self.agent_statuses[step])

        # Create a DataFrame from the list of step data
        status_df = pd.DataFrame(step_data,
                                 columns=["Step"] + [f"Agent_{i}" for i in range(len(self.agent_statuses[0]))])

        # Save the DataFrame to a CSV file
        status_df.to_csv("agent_statuses.csv", index=False)

    def plot_simulation_results(self):
        plt.figure(figsize=(12, 6))
        for agent_type in AgentType.__dict__.values():
            if isinstance(agent_type, str) and agent_type in self.population_data and self.population_data[agent_type]:
                data_length = min(len(self.population_data[agent_type]), self.num_steps)
                plt.plot(range(data_length), self.population_data[agent_type][:data_length], label=agent_type)
        plt.xlabel("Time Step")
        plt.ylabel("Population Count")
        plt.legend()
        plt.savefig("population_plot.png")
        plt.show()

        plt.ioff()
        plt.show()


if __name__ == "__main__":
    num_agents_param = 100
    num_steps_param = 5
    game = ZombieGame(num_agents_param, num_steps_param)
    game.run_simulation()
