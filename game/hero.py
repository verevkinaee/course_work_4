from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Type, Optional
from game.characters import Character
from game.equipment import Weapon, Armor
import random

base_stamina_per_round: float = 0.4


class Hero(ABC):
    def __init__(self, name: str, player_class: Type[Character], weapon=Weapon, armor=Armor):
        self.name = name
        self.player_class = player_class
        self._stamina = player_class.max_stamina
        self._hp = player_class.max_health
        self.weapon = weapon
        self.armor = armor
        self.used_skill: bool = False

    @property
    def hp(self):
        return round(self._hp, 1)

    @hp.setter
    def hp(self, value):
        self._hp = value

    @property
    def stamina(self):
        return round(self._stamina, 1)

    @stamina.setter
    def stamina(self, value):
        self._stamina = value

    @property
    def total_armor(self) -> float:
        if self.stamina - self.armor.stamina_per_turn >= 0:
            return self.armor.defence * self.player_class.armor
        return 0

    def _hit(self, target: Hero) -> Optional[float]:
        if self.stamina - self.weapon.stamina_per_hit < 0:
            return None
        hero_damage = self.weapon.damage * self.player_class.attack
        total_damage = hero_damage - target.total_armor
        if total_damage < 0:
            return 0
        self.stamina -= self.weapon.stamina_per_hit
        return round(total_damage, 1)

    def take_hit(self, damage: float):
        self.hp = round(self.hp, 1)
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def use_skill(self) -> Optional[float]:
        if self.stamina - self.player_class.skill.stamina and not self.used_skill:
            self.used_skill = True
            return round(self.player_class.skill.damage, 1)
        return None

    def regenerate_stamina(self):
        delta_stamina = base_stamina_per_round * self.player_class.stamina
        self.stamina = round(self.stamina, 1)
        if self.stamina + delta_stamina <= self.player_class.max_stamina:
            self.stamina += delta_stamina
        else:
            self.stamina = self.player_class.max_stamina

    @abstractmethod
    def hit(self, target: Hero) -> Optional[float]:
        pass


class Player(Hero):
    def hit(self, target: Hero) -> Optional[float]:
        return self._hit(target)


class Enemy(Hero):
    def hit(self, target: Hero) -> Optional[float]:
        if random.randint(0, 100) < 10 and self.stamina >= self.player_class.skill.stamina and not self.used_skill:
            self.use_skill()
        return self._hit(target)
