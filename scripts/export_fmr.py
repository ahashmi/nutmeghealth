from config import paths
from util import config_log
from logging import getLogger
import pandas as pd



DATA_YEARS = [str(y) for y in range(2015,2022)]
FMR_DIR = paths["data"] / "fmr"


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
    self.sheets = pd.read_excel(self.xl, sheet_name=None)
    for sheet_nm, df in self.sheets.items():
      print(sheet_nm)


def main(
  logger_nm:str
) -> None:
  logger = getLogger(logger_nm)
  logger.debug(f"[extract_fmr] data years -> from: {min(DATA_YEARS)} to: {max(DATA_YEARS)}")
  all_xlsx = [x for x in FMR_DIR.glob("*.xlsx") if x.name.find("~") == -1]
  fmr_xlsx = {
    "MDCD": {},
    "CHIP": {}, 
  }
  for xlsx in all_xlsx:
    for dyear in DATA_YEARS:
      if xlsx.name.find(dyear) > -1:
        if xlsx.name.find("CHIP") > -1:
          fmr_xlsx["CHIP"][dyear] = xlsx
        else:
          fmr_xlsx["MDCD"][dyear] = xlsx
  for fmr_type, fmr_list in fmr_xlsx.items():
    logger.info(f"[extract_fmr] {fmr_type} files found: {len(fmr_list)}")
    for dyear, xlsx_file in fmr_list.items():
      if dyear == '2019':
        crnt_fmr = FMR(
          year=dyear,
          fmr_type=fmr_type,
          xlsx_file=xlsx_file,
          logger_nm=logger_nm,
        )
        crnt_fmr.parse_sheets()
    print()
  
  

if __name__ == "__main__":
  config_log(
    logger_nm="export_fmr"
  )
  main(
    logger_nm="export_fmr"
  )