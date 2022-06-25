import pdc
from pdc import Object, region
import numpy as np
import mpi4py
import asyncio

async def main():
    rank = mpi4py.MPI.COMM_WORLD.Get_rank()

    pdc.init()
    cont = pdc.Container()

    #create np data array of 128 doubles
    data = np.full(128, 1.0, dtype=np.float64)

    #create object property
    prop = Object.Properties(dims=128, type=pdc.Type.DOUBLE)

    #create object
    obj1 = Object(f'o1_{rank}', prop, cont)

    #set all data to data
    await obj1.set_data(data)

    data = np.full(128, 2.0, dtype=np.float64)
    obj2 = Object(f'o2_{rank}', prop, cont)
    await obj2.set_data(data)

    #test object values
    for val in await obj1.get_data():
        assert val == 1.0
    for val in await obj2.get_data():
        assert val == 2.0

asyncio.run(main())