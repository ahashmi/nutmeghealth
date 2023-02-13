from config import paths, states_abbrs, DATA_YEARS
from util import config_log
from logging import getLogger
import pandas as pd
import json
from copy import deepcopy

TEST_STATES = ['VT', 'NH', 'ME', 'MA', 'CT', 'RI']
FMR_PLOTS = ['MAP', 'ADM', 'CHIP']
FMR_TYPES = FMR_PLOTS + ['MCHIP', 'MCHIP 20%']
FMR_DIR = paths['data'] / 'fmr'
SHEET_NAME_SEP = ' - '

fmr_sheet_kwargs = {
  'header': 6
}

fmr_layout_str = """
var layout = {
    title: 'State FMR Total Computable Amounts',
    height: 640,
    yaxis: {
        title: 'MAP',
		side: 'left'
    },
    yaxis2: {
        title: 'ADM & CHIP',
        overlaying: 'y',
        side: 'right'
    }
};
"""

class FMR:
  
  def __init__(
    self,
    year: str,
    fmr_type: str,
    xlsx_file,
    logger_nm: str
  ) -> None:
    self.year = year
    self.type = fmr_type
    self.xlsx = xlsx_file
    self.logger = getLogger(logger_nm)
    self.xl = pd.ExcelFile(self.xlsx)
    self.logger.debug(f"[FMR] {self.year} {self.type} file initialized")
    
  def parse_sheets(self) -> None:
    self.sheets = pd.read_excel(
      self.xl, 
      sheet_name=None,
      **fmr_sheet_kwargs,
    )
    self.logger.debug(f"[parse_sheets] loaded sheets: {len(self.sheets)}")
    
  def extract_amounts(self) -> dict:
    self.fmr_data = {st:{} for st in states_abbrs.values()}
    data_types = set()
    for sheet_nm, df in self.sheets.items():
      data_type, state_nm = sheet_nm.split(SHEET_NAME_SEP)
      data_types.add(data_type)
      state = states_abbrs[state_nm]
      fixed_cols = [col.replace("\n ", "") for col in df.columns]
      df.columns = fixed_cols
      created_indx = df.shape[0] - 1
      created_row = df.loc[created_indx, :]
      df = df.drop(created_indx)
      df = df.dropna(axis=0, how='all').reset_index(drop=True)
      meta = created_row.to_list()[0]
      total_svc_cat = [
          svc for svc in df['Service Category'].to_list() if svc.find('Total') > -1
          ][0]
      service_amounts = df[df['Service Category'] == total_svc_cat].to_dict(orient='records')[0]
      service_amounts.pop('Service Category')
      self.fmr_data[state][data_type] = {
          'meta': meta,
          'service_category': total_svc_cat,
          'amounts': service_amounts,
          # 'dataframe': df,
      }
    self.logger.info(f"[extract_amounts] data types: {data_types}")
    return self.fmr_data

def collect_fmr_files() -> dict:
  fmr_datafiles = {
    'MDCD': {},
    'CHIP': {}, 
  }
  all_xlsx = [x for x in FMR_DIR.glob('*.xlsx') if x.name.find('~') == -1]
  for xlsx in all_xlsx:
    for dyear in DATA_YEARS:
      if xlsx.name.find(dyear) > -1:
        if xlsx.name.find('CHIP') > -1:
          fmr_datafiles['CHIP'][dyear] = xlsx
        else:
          fmr_datafiles['MDCD'][dyear] = xlsx
  return fmr_datafiles

def extract_fmr_data(
  data_files: dict,
  state_abbrs: list,
  logger_nm: str,
  ) -> dict:
  func_logger = getLogger(logger_nm)
  fmr_group = {dtype:{} for dtype in FMR_TYPES}
  state_group = {st:deepcopy(fmr_group) for st in state_abbrs}
  for fmr_type, fmr_list in data_files.items():
    func_logger.info(f'[extract_fmr] {fmr_type} files found: {len(fmr_list)}')
    for dyear, xlsx_file in fmr_list.items():
      crnt_fmr = FMR(
        year=dyear,
        fmr_type=fmr_type,
        xlsx_file=xlsx_file,
        logger_nm=logger_nm,
      )
      crnt_fmr.parse_sheets()
      crnt_fmr_state_totals = crnt_fmr.extract_amounts()
      for st_abbr, st_fmr_types in crnt_fmr_state_totals.items():
        if st_abbr in state_group:
          for dtype, fmr_data in st_fmr_types.items():
            state_group[st_abbr][dtype].update({
              dyear: fmr_data
            })
  func_logger.info(f"[extract_fmr_data] states updated: {len(state_group)}")
  return state_group

def publish_state_totals(state_data: dict, logger_nm: str) -> None:
  func_logger = getLogger(logger_nm)
  publ_dir = paths['site_data'] / "fmr"
  for st_abbr, years_data in state_data.items():
    data_file = publ_dir / f"{st_abbr}_totals.json"
    with open(data_file, 'w') as js_out:
      json.dump(years_data, js_out, indent=4)
  func_logger.info(
    f"[publish_state_data] output files written ({len(state_data)}): {list(state_data.keys())}"
    )
  
def publish_graph_data(state_data: dict, logger_nm: str) -> None:
  func_logger = getLogger(logger_nm)
  publ_dir = paths['site'] / "_analyses"
  plots_str = ', '.join(FMR_PLOTS)
  for st_abbr, fmr_data in state_data.items():
    out_lines = []
    graph_file = publ_dir / f"{st_abbr}_graphs.js"
    for fmr_type, fmr_years in fmr_data.items():
      if fmr_type in FMR_PLOTS:
          out_lines.append(f"var {fmr_type} = " + '{')
          out_lines.append(f"\tx: {DATA_YEARS},")
          amts = []
          for yr_data in fmr_years.values():
            amt = yr_data['amounts']['Total Computable']
            amts.append(round(amt))
          out_lines.append(f"\ty: {amts},")
          if fmr_type != 'MAP':
            out_lines.append(f"\tyaxis: 'y2',")
          out_lines.append(f"\tname: '{fmr_type}',")
          out_lines.append(f"\ttype: 'scatter'")
          out_lines.append("};\n")
    out_lines.append(f"var data = [{plots_str}];")
    out_lines.append(fmr_layout_str)
    out_lines.append("Plotly.newPlot('fmr_plot', data, layout);")
    with open(graph_file, 'w') as graph_out:
      graph_out.write('\n'.join(out_lines))
  func_logger.info(
    f"[publish_graph_data] graph files written -> types: {FMR_PLOTS}, states: {len(state_data)}"
    )

def main(
  logger_nm: str,
  state_list: list = None,   # list of state abbreviations
) -> None:
  """_summary_

  Args:
      state_list (list): _description_
  """
  main_logger = getLogger(logger_nm)
  if state_list is None:
    state_list = list(states_abbrs.values())
    main_logger.debug(f"[Export_FMR main] defaulting to all states")
  main_logger.debug(f"[extract_fmr] data years -> from: {min(DATA_YEARS)} to: {max(DATA_YEARS)}")
  fmr_xlsx = collect_fmr_files()
  all_states = extract_fmr_data(
    data_files=fmr_xlsx,
    state_abbrs=state_list,
    logger_nm=logger_nm,
  ) 
  publish_state_totals(
    state_data=all_states,
    logger_nm=logger_nm
  )
  publish_graph_data(
    state_data=all_states,
    logger_nm=logger_nm
  )
  

if __name__ == '__main__':
  config_log(
    logger_nm='export_fmr'
  )
  main(
    # state_list=TEST_STATES,
    logger_nm='export_fmr',
  )