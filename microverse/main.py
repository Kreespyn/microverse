#!/usr/bin/env python3

import math
from random import randint as rnd
import simulator as sim


WIDTH = 800
HEIGHT = 600
RENDERER = sim.Renderer(WIDTH, HEIGHT, title='Microverse')

SMART_AGENTS_SIZE = 10
FOODS_SIZE = 10

SMART_AGENTS = set()
FOODS = set()


def food_spawner():
    if len(FOODS) < FOODS_SIZE:
        FOODS.add(sim.Food(
            position=random_world_position(),
            velocity=sim.vec2(rnd(1, 2), rnd(-1, 2)).scale_to(3),
            size=15, fill=sim.color(102, 217, 239)
        ))


def smart_agent_spawner():
    if len(SMART_AGENTS) < SMART_AGENTS_SIZE:
        new_agent = sim.SmartAgent(
            environment=FOODS, ray_count=9,
            strength=1000, fov=math.pi / 2, nn=[5]
        )
        new_agent.position = random_world_position()
        new_agent.velocity = sim.vec2(rnd(1, 2), rnd(-1, 2)).scale_to(3)
        new_agent.size = 20
        new_agent.color = sim.color(229, 38, 154)

        if len(SMART_AGENTS) >= 2:
            left_parent, right_parent = select_parents(SMART_AGENTS)
            new_agent.brain = left_parent.brain.crossover(
                right_parent.brain, 0.05
            )
            new_agent.parents = [left_parent, right_parent]

        SMART_AGENTS.add(new_agent)


def random_world_position():
    return sim.vec2(
        rnd(-WIDTH / 2, WIDTH / 2),
        rnd(-HEIGHT / 2, HEIGHT / 2)
    )


def select_parents(population):
    return sorted(list(population),
                  key=lambda agent: -agent.fitness())[:2]


def recycle(items):
    for dead_item in [item for item in items if item.is_dead()]:
        items.remove(dead_item)


def focus_best():
    best_agent = max(SMART_AGENTS, key=lambda a: a.fitness())
    for agent in SMART_AGENTS:
        agent.focus = False
    best_agent.focus = True


while RENDERER.is_running:
    food_spawner()
    smart_agent_spawner()

    RENDERER.update()

    for agent in SMART_AGENTS:
        agent.update()
    for food in FOODS:
        food.update()

    for agent in SMART_AGENTS:
        agent.render(RENDERER)
    for food in FOODS:
        food.render(RENDERER)

    recycle(FOODS)
    recycle(SMART_AGENTS)
    focus_best()
