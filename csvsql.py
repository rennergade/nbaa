import sqlite3


def genInsert(filename):

    conn = sqlite3.connect('datasetfull.db')

    db = []
    assets = []

    header = '''CREATE TABLE rankings(
       asset_id   INTEGER  NOT NULL PRIMARY KEY
      ,asset_name VARCHAR(121) NOT NULL
      ,ranking    INTEGER
      ,team_id    VARCHAR(3)
      ,notes      VARCHAR2(55)
      ,y1         INTEGER
      ,y1g        INTEGER
      ,y2         INTEGER
      ,y2g        INTEGER
      ,y3         INTEGER
      ,y3g        INTEGER
      ,y4         INTEGER
      ,y4g        INTEGER
      ,y5         INTEGER
      ,y5g        INTEGER
      ,playeropt  INTEGER
      ,teamopt    INTEGER
      ,eto        INTEGER
      ,qo         INTEGER
      ,bird       VARCHAR(5)
      ,ebird      VARCHAR(5)
      ,nonbird    VARCHAR(5)
      ,rfa        VARCHAR(5)
      ,ufa        VARCHAR(5)
      ,rights     VARCHAR(22)
      ,rightsinfo VARCHAR(30)
      ,ntc        VARCHAR(30)
      ,agent      VARCHAR(51)
      ,agency     VARCHAR(76)
      ,espn       VARCHAR(30)
      ,fivethirty VARCHAR(7)
    );\n\n'''

    pre = 'INSERT INTO rankings(asset_id,asset_name,ranking,team_id,notes,y1,y1g,y2,y2g,y3,y3g,y4,y4g,y5,y5g,playeropt,teamopt,eto,qo,bird,ebird,nonbird,rfa,ufa,rights,rightsinfo,ntc,agent,agency,espn,fivethirty) VALUES ('
    suff = ');\n'



    with open(filename) as csv:
        for line in csv: db.append(line.strip('\n\r'))
    for i in db:
        assets.append(i.split(','))

    insert = header

    for asset in assets:
        line = pre
        for i in range(len(asset)):
            if (asset[i] == ''): line += 'NULL'
            else:
                if (i == 1) or (i == 3) or (i ==4) or (19 <= i <= len(asset)): line += "'" + asset[i] + "'"
                else: line += asset[i]
            if (i != len(asset)-1): line += ','
        line += suff
        insert += line

    

    c = conn.cursor()
    try:
        c.execute('''DROP TABLE rankings ;''')
    except sqlite3.OperationalError:
        print "creating new table"
    c.executescript(insert)
    conn.commit()
    conn.close()
    return 0
