import sqlite3
import tkinter as tk
import os
import datetime as dt


#variablen
bg_color = "#3d6466"


###Funktionen
def add_geburtstag(name, geburtsdatum):
    conn = sqlite3.connect('geburtstage.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO geburtstage (name, geburtsdatum) VALUES (?, ?)', (name, geburtsdatum))
    conn.commit()
    conn.close()
    print(get_geburtstage())

def get_geburtstage():
    conn = sqlite3.connect('geburtstage.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM geburtstage')
    geburtstage = cursor.fetchall()
    conn.close()
    return geburtstage

def einfuegen():
    
    Name = input_field.get()
    Date = input_field2.get()
    if Name != "" and Date != "":
        add_geburtstag(Name, Date)
    else: 
        print("Keine Eingabe")
    print(Name,":", Date)
    update_text_display()
    update_text_reminder()
"""def clear():
    conn = sqlite3.connect("geburtstage.db")
    cursor = conn.cursor()
    cursor.execute('DELETE FROM geburtstage')
    """
    
   
    
def delete_last_geburtstag():
    conn = sqlite3.connect('geburtstage.db')
    cursor = conn.cursor()
    # Ermittle die ID des letzten Eintrags
    cursor.execute('SELECT id FROM geburtstage ORDER BY id DESC LIMIT 1')
    last_entry = cursor.fetchone()
    if last_entry:
        # Lösche den letzten Eintrag
        cursor.execute('DELETE FROM geburtstage WHERE id = ?', (last_entry[0],))
        conn.commit()
    conn.close()
    update_text_display()
    update_text_reminder()
    print(get_geburtstage())    
 
 
def clear_id():
    id_ = input_id_clear.get()
    conn = sqlite3.connect('geburtstage.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM geburtstage WHERE id = ?', (id_[0],))
    conn.commit()
    conn.close()
    update_text_display()
    update_text_reminder()
    
def update_text_display():
    text_display.delete(1.0, tk.END)  # Vorhandenen Text löschen
    text_display.insert(tk.END, "alle Datensätze:\n")
    geburtstage = get_geburtstage()
    for geburtstag in geburtstage:
        text_display.insert(tk.END, f"{geburtstag}\n")
"""
def update_text_reminder():
    text_reminder.delete(1.0, tk.END)
    next_geburtstage = get_3_gb()
    print(next_geburtstage)
    for geburtstag in next_geburtstage:
        text_reminder.insert(tk.END, f"{geburtstag}\n")"""
    
    
def get_next_gb():
    conn = sqlite3.connect("geburtstage.db")
    cursor = conn.cursor()
    heute = dt.date.today()
    heute_str = heute.strftime("%m-%d")
    print(heute_str)
    cursor.execute('''
        SELECT * FROM geburtstage
        WHERE strftime('%m-%d', geburtsdatum) >= ?
        ORDER BY strftime('%m-%d', geburtsdatum)
        LIMIT 3
    ''', (heute_str,))
    next_geburtstage = cursor.fetchall()
    if len(next_geburtstage) < 3:
        cursor.execute('''
            SELECT * FROM geburtstage
            WHERE strftime('%m-%d', geburtsdatum) < ?
            ORDER BY strftime('%m-%d', geburtsdatum)
            LIMIT ?
        ''', (heute_str, 3 - len(next_geburtstage)))
        next_geburtstage += cursor.fetchall()

    conn.close()   
    formatted_birthdays = [(geb[1], geb[2], dt.datetime.strptime(geb[2], "%Y-%m-%d").strftime("%B %d")) for geb in next_geburtstage]
    
    return formatted_birthdays#next_geburtstage
    
   

def update_text_reminder():
    text_reminder.delete(1.0,tk.END)
    text_reminder.insert(tk.END, "Die nächsten Geburtstage:\n")
    ngb = get_next_gb()
    for gb in ngb:
        text_reminder.insert(tk.END, f"{gb[0]} : {gb[2]}\n")
    

def nxt_bg():
    get_next_gb()
    update_text_reminder()    
    
        
def del_all():
    conn = sqlite3.connect('geburtstage.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM geburtstage')
    conn.commit()
    conn.close()
    update_text_display()
    update_text_reminder()
    
def main_frame():
    
    frame2 = tk.Frame(root, width = 500, height = 600, bg = bg_color)
    frame2.grid(row = 0, column = 0)
    frame2.pack_propagate(False)
    print("Hello")
    label_nextgb = tk.Label(frame2, text = "Datum:",font = ("Arial", 25) ).pack()
    label_nextgb.grid(column = 1, row = 6, sticky = "e", pady = 5, padx = 10)
    #label_nextgb.pack()
    clear_widgets(frame2)
    


def clear_widgets(frame):
    for widget in frame.winfo_children():
        widget.destroy()
        
def popup():
    pass

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect('geburtstage.db')

# Cursor-Objekt erstellen
cursor = conn.cursor()

# Tabelle erstellen
cursor.execute('''
    CREATE TABLE IF NOT EXISTS geburtstage (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        geburtsdatum DATE NOT NULL
    )
''')

# Änderungen speichern und Verbindung schließen
conn.commit()
conn.close()


# Geburtstage abfragen
for geburtstag in get_geburtstage():
    print(geburtstag)
    #print(conn)
    
    
#GUI-------------------------------------------    
root = tk.Tk()
root.title("Geburtstage")
root.eval("tk::PlaceWindow . center")
#root.geometry("500x600")
#root.configure(background=bg_color)
#root.focus()"""
frame1 = tk.Frame(root,bg = bg_color)
#frame1.grid(row = 0, column = 0)
frame1.pack(fill = "both", expand = True)
#frame1.pack_propagate(False)



    
#frames
#frame1 = tk.Frame(root, width = 500, height = 600, bg = bg_color)
#frame1.grid(row = 0, column = 0)

###Text
text_display = tk.Text(frame1, height=5, width=30)
text_display.grid(column=0, row=6, columnspan=1, padx=10, pady=10)
#text_display.pack()
#text_display.insert(END , "Hi")


text_reminder = tk.Text(frame1, height = 5, width = 30 )
text_reminder.grid(column = 0, row = 4, columnspan = 1, padx = 10, pady = 10 )

###Labels
label_name= tk.Label(frame1, text = "Gb.-Datum\n(yyyy-mm-dd):",font = ("Arial", 12))
label_name.grid(column = 0, row = 1, sticky = "w", pady = 5, padx = 10)

label_name= tk.Label(frame1, text = "Name:        ",font = ("Arial", 12))
label_name.grid(column = 0, row = 0, sticky = "w", pady = 5, padx = 10)

###Input
input_field2 = tk.Entry(frame1, width = 20)
input_field2.grid(column = 0, row = 1, sticky = "e", pady = 5, padx = 10)

input_id_clear = tk.Entry(frame1, width = 20)
input_id_clear.grid(column = 0, row = 7, sticky = "e", pady = 5, padx = 10)

input_field = tk.Entry(frame1, width = 20)
input_field.grid(column = 0, row = 0, sticky = "e", pady = 5, padx = 10)

###button
button = tk.Button(frame1, text = "Einfügen", width = 30,  command = einfuegen) 
button.grid(column = 0, row = 2, sticky = "w", pady = 5, padx = 10)    

button_idclear = tk.Button(frame1, text = "ID-Nr. löschen:", command = clear_id )
button_idclear.grid(column = 0, row = 7, sticky = "w", pady = 5, padx = 10)

button_delete_last = tk.Button(frame1, text="Lösche letzten Eintrag", command=delete_last_geburtstag)
button_delete_last.grid(column=0, row=8, sticky="w", pady = 5, padx = 10)

button_del_all = tk.Button(frame1, text = "Lösche alles", command = del_all)
button_del_all.grid(column = 0, row = 9, sticky = "w", padx = 10, pady = 5)
"""
button_popup = tk.Button(frame1, text = "nächster Geburtstag", command = nxt_bg)
button_popup.grid(column = 0, row = 5, sticky = "w", padx = 10, pady = 5)"""
###
#main_frame()

get_next_gb()
update_text_reminder()
update_text_display()
root.mainloop()   




