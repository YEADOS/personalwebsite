from datetime import datetime, timedelta

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from app.db import get_db

bp = Blueprint('tracker', __name__, url_prefix='/tracker')

@bp.route('/leetcode', methods=('GET', 'POST'))
def view():

    db = get_db()
    streak = db.execute('SELECT * FROM streak WHERE id = 1').fetchone()

    return render_template('tracker/leetcode.html', streak=streak)

# Admin can manually update and change the values of the streak
@bp.route('/update_streak_admin', methods=['POST'])
def update_info():

    if request.method == 'POST':
        current_streak = request.form['cur_streak']
        longest_streak = request.form['lng_streak']
        start_date = request.form['start_date']
        
        db = get_db()
        error = None

        if not current_streak:
            error = 'Missing current streak.'
        elif not longest_streak:
            error = 'Missing longest streak.'
        elif not start_date:
            error = 'Missing start date.'

        if error is None: 
            try:
                db.execute(
                    """UPDATE streak
                    SET current_streak = ?, 
                        longest_streak = ?, 
                        streak_start_date = ?
                    WHERE id = ?""",
                    (current_streak, longest_streak, start_date, 1),
                )
                db.commit()
                               
            except db.IntegrityError:
                error = "Steak failed to update in database"

            return redirect(url_for('tracker.view'))

        
        flash(error)

    return redirect(url_for('tracker.view'))
    
# Chrome extension sends post request to this function which updates the streaks data in database and display
@bp.route('/update_streak', methods=['POST'])
def update_steak():


    db = get_db()
    error = None
    streak = db.execute('SELECT * FROM streak WHERE id = 1').fetchone()

    if streak is None:
        error = 'Could not load streak'
        # add streak to database
    
    if error is None:
        current_streak = streak['current_streak']
        longest_streak = streak['longest_streak']
        start_date = streak['streak_start_date']
        last_date = streak['streak_last_date']
        today_date = datetime.now().date()

        print(today_date)

        print("Before: " + str(current_streak) + " " + str(longest_streak) + " " + str(start_date) + " " + str(last_date))

        if (start_date is None):
            start_date = today_date
        elif (last_date is None):
            last_date = today_date

        # print(last_date + " " + start_date)

        if (last_date < today_date and (today_date - last_date).days ==1):
            current_streak += 1
        elif last_date < today_date and (today_date - last_date).days > 1:
            current_streak = 1      

        if (current_streak > longest_streak):
            longest_streak = current_streak

        last_date = today_date

        # if (last_date-start_date).days + 1 != current_streak:
        #     start_date = last_date
        
        # print(str(current_streak) + " " + str(longest_streak) + " " + str(start_date) + " " + str(last_date))

        try:
            db.execute(
                """UPDATE streak
                SET current_streak = ?, 
                    longest_streak = ?, 
                    streak_start_date = ?, 
                    streak_last_date = ?
                WHERE id = ?""",
                (current_streak, longest_streak, start_date, last_date, 1),
            )
            db.commit()
            print("After: " + str(current_streak) + " " + str(longest_streak) + " " + str(start_date) + " " + str(last_date))
            
        except db.IntegrityError:
            error = "Steak failed to update in database"

        return redirect(url_for('index'))

    flash(error)

    
    
    return redirect(url_for('index'))