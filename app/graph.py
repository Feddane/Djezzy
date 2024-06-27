# import matplotlib
# matplotlib.use('Agg')

# from .models import ReclamationUser
# from . import db
# from sqlalchemy import func, extract
# import pandas as pd
# import circlify as cr
# import matplotlib.pyplot as plt
# import textwrap
# import base64
# from io import BytesIO
# from random import choice

# def split_text(text, max_line_length):
#     return '\n'.join(textwrap.wrap(text, max_line_length))


# def bubble(property="famille", month=None, categorie=None):

#     current_year = func.extract('year', func.current_date())
#     query = db.session.query(getattr(ReclamationUser, property), func.count().label('count'))

#     if month:
#         query = query.filter(extract('year', ReclamationUser.date_fin) == extract('year', func.current_date()))
#         query = query.filter(extract('month', ReclamationUser.date_fin) == month)

#     if categorie:
#         query = query.filter(ReclamationUser.categorie == categorie)

#     query = query.group_by(getattr(ReclamationUser, property))
#     query = query.order_by(func.count().desc())

#     res = query.all()
    
#     res = pd.DataFrame(res, columns=[property, "count"])

#     circles = cr.circlify(res['count'].tolist(),
#                             show_enclosure=False,
#                             target_enclosure=cr.Circle(x=0, y=0, r=1))

#     circles.reverse()
#     fig, ax = plt.subplots()

#     ax.axis('off')
#     ax.set_aspect('equal')  # show circles as circles, not as ellipses

#     lim = max(max(abs(circle.x) + circle.r, abs(circle.y) + circle.r)
#               for circle in circles)
#     ax.set_xlim(-lim, lim)
#     ax.set_ylim(-lim, lim)

#     labels = res[property]
#     colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

#     for i, (circle, label) in enumerate(zip(circles, labels)):
#         picked_color = choice(colors)
#         x, y, r = circle
#         ax.add_patch(plt.Circle((x, y), r, alpha=0.7, linewidth=2, color=picked_color))
#         if i < 3:
#             wrapped_label = split_text(label, 10)
#             ax.annotate(wrapped_label, (x, y), va='center', ha='center', size=10)

#     buf = BytesIO()
#     plt.savefig(buf, format='png')
#     plt.close()
#     buf.seek(0)
#     return base64.b64encode(buf.getvalue()).decode('utf8')

# def horizentalBar(month=None, categorie=None):

#     current_year = func.extract('year', func.current_date())
#     query = db.session.query(ReclamationUser.operateur, func.count().label('count'))

#     if month:
#         query = query.filter(extract('year', ReclamationUser.date_fin) == extract('year', func.current_date()))
#         query = query.filter(extract('month', ReclamationUser.date_fin) == month)

#     if categorie:
#         query = query.filter(ReclamationUser.categorie == categorie)

#     query = query.group_by(ReclamationUser.operateur)

#     res = query.all()
    
#     res = pd.DataFrame(res, columns=["operateur", "count"])

#     fig, ax = plt.subplots()
#     plt.box(False)

#     ax.barh(res["operateur"].tolist(), res["count"].tolist(), align="center", color="#00BDAE")
#     ax.set_xlabel("incidents traités", weight="bold")
#     ax.set_ylabel("operateur", rotation="horizontal", weight="bold")
#     ax.yaxis.set_label_coords(-0.05, 1.01)

#     buf = BytesIO()
#     plt.savefig(buf, format='png')
#     plt.close()
#     buf.seek(0)
#     return base64.b64encode(buf.getvalue()).decode('utf8')

# def verticalBar(month=None):

#     current_year = func.extract('year', func.current_date())
#     query = db.session.query(ReclamationUser.categorie, func.count().label('count'))

#     if month:
#         query = query.filter(extract('year', ReclamationUser.date_fin) == extract('year', func.current_date()))
#         query = query.filter(extract('month', ReclamationUser.date_fin) == month)

#     query = query.group_by(ReclamationUser.categorie)

#     res = query.all()
    
#     res = pd.DataFrame(res, columns=["categorie", "count"])

#     fig, ax = plt.subplots()
#     plt.box(False)
#     bar_container = ax.bar([split_text(text, 10) for text in res["categorie"].tolist()], res["count"].tolist(), color="#00BDAE")
#     ax.set(ylabel="Total d'Incidents", title="Category")

#     buf = BytesIO()
#     plt.savefig(buf, format='png')
#     plt.close()
#     buf.seek(0)
#     return base64.b64encode(buf.getvalue()).decode('utf8')

# def plotmois(categorie=None):
#     query = db.session.query(func.to_char(ReclamationUser.date_ouverture, "YYYY-MM-DD"))
#     query = query.filter(ReclamationUser.date_ouverture.is_not(None))
#     query = query.filter(extract('year', ReclamationUser.date_fin) == extract('year', func.current_date()))

#     if categorie:
#         query = query.filter(ReclamationUser.categorie == categorie)

#     res = query.all()

#     res = pd.DataFrame(res, columns=["date_ouverture"])

#     res['date_ouverture'] = pd.to_datetime(res['date_ouverture'])

#     res['mois_annee'] = res['date_ouverture'].dt.to_period('M')
#     monthly_counts = res['mois_annee'].value_counts().sort_index()


#     if monthly_counts.empty:
#         print("No data to plot.")
#         return None

#     plt.fill_between(monthly_counts.index.astype(str), monthly_counts.values, color='#DABCD1', alpha=0.4)
#     plt.plot(monthly_counts.index.astype(str), monthly_counts.values, color='Slateblue', alpha=0.6)
#     plt.ylabel('Total d\'incidents')
#     plt.xticks(rotation=45)
#     plt.tight_layout()

#     buf = BytesIO()
#     plt.savefig(buf, format='png')
#     plt.close()
#     buf.seek(0)
#     return base64.b64encode(buf.getvalue()).decode('utf8')

# def month_name_to_number(month_name):
#     month_names = {
#         'janvier': 1, 'février': 2, 'mars': 3, 'avril': 4,
#         'mai': 5, 'juin': 6, 'juillet': 7, 'août': 8,
#         'septembre': 9, 'octobre': 10, 'novembre': 11, 'décembre': 12
#     }
#     return month_names.get(month_name.lower())

def generate_statistic_images(mois=None, categorie=None):
    return None, None

# def generate_statistic_images(mois=None, categorie=None):
#     mois_num = None
#     if mois:
#         mois_num = month_name_to_number(mois)
#         if mois_num is None:
#             return None, "Invalid month name"

#     img_famille = bubble(property="famille", month=mois_num, categorie=categorie)
#     img_employe = horizentalBar(month=mois_num, categorie=categorie)
#     img_priorite = bubble(property="priorite", month=mois_num, categorie=categorie)
#     img_categorie = verticalBar(month=mois_num)
#     img_mois = plotmois(categorie=categorie)

#     return {
#         'img_famille': img_famille,
#         'img_employe': img_employe,
#         'img_priorite': img_priorite,
#         'img_categorie': img_categorie,
#         'img_mois': img_mois
#     }, None