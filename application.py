import os
from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from werkzeug import secure_filename
from rankdbsetup import Base, Rankings
from csvsql import genInsert
import sqlite3


application = Flask(__name__)


engine = create_engine('sqlite:///datasetfull.db')
Base.metadata.bind = engine

session = scoped_session(sessionmaker(bind=engine))

@application.teardown_request
def remove_session(ex=None):
    session.remove()

@application.route('/')
@application.route('/index')
@application.route('/top100')
def top200():
    try:
        ranks = session.query(Rankings).filter(Rankings.ranking, Rankings.ranking <= 100).order_by(Rankings.ranking).all()
    except ValueError:
        print "Oops!  Database Error.  Try again..."

    return render_template('teams.html', ranks = ranks, team_name='Top 100', team_abbrev='nba')

@application.route('/all')
def allrank():
        try:
            ranks = session.query(Rankings).order_by(Rankings.ranking).all()
        except ValueError:
            print "Oops!  Database Error.  Try again..."

        return render_template('teams.html', ranks = ranks, team_name='Top 100', team_abbrev='nba')

@application.route('/<string:team_id>/')
def teams(team_id):
    try:
        ranks = session.query(Rankings).filter_by(team_id=team_id).order_by(Rankings.ranking).all()
    except ValueError:
        print "Oops!  Database Error.  Try again..."
    return render_template('teams.html', ranks = ranks, team_name=teamabbrev[team_id], team_abbrev=team_id)

@application.route('/player/<string:asset_id>/')
def player(asset_id):
    try:
        player = session.query(Rankings).filter_by(asset_id=asset_id).order_by(Rankings.ranking).all()
        team_id = player[0].team_id
    except ValueError:
        print "Oops!  Database Error.  Try again..."
    return render_template('player.html', player = player, team_name=teamabbrev[team_id], team_abbrev=team_id)

@application.route('/about')
def about():
    return render_template('about.html')

@application.route('/upload')
def upload():
   return render_template('upload.html')

@application.route('/uploadsuccess')
def uploadsuccess():
  return render_template('uploadsuccess.html')

@application.route('/uploaderror')
def uploaderror():
    return render_template('uploaderror.html')

@application.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      filename = str(f.filename)
      try:
          genInsert(filename)
      except:
          return redirect(url_for('uploaderror'))
      return redirect(url_for('uploadsuccess'))

@application.route('/snek')
def snek():
   return render_template('snek.html')



teamabbrev = {
    'DAL': 'Dallas Mavericks',
    'HOU': 'Houston Rockets',
    'MEM': 'Memphis Grizzlies',
    'NOP' : 'New Orleans Pelicans',
    'SAS': 'San Antonio Spurs',
    'GSW': 'Golden State Warriors',
    'LAL': 'Los Angeles Lakers',
    'LAC': 'Los Angeles Clippers',
    'PHX': 'Phoenix Suns',
    'SAC': 'Sacramento Kings',
    'DEN': 'Denver Nuggets',
    'MIN': 'Minnesota Timberwolves',
    'OKC': 'Oklahoma City Thunder',
    'POR': 'Portland Trailblazers',
    'UTH': 'Utah Jazz',

    'BOS': 'Boston Celtics',
    'BRK': 'Brooklyn Nets',
    'NYK': 'New York Knicks',
    'PHL': 'Philadelphia 76ers',
    'TOR': 'Toronto Raptors',
    'CHI': 'Chicago Bulls',
    'CLE': 'Cleveland Cavaliers',
    'DET': 'Detroit Pistons',
    'IND': 'Indiana Pacers',
    'MIL': 'Milwaukee Bucks',
    'ATL': 'Atlanta Hawks',
    'CHA': 'Charlotte Hornets',
    'MIA': 'Miami Heat',
    'ORL': 'Orlando Magic',
    'WAS': 'Washington Wizards'
}

if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production application.
    application.debug = False
    application.run()
