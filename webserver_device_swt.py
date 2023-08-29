from flask import Flask, request, render_template, redirect
import datetime
import __exec_sql
import create_table
create_table.create_db()

app = Flask(__name__)


def __reset_db():
    """Reset DB entries except locked ones"""
    __exec_sql.exec_querry(f"UPDATE device_list SET status ='Available', user ='' WHERE lock='F'")
    return redirect(request.referrer)
def last_upd_time():
    last = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    __exec_sql.exec_querry(f"UPDATE last_update SET time = '{last}'")
   
@app.route('/')
@app.route('/update', methods=['POST', 'GET'])
def main_page():
    if request.method == 'POST':
        last_upd_time()
        if request.form['add_txt']:
            add_name = request.form['add_txt']
            __exec_sql.exec_querry(
                f"INSERT INTO device_list(devices, status, user, type) VALUES ('{add_name}', 'Available', '', '')")
            return redirect(request.referrer)
        elif request.form['del_txt']:
            del_id = request.form['del_txt']
            if del_id.isdigit():
                del_id = int(del_id)
                if del_id != 0:
                    __exec_sql.exec_querry(
                        f"DELETE FROM device_list WHERE rowid = {del_id}")
                    db_list = __exec_sql.lista_db(
                        f"SELECT rowid,* FROM device_list")
                    for i in range(len(db_list)):
                        __exec_sql.exec_querry(
                            f"UPDATE device_list SET rowid = {del_id} WHERE rowid = {del_id + 1} ")
                        del_id += 1
                    return redirect(request.referrer)
                else:
                    return redirect(request.referrer)
            else:
                return redirect(request.referrer)
        else:
            db_list = __exec_sql.lista_db(f"SELECT rowid,* FROM device_list")
            lista_status_form = {}
            lista_user_form = {}
            lista_type_form = {}
            a = request.form.to_dict(flat=False)
            checkbox_list = {}
            for i in range(1, len(db_list)+1, 1):
                checkbox_list[f"lock_{i}"] = str(bool(a.get(f"lock_{i}")))
            i = 1
            for key in request.form.to_dict(flat=False):
                if f"type_inserat_{i}" in key:
                    lista_type_form[key] = request.form.to_dict(flat=False)[
                        key]
                elif f"status_inserat_{i}" in key:
                    lista_status_form[key] = request.form.to_dict(flat=False)[
                        key]
                elif f"user_inserat_{i}" in key:
                    lista_user_form[key] = request.form.to_dict(flat=False)[
                        key]
                    i += 1

            i = 0
            for key1, key2, key3, key4 in zip(lista_status_form, lista_user_form, checkbox_list, lista_type_form):
                if lista_status_form[key1][0] != db_list[i][2]:
                    __exec_sql.exec_querry(
                        f"UPDATE device_list SET status = '{lista_status_form[key1][0]}' WHERE rowid = {db_list[i][0]} ")
                if lista_user_form[key2][0] != db_list[i][3]:
                    __exec_sql.exec_querry(
                        f"UPDATE device_list SET user = '{lista_user_form[key2][0]}' WHERE rowid = {db_list[i][0]} ")
                if checkbox_list[key3][0] != db_list[i][4]:
                    __exec_sql.exec_querry(
                        f"UPDATE device_list SET lock = '{checkbox_list[key3][0]}' WHERE rowid = {db_list[i][0]} ")
                if lista_type_form[key4][0] != db_list[i][5]:
                    __exec_sql.exec_querry(
                        f"UPDATE device_list SET type = '{lista_type_form[key4][0]}' WHERE rowid = {db_list[i][0]} ")
                i += 1
            return redirect(request.referrer)
    else:
        # get current time
        now = datetime.datetime.now().time()
        # check if 19.00
        if now > datetime.time(19, 0, 0) and now < datetime.time(19, 10, 0):
            __reset_db()
        target_time = datetime.time(19, 0, 0)
        time_remaining = datetime.datetime.combine(datetime.date.today(), target_time) - datetime.datetime.combine(datetime.date.today(), now)
        countdown = int(time_remaining.total_seconds()/60)
        lista_devices = __exec_sql.lista_db(f"SELECT rowid,* FROM device_list")
        last_update = __exec_sql.lista_db(f"SELECT time FROM last_update")
        return render_template('webserver.html', lista_devices=lista_devices, last_update=last_update,countdown=countdown)
@app.route('/reset_fields', methods=['POST', 'GET'])
def reset_fields():
    if request.method=='POST':
        last_upd_time()
        __exec_sql.exec_querry(f"UPDATE device_list SET status = 'Available', user = '', lock = 'F'")
    return redirect(request.referrer)

@app.route('/help', methods=['POST', 'GET'])
def help_page():
    return render_template('help_page.html')

if __name__ == "__main__":
    app.run(debug=True)
