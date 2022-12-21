from pathlib import Path

PROJ_PATH = Path(__file__).parents[1]

paths = {
  'data': PROJ_PATH / 'DATA',
  'logs': PROJ_PATH / 'logs',
  'refs': PROJ_PATH / 'references',
}
