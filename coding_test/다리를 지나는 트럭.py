from __future__ import annotations  
from dataclasses import dataclass
from collections import deque

# ==========================================
# 1. Domain Models (도메인 영역)
# ==========================================

@dataclass
class Truck:
    """트럭 도메인: 트럭의 고유 속성을 가집니다."""
    weight: int

class MovingTruck:
    """다리 위를 건너고 있는 트럭의 상태를 관리합니다."""
    def __init__(self, truck: Truck, remaining_time: int):
        self.truck = truck
        self.remaining_time = remaining_time

    def move(self):
        """1초 동안 다리를 이동합니다."""
        self.remaining_time -= 1

    def has_crossed(self) -> bool:
        """다리를 완전히 건넜는지 확인합니다."""
        return self.remaining_time <= 0


class Bridge:
    """다리 도메인: 다리의 상태를 관리하고 트럭의 진입/진출을 통제합니다."""
    def __init__(self, length: int, weight_limit: int):
        self.length = length
        self.weight_limit = weight_limit
        self.current_weight = 0
        self.on_bridge = deque() # type: deque[MovingTruck]

    def can_enter(self, truck: Truck) -> bool:
        """해당 트럭이 다리에 진입할 수 있는지 하중을 검증합니다."""
        return self.current_weight + truck.weight <= self.weight_limit

    def enter(self, truck: Truck):
        """트럭이 다리에 진입합니다."""
        self.on_bridge.append(MovingTruck(truck, self.length))
        self.current_weight += truck.weight

    def tick(self):
        """1초의 시간이 흘렀을 때 다리 위의 상태를 업데이트합니다."""
        # 1. 다리 위 트럭들 1초씩 이동
        for moving_truck in self.on_bridge:
            moving_truck.move()
        
        # 2. 다리를 완전히 건넌 트럭들 진출 처리
        while self.on_bridge and self.on_bridge[0].has_crossed():
            exited_truck = self.on_bridge.popleft()
            # 캡슐화: 다리가 스스로 현재 하중을 차감하여 O(1)로 상태를 유지합니다.
            self.current_weight -= exited_truck.truck.weight
            
    def is_empty(self) -> bool:
        return len(self.on_bridge) == 0


# ==========================================
# 2. Application Service (서비스 영역)
# ==========================================

class BridgeSimulation:
    """전체 시나리오의 흐름을 제어하는 오케스트레이터입니다."""
    def __init__(self, bridge: Bridge, trucks: list[Truck]):
        self.bridge = bridge
        self.waiting_trucks = deque(trucks)
        self.elapsed_time = 0

    def run(self) -> int:
        """모든 트럭이 다리를 건널 때까지 시뮬레이션을 실행합니다."""
        while self.waiting_trucks or not self.bridge.is_empty():
            self.elapsed_time += 1
            
            # 1. 시간 경과에 따른 다리 상태 업데이트 (트럭 이동 및 도착)
            self.bridge.tick()
            
            # 2. 대기 중인 트럭이 있다면 다리 진입 시도
            if self.waiting_trucks:
                next_truck = self.waiting_trucks[0]
                if self.bridge.can_enter(next_truck):
                    self.bridge.enter(self.waiting_trucks.popleft())
                    
        return self.elapsed_time


# ==========================================
# 3. Entry Point (실행부)
# ==========================================

def solution(bridge_length, weight, truck_weights):
    # 의존성 주입(DI)처럼 각 객체를 생성하고 조립합니다.
    bridge = Bridge(length=bridge_length, weight_limit=weight)
    trucks = [Truck(w) for w in truck_weights]
    
    simulation = BridgeSimulation(bridge, trucks)
    return simulation.run()