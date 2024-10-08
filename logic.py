"""
This file contains classes and functions for simulating a pandemic using Pygame.

Classes:
- Person: Represents an individual in the simulation.

Functions:
- community(num_persons): Creates a community of people based on a graph.
- calculate_distance(p1, p2): Calculates the Euclidean distance between two points.
- draw_edge_and_infect(vertex1, vertex2, threshold, infection_probability, recovery_time, screen):
    Draws an edge between two people and infects them based on proximity and infection probability.
- simulate_one_time_step(G, infection_radius, infection_probability, recovery_time, screen):
    Simulates one time step of epidemic spread.
- track_infections_over_time(people, num_iterations, infection_radius, infection_probability, recovery_time, screen):
    Tracks the number of infected individuals over the course of the simulation.

Dependencies:
- pygame: Library for creating video games and multimedia applications.
- numpy: Library for numerical computations.

Note: This file relies on the 'graph_model' module for graph-related functionality.
"""
import pygame
import numpy as np
import python_ta
import graph_model
import getting_data


class Person:
    """
    person class that represents a person in a pandemic

    Instance attributes:
    - x: int, the x position of the person
    - y: int, the y position of the person
    - speed_x: float, how fast the person moves in the x direction
    - speed_y: float, how fast the person moves in the y direction
    - infected: bool, if person is infected
    - recovered: bool, if the person recovered from infection
    - infection_probability: float, the indvidual chance for a person to be infected
    - infected_timer: int, the amount of time the person is infected for

    Representation Invariants:
    None
    """
    x: int
    y: int
    speed_x: float
    speed_y: float
    infected: bool
    recovered: bool
    infection_probability: float
    infection_timer: int

    def __init__(self) -> None:
        self.x = np.random.randint(0, 800)
        self.y = np.random.randint(0, 600)
        self.speed_x = np.random.uniform(-1.5, 1.5)
        self.speed_y = np.random.uniform(-1.5, 1.5)
        self.infected = False
        self.recovered = False
        self.infection_probability = getting_data.global_infect * 10
        self.infection_timer = 0

    def move(self, width: int, height: int) -> None:
        """
        moves the vertex in a direction
        """
        self.x += self.speed_x
        self.y += self.speed_y

        # Bounce off edges
        if self.x <= 0 or self.x >= width:
            self.speed_x *= -1
        if self.y <= 0 or self.y >= height:
            self.speed_y *= -1

    # Modify the draw method of the Person class to change the color of infected particles
    def draw(self, screen: pygame.Surface) -> None:
        """
        draws the vertexes with its correspomding color in pyagame window
        """
        if self.infected:
            color = (255, 0, 0)  # red
        elif self.recovered:
            color = (0, 255, 0)  # Green
        else:
            color = (255, 255, 255)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), 3)


# Create people
def community(num_persons: int) -> graph_model.Graph():
    """
    creates a community of people based on a graph
    :param num_persons:
    :return: graph_model.Graph()
    """
    people = [Person() for _ in range(num_persons)]

    infected_particle = people[np.random.choice(len(people))]
    infected_particle.infected = True

    # Create graph to represent connections between people
    g = graph_model.Graph()

    # Add people as nodes to the graph
    for num in range(len(people)):
        g.add_node(num, people[num])

    # Add edges between people based on distance
    for i, person1 in enumerate(people):
        for person2 in people[i + 1:]:  # Only iterate over people that come after person1
            g.add_edge(person1, person2)

    return g


def calculate_distance(p1: Person, p2: Person) -> float:
    """
    calculates the distance between two vertexes
    :param p1:
    :param p2:
    :return:
    """
    return np.sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2)


def draw_edge_and_infect(vertex1: Person, vertex2: Person, model_params: tuple[int, int],
                         screen: pygame.Surface) -> None:
    """
    draws the edge between two people under a certain distance
    :param vertex1:
    :param vertex2:
    """
    threshold, recovery_time = model_params
    distance = calculate_distance(vertex1, vertex2)
    if distance < threshold:  # Adjust the threshold distance as needed
        pygame.draw.line(screen, (255, 255, 255), (int(vertex1.x), int(vertex1.y)),
                         (int(vertex2.x), int(vertex2.y)))
        # Check if one is infected and the other is not, then infect based on the infection probability
        infect = np.random.rand()
        if vertex1.infected and not vertex2.infected:
            if infect < vertex1.infection_probability:
                vertex2.infected = True
        elif vertex2.infected and not vertex1.infected:
            if infect < vertex2.infection_probability:
                vertex1.infected = True

        if vertex1.infected:
            vertex1.infection_timer += 1
            if vertex1.infection_timer >= recovery_time:
                vertex1.infected = False
                vertex1.recovered = True
                vertex1.infection_timer = 0

        if vertex2.infected:
            vertex2.infection_timer += 1
            if vertex2.infection_timer >= recovery_time:
                vertex2.infected = False
                vertex2.recovered = True
                vertex2.infection_timer = 0


if __name__ == "__main__":
    python_ta.check_all(config={
        'max-line-length': 170,
        'disable': ['E1136', 'W0221'],
        'extra-imports': ['random', 'graph_model', 'statistics', 'logic', 'pygame', 'numpy', 'getting_data'],
        'allowed-io': ['preventions', 'create_graph', 'preventions', 'pygame'],
    })
