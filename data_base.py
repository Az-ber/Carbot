#######################################################
#Импорт Склютайт3 база данных
#######################################################
import sqlite3 as sq


###########################################################
#Функция старта база данных: создание бд, создание таблицы
###########################################################

def sqlite_start():
  global base, cur
  base = sq.connect('car.db')
  cur = base.cursor()
  if base:
    print('Data base connected OK!')
  base.execute('CREATE TABLE IF NOT EXISTS menu(names TEXT, pass TEXT, cars TEXT, payment TEXT)')
  base.commit()


###########################################################################
#Функция добавить ячейкам данные из Memorystorage data после окончания FSM
###########################################################################

async def sql_add_command(state):
  async with state.proxy() as data:
    cur.execute('INSERT INTO menu VALUES(?,?,?,?)', tuple(data.values()))
    base.commit()


