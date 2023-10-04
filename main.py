import logging
import numpy as np

###########################################
#   Global Definitions
###########################################
MAX_ITER = 1000

agent_cnt_seed = 100
# Probability of Agents
H_PROB = 0.5
D_PROB = 0.2
Z_PROB = 0.3

# np.random.multinomial
H_ENERGY = 100
D_ENERGY = 100
Z_ENERGY = 100

#  AGENT STATES
ALIVE = 0
INFECTED = 1
DEAD = 2

#ZOMBIE
BITE_PROB = 0.7

#DOCTOR
BITE_EFF = 10

############################################
#   Class Definitions
############################################
class ZombieGameSim:
    # The full list of agents
    m_l_all_agents = None
    # The current moment
    m_current_moment = None


    def __init__(self, agent_cnt_seed):
        self.m_l_all_agents = []
        nd_agent_cnt = np.random.multinomial(agent_cnt_seed, pvals=[H_PROB, D_PROB,Z_PROB])
        self.m_l_all_agents += [Human(H_ENERGY, self) for i in range(nd_agent_cnt[0])]
        self.m_l_all_agents += [Doctor(D_ENERGY, self) for i in range(nd_agent_cnt[0])]
        self.m_l_all_agents += [Zombie(Z_ENERGY, self) for i in range(nd_agent_cnt[0])]

    def start(self):
        self.m_current_moment = 0
        while True:
            if self.m_current_moment >= MAX_ITER:
                break
            while m_l_all_agents > 0:
                Human_init = Human()
                Doctor_init = Doctor()
                Zombie_init = Zombie()
                Human_init()
                Doctor_init()
                Zombie_init()
                for agent in self.m_l_all_agents:
                    agent.update()
                self.m_current_moment += 1
        


    def get_all_agents(self):
        return self.m_l_all_agents

    def get_current_moment(self):
        return self.m_current_moment


    def ts_statement(self):
        print("The number of Alive Humans are:", )
        print("The number of Infected Humans are:", )
        print("The number of Dead Humans are:", )
        print("The number of Alive Doctors are:", )
        print("The number of infected Doctors are:", )
        print("The number of Dead Doctors are:",)
        print("The number of Alive Zombies are:", )
        print("The number of Dead Zombies are:", )


class AbsAgent:

    #Member Variables
    m_state = None

    m_full_energy = None
    #Agent Energy
    m_energy = None
    # The number of neighbors in previous iteration
    m_num_neigh_prev = None
    # The full list of agents
    m_l_all_agents = None
    #The reference of ZombieGameSim
    m_ref_sim = None

    def __init__(self, init_energy, ref_sim):
        """
        Constructor
        :param init_energy: (int) >0 Initial energy for this agent
        """
        #TODO
        #  If anything needs to be initialized
        self.m_state = ALIVE
        if init_energy <= 0:
            logging.error('[AbsAgent:__init__] `init_energy` needs to be a positive integer')
            return
        m.full_energy = 100
        self.m_energy = init_energy
        if ref_sim is None or not isinstance('[AbsAgent:__init__] `ref_sim` needs to be in `ZombieGameSim`.'):
            self.m_ref_sim = ref_sim
            self.m_energy = init_energy

    def get_state(self):
        return m_state

    def update_state(self, new_state):
        self.m_state = new_state


    def _get_life_decay_amount(self):
        life_decay_amount = 5
        return life_decay_amount

    def life_decay(self):
        """
               Decay Agent's energy over time.
               :return: None.
               """
        self.m_energy -= self._get__life__decay__amount()
        super().check_death()

    def life_increases(self):
        self.m_energy += 4
        return self.m_energy


    #Member Methods
    def _check_death(self):
        """
        Check if this agent is about to die.
        :return: None.
        """
        if self.m_energy is not None and self.m_energy <= 0:
            self.m_state = DEAD


    def __get_num_neigh(self):
            """
            update the desired num of neighbors for this agent
            :return: (int) the num of neighbors
            """
            # TODO
            #   Make it vary for each iteration
            return 5

    def _select_neighbors(self):
        """
        Randomly select a specific number on agents as the neighbors.
        :param num_neigh: (int) >0 The number on desired neighbors
        :param l_all_agents: (list of agent instances) A full list of agents in the game.
        :return: (List of agent instances) The current neighbors.
        """
        num_neigh = self.__get
        l_all_agents = self.m_ref_sim.get_all_agents()
        l_neigh_idx = np.random.choice(list(range(len(l_all_agents))), size=m_num_neigh)
        l_neigh = [l_all_agents[idx] for idx in range(len(l_all_agents)) if idx in l_neigh_idx]
        return l_neigh

    def update(self):
        '''
        Update the state as well as the energy, if necessary
        :param self:
        :return: None
        '''
        def bite_success(self):
            if bite_success == 0:
                Human.bitten()
                neigh.change_state(INFECTED)
                neigh.life_decay()

        def new_state(self):
            if self.m_energy == 100 :
               change_state = "ALIVE"
            return














###################################
    # HUMAN CLASS
###################################

class Human(AbsAgent):

    m_bite_start = None

    def get_life_decay_amount(self):
        life_decay_amt = 5
        return life_decay_amt

    def life_decay(self):
        self.m_energy -= self._get_life_decay_amount()
        self._check_death()

    def bitten(self):
        '''
        Record the moment of the bite
        :return: None
        '''
        self.m_bite_start = self.m_ref_sim.get_current_moment()
        print("A human has been bitten!")

    def update(self):
        if self.get_state() == INFECTED:
            cur_moment = self.m_ref_sim.get_current_moment()
            bite_len = cur_momeent - self.m_bite_start
            if bite_len > BITE_EFF and self.get_state() != DEAD:
                self.change_state(ALIVE)
                self.life_increase()
            else:
                self.life_decay()
        elif self.get_state() == INFECTED:
            self.life_decay()



####################################
    # DOCTOR CLASS
####################################

class Doctor(Human):
    m_bite_start = None

    def bitten(self):
        '''
        Record the moment of the bite
        :return: None
        '''
        self.m_bite_start = self.m_ref_sim.get_current_moment()
        print("A human has been bitten!")

    def update(self):
        if self.get_state() == INFECTED:
            cur_moment = self.m_ref_sim.get_current_moment()
            bite_len = cur_momeent - self.m_bite_start
            if bite_len > BITE_EFF and self.get_state() != DEAD:
                self.change_state(ALIVE)
                self.life_increase()
            else:
                self.life_decay()
        elif self.get_state() == ALIVE:
            self.life_increase()



    def cure(self):
        l_neigh = super()._select_neighbors()
        for neigh in l_neigh:
            if not isinstance(neigh, Human):
                continue
            if neigh.get_state() == INFECTED:
                neigh.change_state(ALIVE)
                break


#####################################
    # ZOMBIE CLASS
#####################################

class Zombie(AbsAgent):

    def _get__life__decay__amount(self):
        """
        Compute the life decay amount for the current state.
        :return: (int) The life decay amount
        """
        #  TODO
        #    Make it more fun.
        return 1

        # TODO
            # Double-check the invocation of Zombie._get_life decay amy when calling life_decay from AbsAgent

    def life_decay(self):
        """
        Decay Zombie's energy over time.
        :return: None.
        """
       # self.m_energy -= self._get__life__decay__amount()
      #  super().check_death()

    def bite(self):
        l_neigh = super()._select_neighbors()
        for neigh in l_neigh:
            if not isinstance(neigh, Human):
                continue
            if neigh.get_state() != ALIVE:
                continue
            bite_odd = np.random.binomial(n=1, p=BITE_PROB)
            if bite_success == 0:
                continue
            neigh.change_state(INFECTED)
            neigh.life_decay()
            self.life_increases()
            break


#############################
# GAME FUNCTION
#############################
if __name__ == '__main__':
        game_ins = ZombieGameSim()
        game_ins.start()
