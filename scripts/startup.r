# library("tidyverse")
library("readxl")

dev_root <- "C:/Users/AliHashmi/Desktop/Development"
project_nm <- "medicaid_analytics"

proj_path <- file.path(dev_root, project_nm)

setwd(proj_path)

data_path <- file.path(proj_path, 'DATA')
mbes_path <- file.path(data_path, 'mbes')

list.files(path=mbes_path)
