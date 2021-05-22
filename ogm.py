import asyncio
import gremlin_python
from goblin import Goblin

loop = asyncio.get_event_loop()

app = loop.run_until_complete(Goblin.open(loop))
app.config_from_file('config.yml')
