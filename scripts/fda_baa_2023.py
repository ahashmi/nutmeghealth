from config import paths
from util import config_log
import pdfplumber
import logging

LOGGER_NM = 'fda_baa_2023'
USE_CONTENTS = False


def get_contents(doc, page_no, debug:bool=True) -> dict:
  logger = logging.getLogger(LOGGER_NM)
  logger.debug(f'[get_content] retrieving contents from page: {page_no}')
  contents_page = doc.pages[page_no - 1]
  contents = {}
  c = 0
  for contents_entry in contents_page.extract_text().split('\n'):
    if contents_entry.find('...') != -1:
      contents_line = contents_entry.replace('.', '')
      if not c:
        section, section_page = contents_line.split()
        section_name = section.capitalize()
      else:
        section = contents_line.split(':')[0]
        contents_line = contents_line.replace(f'{section}: ', '')
        contents_elems = contents_line.split()
        section_page = contents_elems.pop(-1)
        section_name = ' '.join(contents_elems)
      if debug:
        print(f'{c}: {section} - {section_name} - {section_page}')
      contents[section] = {
        'name': section_name,
        'page': section_page,
      }
      c += 1
  logger.info(f'[get_contents] contents entries loaded: {len(contents)}')
  return contents

def extract_section(section_pages:list) -> dict:
  logger = logging.getLogger(LOGGER_NM)
  pages = {}
  tot_lines = 0
  for page in section_pages:
    page_lines = page.extract_text().split('\n')
    pages[page.page_number] = page_lines
    logger.info(f'[extract_section] page: {page.page_number}, lines: {len(page_lines)}')
    tot_lines += len(page_lines)
  logger.debug(f'[extract_pages] total pages: {len(section_pages)}, total lines: {tot_lines}')
  return pages

def export(text_by_page:dict, outfile) -> None:
  logger = logging.getLogger(LOGGER_NM)
  with open(outfile, 'w') as txt_out:
    for pg, lines in text_by_page.items():
      txt_out.write('\n'.join(lines))
      txt_out.write('')
  logger.info(f'[export] text written to: {outfile.name}')
  
def main(src_doc:str, contents_page_no:int, selected_sections:dict) -> None:
  logger = logging.getLogger(LOGGER_NM)
  path_to_pdf=paths['refs'] / (src_doc + '.pdf')
  path_to_txt=paths['refs'] / (src_doc + '.txt')
  logger.info(f'[main] opening {path_to_pdf.name}...')
  with pdfplumber.open(path_to_pdf) as pdf:
    doc_contents = get_contents(doc=pdf, page_no=contents_page_no)
    for section_id, section_info in selected_sections.items():
      if USE_CONTENTS:
        crnt_section = list(doc_contents.keys())[section_id]
        start = int(doc_contents[crnt_section]['page']) - 1
        next_section = list(doc_contents.keys())[section_id + 1]
        stop = int(doc_contents[next_section]['page']) - 2
      else:
        logger.warning(f'[main] disregarding document contents')
        crnt_section = section_info['name']
        start = section_info['start']
        stop = section_info['stop']
      logger.info(f'[main] current section: {crnt_section}, pages: {start}-{stop}')
      section_text = extract_section(pdf.pages[(start-1):stop])
      export(text_by_page=section_text, outfile=path_to_txt)
  
  
if __name__ == '__main__':
  config_log(logger_nm=LOGGER_NM)
  doc_info = {
    'src_doc': 'FY23+FDA+BAA-23-00123',
    'contents_page_no': 3,
    'selected_sections': {
        1: {
          'name': 'Background',
          'start': 4,
          'stop': 36,
        }
      },
  }
  main(**doc_info)