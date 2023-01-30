from config import paths, states_abbrs
from util import config_log
from logging import getLogger
import pandas as pd

TEST_STATES = ['VT', 'NH', 'ME', 'MA', 'CT', 'RI']
DATA_YEARS = [str(y) for y in range(2015,2022)]
FMR_DIR = paths['data'] / 'fmr'
SHEET_NAME_SEP = ' - '

fmr_sheet = {
  'header': 6
}

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
      **fmr_sheet,
    )
    self.logger.
    
  def extract_totals(self) -> dict:
    self.fmr_data = {st:{} for st in states_abbrs.values()}
    for sheet_nm, df in self.sheets.items():
      data_type, state_nm = sheet_nm.split(SHEET_NAME_SEP)
      state = states_abbrs[state_nm]
      fixed_cols = [col.replace("\n ", "") for col in df.columns]
      df.columns = fixed_cols
      created_indx = df.shape[0] - 1
      created_row = df.loc[created_indx, :]
      df = df.drop(created_indx)
      df = df.dropna(axis=0, how='all').reset_index(drop=True)
      meta = created_row.to_list()[0]
      total_category = [
        svc for svc in df['Service Category'].to_list() if svc.find('Total') > -1
        ][0]
      totals = df[df['Service Category'] == total_category].to_dict(orient='records')[0]
      totals.pop('Service Category')
      self.fmr_data[state][data_type] = {
          'meta': meta,
          'total_category': total_category,
          'totals': totals,
          # 'dataframe': df,
      } 
    return self.fmr_data

def main(
  logger_nm:str
) -> None:
  logger = getLogger(logger_nm)
  logger.debug(f"[extract_fmr] data years -> from: {min(DATA_YEARS)} to: {max(DATA_YEARS)}")
  all_xlsx = [x for x in FMR_DIR.glob('*.xlsx') if x.name.find('~') == -1]
  fmr_xlsx = {
    'MDCD': {},
    'CHIP': {}, 
  }
  for xlsx in all_xlsx:
    for dyear in DATA_YEARS:
      if xlsx.name.find(dyear) > -1:
        if xlsx.name.find('CHIP') > -1:
          fmr_xlsx['CHIP'][dyear] = xlsx
        else:
          fmr_xlsx['MDCD'][dyear] = xlsx
  all_states = {st_abbr:{} for st_abbr in TEST_STATES}
  for fmr_type, fmr_list in fmr_xlsx.items():
    logger.info(f'[extract_fmr] {fmr_type} files found: {len(fmr_list)}')
    for dyear, xlsx_file in fmr_list.items():
      if dyear == '2019':
        crnt_fmr = FMR(
          year=dyear,
          fmr_type=fmr_type,
          xlsx_file=xlsx_file,
          logger_nm=logger_nm,
        )
        crnt_fmr_states = crnt_fmr.parse_sheets()
        # print(all_states.keys())
        for st_abbr, st_data in crnt_fmr_states.items():
          if st_abbr in all_states:
            all_states[st_abbr][dyear] = st_data
            
    print(all_states)
  
  

if __name__ == '__main__':
  config_log(
    logger_nm='export_fmr'
  )
  main(
    logger_nm='export_fmr'
  )