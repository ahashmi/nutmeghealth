from config import paths, states_abbrs
from util import config_log
from logging import getLogger
from us import TERRITORIES 
import json
import csv

abbrs_states = {abbr: nm for nm, abbr in states_abbrs.items() if abbr != 'USA'}
states_rename = {
  'District of Columbia': 'Dist. Of Col.'
}
terr_abbrs = [state.abbr for state in TERRITORIES]
EXP_STATUS = 'Adopted'


def load_expansion_data(logger_nm: str) -> dict:
  func_logger = getLogger(logger_nm)
  mdcd_expansion = {}
  mdcd_expansion_csv = paths['refs'] / 'medicaid_expansion.csv'
  with open(mdcd_expansion_csv, 'r') as csv_in:
    reader = csv.DictReader(csv_in)
    for row in reader:
      st_name = row.pop('STATE')
      if st_name in states_rename:
        st_name = states_rename[st_name]
      st_abbr = states_abbrs[st_name]
      mdcd_expansion[st_abbr] = row
      mdcd_expansion[st_abbr]['expanded'] = row['STATUS'] == EXP_STATUS
    func_logger.debug(f"[load_expansion_data] states loaded: {len(mdcd_expansion)}")
    return mdcd_expansion
  
def build_state_data(
  logger_nm: str,
  states_mdcd: dict,
) -> tuple:
  func_logger = getLogger(logger_nm)
  state_pages = {}
  state_maps = {}
  for st_abbr, st_name in abbrs_states.items():
    state_pages[st_abbr] = {
      'title': st_name,
    }
    state_maps[st_abbr] = {
      'name': st_name,
      'url': f"analyses/{st_abbr}",
    }
    if st_abbr in states_mdcd:
      if states_mdcd[st_abbr]['expanded']:
        exp_yr = states_mdcd[st_abbr]['EFFECTIVE'].split('-')[-1]
        state_pages[st_abbr]['expansion'] =  exp_yr
        state_maps[st_abbr]['description'] = f"Expansion: {exp_yr}"
      else:
        state_pages[st_abbr]['expansion'] = "No"
        state_maps[st_abbr]['description'] = 'Non-Expansion State'
    if st_abbr in terr_abbrs:
      state_pages[st_abbr]['territory'] = True
      state_maps[st_abbr]['hide'] = 'no'
  func_logger.info(f"[build_state_data] pages: {len(state_pages)}, maps: {len(state_maps)}")
  return state_pages, state_maps

def publish_state_pages(
  logger_nm: str,
  state_page_data: dict,  
) -> None:
  func_logger = getLogger(logger_nm)
  publ_dir = paths['site'] / "_analyses"
  for st_abbr, st_page in state_page_data.items():
    state_page = publ_dir / f"{st_abbr}.md"
    out_lines = [
      '---',
      "layout: state_page",
      f"title: {st_page['title']}",
      f"state_cd: {st_abbr}",
    ]
    if 'expansion' in st_page:
      out_lines.append(f"expansion: {st_page['expansion']}")
    if 'territory' in st_page or st_abbr == 'DC':
      out_lines.append(f"territory: true")
    out_lines.append('---')
    with open(state_page, 'w') as md_out:
      md_out.write('\n'.join(out_lines))
  func_logger.info(f"[publish_state_pages] pages written: {len(state_page_data)}")
  
def publish_map_data(
  logger_nm: str,
  state_map_data: dict,
) -> None:
  func_logger = getLogger(logger_nm)
  js_dir = paths['site'] / 'assets' / 'js'
  state_data_js = js_dir / 'statedata2.js'
  with open(state_data_js, 'w') as js_out:
    js_out.write('var stateData = ')
    js_out.write(json.dumps(state_map_data, indent=2))
    js_out.write(';')
    func_logger.debug(f"[publish_map_data] file written: {state_data_js.name}")
    
def main(
  logger_nm: str,
) -> None:
  mdcd_data = load_expansion_data(
    logger_nm=logger_nm,
  )
  pages_data, maps_data = build_state_data(
    logger_nm=logger_nm,
    states_mdcd=mdcd_data,
  )
  publish_state_pages(
    logger_nm=logger_nm,
    state_page_data=pages_data,
  )
  publish_map_data(
    logger_nm=logger_nm,
    state_map_data=maps_data,
  )
  
if __name__ == '__main__':
  script_nm = 'state_pages'
  config_log(script_nm)
  main(
    logger_nm=script_nm
  )
