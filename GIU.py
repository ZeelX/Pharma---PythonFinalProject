import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import oracledb


def get_data_from_oracle(query):
    connection = oracledb.connect(user="system", password="root", dsn="localhost:1521/xe")
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    connection.close()
    return results

def get_graph_from_oracle(query):
    connection = oracledb.connect(user="system", password="root", dsn="localhost:1521/xe")
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()

    dates = []
    balances = []
    for row in results:
        dates.append(row[0])
        balances.append(row[1])

    return dates, balances


# Fonction pour créer et afficher le graphique
def show_graph():
    # Obtenir les données de la base Oracle
    query = """
        SELECT date_FK, count_value AS balance
        FROM F_TRANSACTION
        ORDER BY date_FK
    """
    dates, balances = get_graph_from_oracle(query)

    # Créer le graphique
    fig, ax = plt.subplots()
    ax.plot(dates, balances)
    ax.set_xlabel('Date')
    ax.set_ylabel('Balance')
    ax.set_title('Évolution de la balance du compte')

    # Afficher le graphique dans l'interface Tkinter
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()

def show_lowest_expense():

    query_expense = """
           SELECT name_category_FK, SUM(count_value)
            FROM F_TRANSACTION
            WHERE transaction_type_FK = 'D'
            GROUP BY name_category_FK
            ORDER BY SUM(count_value) ASC
            FETCH FIRST 1 ROWS ONLY
        """
    result_expense = get_data_from_oracle(query_expense)
    if result_expense:
        category_expense, expense = result_expense[0]
        result_label.config(
            text=f"Catégorie avec la dépense la plus basse : {category_expense}, Dépense totale : {expense}")


def show_highest_income():
    query = """
        SELECT name_category_FK, SUM(count_value)
        FROM F_TRANSACTION
        WHERE transaction_type_FK = 'C' 
        GROUP BY name_category_FK
        ORDER BY SUM(count_value) DESC
        FETCH FIRST 1 ROWS ONLY
    """
    result_income = get_data_from_oracle(query)
    if result_income:
        category_income, income = result_income[0]
        result_label.config(text=f"Catégorie avec le revenu le plus élevé : {category_income}, Revenu total : {income}")


window = tk.Tk()
window.title("Balance du compte")
# Créer un menu déroulant


show_lowest_expense_button = ttk.Button(window, text="Question 1", command=show_lowest_expense)
show_highest_income_button = ttk.Button(window, text="Question 2", command=show_highest_income)
show_graph_button = ttk.Button(window, text="Question 3", command=show_graph)

# Placement des boutons sur la même ligne
show_lowest_expense_button.pack(padx=10)
show_highest_income_button.pack(padx=10)
show_graph_button.pack(padx=10)

# Création d'un label pour afficher les résultats
result_label = ttk.Label(window, text="")
result_label.pack()

window.mainloop()
