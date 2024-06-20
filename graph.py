from io import BytesIO
from random import choice
import pandas as pd
import circlify as cr
import matplotlib.pyplot as plt
import textwrap
import base64

def split_text(text, max_line_length):
    return '\n'.join(textwrap.wrap(text, max_line_length))

def bubble(db, property="famille", month=None):
    if not month:
        query = f"""
            SELECT {property}, COUNT(*) as count
            FROM reclamation_users
            GROUP BY {property}
            ORDER BY count DESC;
        """
    else:
        query = f"""
            SELECT {property}, COUNT(*) as count
            FROM reclamation_users
            WHERE EXTRACT(YEAR from date_fin) = EXTRACT(YEAR from CURRENT_DATE) AND EXTRACT(MONTH from date_fin) = {month}
            GROUP BY {property}
            ORDER BY count DESC;
        """

    res = pd.read_sql_query(query, db.engine)
    circles = cr.circlify(res['count'].tolist(),
                            show_enclosure=False,
                            target_enclosure=cr.Circle(x=0, y=0, r=1))

    circles.reverse()
    fig, ax = plt.subplots()

    ax.axis('off')
    ax.set_aspect('equal')  # show circles as circles, not as ellipses

    lim = max(max(abs(circle.x) + circle.r, abs(circle.y) + circle.r, )
              for circle in circles)
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)

    labels = res[property] 
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

    for i, (circle, label) in enumerate(zip(circles, labels)):
        picked_color = choice(colors)
        x, y, r = circle
        ax.add_patch(plt.Circle((x, y), r, alpha=0.7, linewidth=2, color=picked_color))
        if i < 3:
            wrapped_label = split_text(label, 10)
            ax.annotate(wrapped_label, (x, y), va='center', ha='center', size=10)

    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf8')



def horizentalBar(db, month=None):

    if not month:
        query = """ 
            select operateur, count(*) as count
            from reclamation_users
            group by operateur;
        """
    else:
        query = f""" 
            select operateur, count(*) as count
            from reclamation_users
            WHERE EXTRACT(YEAR from date_fin) = EXTRACT(YEAR from CURRENT_DATE) AND EXTRACT(MONTH from date_fin) = {month}
            group by operateur;
        """
    res = pd.read_sql_query(query, db.engine)
    fig, ax = plt.subplots()
    plt.box(False)

    ax.barh(res["operateur"].tolist(), res["count"].tolist(), align="center", color="#00BDAE")
    ax.set_xlabel("incidents traités", weight="bold")
    ax.set_ylabel("operateur", rotation="horizontal", weight="bold")
    ax.yaxis.set_label_coords(-0.05, 1.01)

    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf8')


def verticalBar(db, month=None):
    plt.rcParams.update({'font.size':6})
    if not month:
        query = """
            SELECT categorie, COUNT(*) as count
            FROM reclamation_users
            GROUP BY categorie;
        """
    else:
        query = """
            SELECT categorie, COUNT(*) as count
            FROM reclamation_users
            WHERE EXTRACT(YEAR from date_fin) = EXTRACT(YEAR from CURRENT_DATE) AND EXTRACT(MONTH from date_fin) = {month}
            GROUP BY categorie;
        """

    res = pd.read_sql_query(query, db.engine)
    fig, ax = plt.subplots()
    plt.box(False)
    bar_container = ax.bar([split_text(text, 10) for text in res["categorie"].tolist()], res["count"].tolist(), color="#00BDAE")
    ax.set(ylabel="Total d'Incidents", title="Category")

    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf8')

def plotmois(db):
    query = """
    SELECT date_ouverture
    FROM reclamation_users
    WHERE date_ouverture IS NOT NULL
    """
    df = pd.read_sql_query(query, db.engine)
    df['date_ouverture'] = pd.to_datetime(df['date_ouverture'])

    df['mois_annee'] = df['date_ouverture'].dt.to_period('M')
    monthly_counts = df['mois_annee'].value_counts().sort_index()

    plt.fill_between(monthly_counts.index.astype(str), monthly_counts.values, color='#DABCD1', alpha=0.4)
    plt.plot(monthly_counts.index.astype(str), monthly_counts.values, color='Slateblue', alpha=0.6)
    plt.ylabel('Total d\'incidents')
    plt.xticks(rotation=45)
    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf8')