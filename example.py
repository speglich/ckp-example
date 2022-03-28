from devito import TimeFunction, Grid, Eq, Operator
from devito import DevitoCheckpoint, CheckpointOperator

from pyrevolve import Revolver

def Forward(grid):

    u = TimeFunction(name="u", grid=grid)
    eq = Eq(u, u+1)

    return Operator([eq])

def Reverse(grid):

    u = TimeFunction(name="u", grid=grid)
    v = TimeFunction(name="v", grid=grid)
    eq = Eq(v, -1*u + 1)

    return Operator([eq])

if __name__ == "__main__":

    nt = 10
    nx = 5
    ny = 5
    nz = 5

    grid = Grid(shape=(nx, ny, nz))

    u = TimeFunction(name="u", grid=grid)
    v = TimeFunction(name="v", grid=grid)

    fwd = CheckpointOperator(Forward(grid=grid), u=u)
    rev = CheckpointOperator(Reverse(grid=grid), u=u, v=v)
    cp = DevitoCheckpoint([u])

    revolver = Revolver(cp, fwd, rev, n_checkpoints=None, n_timesteps=nt)

    revolver.apply_forward()
    revolver.apply_reverse()
