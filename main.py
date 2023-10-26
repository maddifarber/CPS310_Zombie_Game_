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
        pass

# Define subclasses for each agent type
class Human(Agent):
    def __init__(self, energy_range=(0, 100)):
        super().__init__(AgentType.HUMAN, energy_range)

    def update(self):
        self.energy -= 5

class Zombie(Agent):
    def __init__(self, energy_range=(0, 100)):
        super().__init__(AgentType.ZOMBIE, energy_range)

    def update(self):
        if self.state == AgentState.ALIVE:
            for neighbor in self.neighbors:
                if neighbor.agent_type == AgentType.HUMAN and neighbor.state != AgentState.INFECTED:
                    if random.random() < 0.3:
                        neighbor.state = AgentState.INFECTED
                        neighbor.energy -= 20
                        self.energy += 10
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

    def run_simulation(self):
        for step in range(self.num_steps):
            self.agent_statuses.append([str(agent) for agent in self.agents])

            # TODO
            #   ALIVE counts for each iteration
            agent_counts = {
                AgentType.HUMAN: 0,
                AgentType.ZOMBIE: 0,
                AgentType.DOCTOR: 0,
                AgentType.DEAD: 0
            }

            for agent in self.agents:
                # TODO: Inside this loop, we update ALIVE counts.
                agent.update()
                agent.neighbors = random.sample(self.agents, min(5, self.num_agents))  # Random neighbors

                if agent.state == AgentState.DEAD:
                    agent_counts[AgentType.DEAD] += 1
                    continue
                if agent.state == AgentType.HUMAN:
                    self.population_data[AgentType.HUMAN].append(1)
                elif agent.state == AgentType.ZOMBIE:
                    self.population_data[AgentType.ZOMBIE].append(1)
                elif agent.state == AgentType.DOCTOR:
                    self.population_data[AgentType.DOCTOR].append(1)

            # Correctly access the corresponding list based on agent_type
            # Summarize ALIVE counts.
            self.population_data[AgentType.HUMAN].append(agent_counts[AgentType.HUMAN])
            self.population_data[AgentType.DOCTOR].append(agent_counts[AgentType.DOCTOR])
            self.population_data[AgentType.ZOMBIE].append(agent_counts[AgentType.ZOMBIE])

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
            if agent_type in self.population_data and self.population_data[agent_type]:
                plt.plot(range(self.num_steps), self.population_data[agent_type], label=agent_type)
        plt.xlabel("Time Step")
        plt.ylabel("Population Count")
        plt.legend()
        plt.savefig("population_plot.png")
        plt.show()


if __name__ == "__main__":
    num_agents_param = 100
    num_steps_param = 50
    game = ZombieGame(num_agents_param, num_steps_param)
    game.run_simulation()


