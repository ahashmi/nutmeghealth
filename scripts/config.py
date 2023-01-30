from pathlib import Path
import us

PROJ_PATH = Path(__file__).parents[1]

paths = {
  'data': PROJ_PATH / 'DATA',
  'logs': PROJ_PATH / 'logs',
  'refs': PROJ_PATH / 'references',
  'site': PROJ_PATH / 'docs',
  'site_data': PROJ_PATH / 'docs' / '_data',
}

states_abbrs =  us.states.mapping('name', 'abbr')
states_abbrs['National Totals'] = 'USA'
# corrections
states_abbrs.pop('District of Columbia')
states_abbrs['Dist. Of Col.'] = 'DC'
states_abbrs.pop('Northern Mariana Islands')
states_abbrs['N. Mariana Islands'] = 'MP'
states_abbrs.pop('American Samoa')
states_abbrs['Amer. Samoa'] = 'AS'