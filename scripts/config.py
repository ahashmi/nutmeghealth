from pathlib import Path
import us

PROJ_PATH = Path(__file__).parents[1]

paths = {
  "data": PROJ_PATH / "DATA",
  "logs": PROJ_PATH / "logs",
  "refs": PROJ_PATH / "references",
}

states_abbrs =  us.states.mapping("name", "abbr")
# corrections
states_abbrs.pop("District of Columbia")
states_abbrs["Dist. Of Col."] = "DC"
states_abbrs.pop("Northern Mariana Islands")
states_abbrs["N. Mariana Islands"] = "MP"
states_abbrs.pop("American Samoa")
states_abbrs["Amer. Samoa"] = "AS"