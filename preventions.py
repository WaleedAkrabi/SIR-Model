"""
Module for defining prevention measures for controlling disease spread.

This module contains functions for implementing preventive measures such as vaccines, lockdowns, social distancing,
mask wearing, infection tracing, staggered work hours, and remote work.

Functions:
    vaccine_prevention: Apply vaccine prevention by reducing the infection probability for vaccinated individuals.
    lockdown: Apply lockdown by reducing the movement speed of individuals.
    social_distance: Implement social distancing by increasing the distance between individuals.
    mask_wearing: Implement mask wearing by reducing the infection probability for individuals wearing masks.
    infection_tracing: Implement infection tracing to identify and isolate individuals who have been in contact with infected individuals.
    staggered_work_hours: Implement staggered work hours to reduce the number of people present in a shared space at any given time.
    remote_work: Encourage remote work to minimize physical interactions in workplaces.
"""
import random

import numpy as np
import python_ta
import graph_model


def vaccine_prevention(people: graph_model.Graph(), people_with_vaccines: float) -> None:
    """
    Apply vaccine prevention by reducing the infection probability for vaccinated individuals.
    :param people: List of Person objects.
    :param people_with_vaccines: Effectiveness of the vaccine (0 to 1).
    """
    # Calculate the number of vaccinated people
    num_vaccinated = int(people_with_vaccines * len(people))

    # Shuffle the keys of the dictionary
    keys = list(people.nodes.keys())
    random.shuffle(keys)

    # Select the first num_vaccinated keys
    vaccinated_people = keys[:num_vaccinated]

    # Update infection probability for vaccinated individuals
    for person_key in vaccinated_people:
        person = people.nodes[person_key]
        # Reduce the person's infection probability based on vaccine effectiveness
        person.infection_probability *= 0.3  # Assuming 30% reduction in infection probability


def lockdown(people: graph_model.Graph(), lockdown_factor: float) -> None:
    """
    Apply lockdown by reducing the movement speed of individuals.
    :param people: List of Person objects.
    :param lockdown_factor: Factor to reduce movement speed (0 to 1).
    """
    for person in people.nodes.values():
        person.speed_x *= abs(lockdown_factor - 1)  # Reduce movement speed
        person.speed_y *= abs(lockdown_factor - 1)


def social_distance(people: graph_model.Graph(), distance_threshold: float, s_width: int, s_height: int) -> None:
    """
    Implement social distancing by increasing the distance between individuals.
    :param people: List of Person objects.
    :param distance_threshold: Minimum distance to maintain between individuals.
    """
    for person1, person2 in people.edges:
        distance = np.sqrt((person2.x - person1.x) ** 2 + (person2.y - person1.y) ** 2)
        if distance < distance_threshold:
            # Adjust positions to increase distance
            angle = np.arctan2(person2.y - person1.y, person2.x - person1.x)
            move_x = (distance_threshold - distance) * np.cos(angle) / 2
            move_y = (distance_threshold - distance) * np.sin(angle) / 2

            # Update positions ensuring they don't go beyond screen boundaries
            if 0 <= person1.x - move_x <= s_width and 0 <= person2.x + move_x <= s_width:
                person1.x -= move_x
                person2.x += move_x
            if 0 <= person1.y - move_y <= s_height and 0 <= person2.y + move_y <= s_height:
                person1.y -= move_y
                person2.y += move_y


def mask_wearing(people: graph_model.Graph(), people_with_masks: float) -> None:
    """
    Implement mask wearing by reducing the infection probability for individuals wearing masks.
    :param people: List of Person objects.
    :param people_with_masks: Effectiveness of masks (0 to 1).
    """
    # Calculate the number of vaccinated people
    num_vaccinated = int(people_with_masks * len(people.nodes))

    # Shuffle the keys of the dictionary
    keys = list(people.nodes.values())
    random.shuffle(keys)

    # Select the first num_vaccinated keys
    vaccinated_people = keys[:num_vaccinated]

    # Update infection probability for vaccinated individuals
    for person in vaccinated_people:
        person.infection_probability *= 0.4  # Assuming 40% reduction in infection probability from canada.gov


def infection_tracing(people: graph_model.Graph(), infected_threshold: float) -> None:
    """
    contact tracing to identify and isolate individuals who have been in contact with infected individuals.
    :param people: List of Person objects.
    :param infected_threshold: Threshold for identifying infected individuals (0 to 1).
    """
    for person in people:
        if person.infected and random.random() < infected_threshold:
            # Transport infected person to the bottom corner of the map
            person.x = np.random.randint(0, 100)
            person.y = np.random.randint(0, 100)
            person.move(100, 100)  # Set y-coordinate to the bottom edge of the screen


def staggered_work_hours(people: graph_model.Graph(), staggered_factor: float) -> None:
    """
    Implement staggered work hours to reduce the number of people present in a shared space at any given time.
    :param people: List of Person objects.
    :param staggered_factor: Factor to adjust work hours (0 to 1).
    """
    people_list = list(people.nodes.values())

    # Adjust work hours for individuals to stagger their arrival and departure times
    total_people = len(people_list)
    num_staggered_people = int(total_people * staggered_factor)
    staggered_people = random.sample(people_list, num_staggered_people)

    for person in staggered_people:
        # Reduce the movement speed only for the staggered individuals
        person.speed_x *= 0.5  # Example: Reduce movement speed by half
        person.speed_y *= 0.5  # Example: Reduce movement speed by half


def remote_work(people: graph_model.Graph(), remote_work_factor: float) -> None:
    """
    Encourage remote work to minimize physical interactions in workplaces.
    :param people: List of Person objects.
    :param remote_work_factor: Factor to increase remote work (0 to 1).
    """
    # Transition individuals to remote work where feasible
    people_list = list(people.nodes.values())

    # Adjust remote work  for individuals to prevent them from moving much
    num_staggered_people = int(len(people_list) * remote_work_factor)
    staggered_people = random.sample(people_list, num_staggered_people)

    for person in staggered_people:
        person.speed_x *= abs(remote_work_factor - 1)  # Reduce movement speed
        person.speed_y *= abs(remote_work_factor - 1)


if __name__ == "__main__":
    python_ta.check_all(config={
        'max-line-length': 170,
        'disable': ['E1136', 'W0221'],
        'extra-imports': ['random', 'graph_model', 'statistics', 'logic', 'numpy'],
        'allowed-io': ['preventions', 'create_graph', 'preventions', 'pygame'],
    })
