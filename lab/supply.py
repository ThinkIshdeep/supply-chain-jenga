import numpy as np
from scipy.optimize import linprog
from sklearn.ensemble import RandomForestRegressor
from .core import Base, bounded

class Engine(Base):
    actions = Base.actions | {'simulate', 'configure'}

    def __init__(self):
        super().__init__()
        self.reset({})

    def reset(self, p):
        self.state = {'shock_start': 20, 'shock_length': 20, 'backup_capacity': 12, 'policy': 'optimized', 'history': [], 'last_result': None, 'suppliers': [{'name': 'Pack Primary', 'capacity': 40, 'cost': 1.2}, {'name': 'Pack Backup', 'capacity': 12, 'cost': 2.5}, {'name': 'Raw A', 'capacity': 30, 'cost': 3.0}, {'name': 'Raw B', 'capacity': 25, 'cost': 4.0}]}
        self.simulate({})

    def configure(self, p):
        s = self.state
        for key, lo, hi in [('shock_start', 5, 50), ('shock_length', 0, 35), ('backup_capacity', 0, 40)]:
            if key in p:
                s[key] = bounded(p, key, s[key], lo, hi, True)
        if p.get('policy') in ['fixed', 'optimized']:
            s['policy'] = p['policy']
        return self.simulate({})

    def rollout(self, policy, seed):
        s = self.state
        r = np.random.default_rng(seed)
        demand = np.maximum(1, np.rint(r.normal([14, 9], [3, 2], size=(75, 2)))).astype(int)
        stock = np.array([60.0, 45.0, 100.0])
        pending = []
        backlog = np.zeros(2)
        history = []
        cost = 0.0
        fulfilled = 0.0
        total = 0.0
        minimum = 1000000000.0
        for day in range(75):
            self.check_cancel()
            for due, amount in pending[:]:
                if due <= day:
                    stock += amount
                    pending.remove((due, amount))
            shock = s['shock_start'] <= day < s['shock_start'] + s['shock_length']
            cap = 0 if shock else 40
            need = demand[day] + backlog
            produced = np.zeros(2)
            for product in np.argsort(need)[::-1]:
                made = min(need[product], stock[product], stock[2])
                stock[product] -= made
                stock[2] -= made
                produced[product] = made
            backlog = need - produced
            fulfilled += produced.sum()
            total += demand[day].sum()
            cost += float(0.05 * stock.sum() + 1.5 * backlog.sum())
            minimum = min(minimum, float(stock.min()))
            forecast = demand[max(0, day - 6):day + 1].mean(axis=0)
            pipeline = sum((amount for _, amount in pending), np.zeros(3))
            desired = np.maximum(0, np.r_[forecast * 4, forecast.sum() * 4] - stock - pipeline)
            if policy == 'fixed':
                pack = min(cap, desired[2])
                backup = min(s['backup_capacity'], max(0, desired[2] - pack)) if shock else 0.0
                a = min(30, desired[0])
                b = min(25, desired[1])
            else:
                solution = linprog([3 - 15, 4 - 15, 1.2 - 12, 2.5 - 12], A_ub=[[0, 0, 1, 1]], b_ub=[desired[2]], bounds=[(0, min(30, desired[0])), (0, min(25, desired[1])), (0, cap), (0, s['backup_capacity'])], method='highs')
                a, b, pack, backup = solution.x if solution.success else (0, 0, 0, 0)
            shipment = np.array([a, b, pack + backup])
            pending.append((day + 2, shipment))
            cost += 3 * a + 4 * b + 1.2 * pack + 2.5 * backup
            history.append({'day': day, 'demand': float(demand[day].sum()), 'fulfilled': float(produced.sum()), 'backlog': float(backlog.sum()), 'pack_stock': float(stock[2]), 'raw_a': float(stock[0]), 'raw_b': float(stock[1]), 'shock': shock, 'cumulative_cost': cost})
        return {'history': history, 'fill_rate': float(fulfilled / total), 'backlog': float(backlog.sum()), 'cost': cost, 'stockout_days': sum((h['backlog'] > 0 for h in history)), 'minimum_inventory': minimum, 'total_demand': int(total)}

    def simulate(self, p):
        result = self.rollout(self.state['policy'], int(p.get('seed', 42)))
        self.state['history'] = result['history']
        self.state['current'] = {k: v for k, v in result.items() if k != 'history'}
        return self.state['current']

    def evaluate(self, p):
        rows = []
        for policy in ['fixed', 'optimized']:
            result = [self.rollout(policy, i) for i in [881, 882, 883, 884]]
            rows.append({'policy': policy, 'fill_rate': float(np.mean([x['fill_rate'] for x in result])), 'cost': float(np.mean([x['cost'] for x in result])), 'stockout_days': float(np.mean([x['stockout_days'] for x in result])), 'nonnegative_inventory': all((x['minimum_inventory'] >= 0 for x in result))})
        out = {'metrics': rows, 'seeds': [881, 882, 883, 884], 'note': 'Synthetic two-product inventory model; both policies see identical realized demand, never future demand. Costs are declared model units.'}
        self.state['last_result'] = out
        return out
