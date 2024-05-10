from bs4 import BeautifulSoup

def filter_parse(tables: list, grade: str, classes: list) -> dict:
  parsed = parse(tables)

  return parsed

def parse(tables: list) -> dict:
  data = {}

  first = BeautifulSoup(tables[0], 'html.parser').find('center')
  
  try: info = first.find('div', { 'class': 'mon_title' }).text.split(' ')
  except: return { 'error': 'unexpected structure of the dsb server response' }
  data['date'] = info[0]
  data['day'] = info[1]

  extra = first.find_all('tr', { 'class': 'info' })
  if len(extra) == 2:
    texts = extra[1].find_all('td')
    text = ''
    for text_snippet in texts: text += text_snippet.text

    data['extra'] = text

  column_names = []
  for column_name in first.find('tr', { 'class': 'list' }).findChildren('th'):
    column_names.append(column_name.text)

  table_data = {}
  current_class = ''
  for table in tables:
    table = BeautifulSoup(table, 'html.parser').find('table', { 'class': 'mon_list' }).findChildren('tr')
    table.pop(0)

    for row in table:
      children = row.findChildren('td')
      if len(children) == 1:
        current_class = children[0].text
        if current_class not in table_data: table_data[current_class] = []
      else:
        row_data = {}
        for column_idx, column in enumerate(children):
          row_data[column_names[column_idx]] = column.text

        table_data[current_class].append(row_data)

  data['data'] = table_data

  return data
