# `pyrl`

In this repo I followed along the excellent Python TCOD Roguelike Tutorial: http://rogueliketutorials.com/tutorials/tcod/.
There is one major trick: I used an [ECS](https://en.wikipedia.org/wiki/Entity_component_system) framework
([`esper`](https://github.com/benmoran56/esper), specifically). I made several monkey-patches to Esper (refer to
[`pyrl/esper_ext.py`](pyrl/esper_ext.py)). The implementation (especially data model) differs to varying degrees
from the tutorial, both to more clearly express stuff within the ECS system, and to satisfy my sense of elegance.
Also, the code is fully typed (with the exception of some pieces of black magic), and heavily utilizes Python 3
features like dataclasses.

There is much room for improvement, but for now I consider this project finished. I publish it with the hopes that
it might be useful to someone furiously searching Google for "python tcod roguelike ECS example".