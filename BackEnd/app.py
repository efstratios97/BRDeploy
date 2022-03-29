# Project Athena
'''
Owner: Efstratios Pahis
Contributors:
Description: Main-Class
'''

from flask import Flask
from flask_cors import CORS
import Flask.Endpoints.DataManagerAPI as api_dm
import Flask.Endpoints.UserManagerAPI as api_um
import Flask.Endpoints.DataCleanserAPI as api_dc
import Flask.Endpoints.DataAnalyzerAPI as api_da
import Flask.Endpoints.DataHealthAPI as api_dh
import Flask.Endpoints.ArchitectureViewAPI as api_av
import Flask.Endpoints.ExecutiveDashboardAPI as api_ed
import Flask.Endpoints.DataPlotManagerApi as api_dpm
import Flask.Endpoints.KPIManagerAPI as api_kpi
import Flask.Endpoints.KPIAspectManagerAPI as api_aspct
import BRIndividual.Endpoints.IndividualAPI as api_ind

BRapp = Flask(__name__)
CORS(BRapp)


@BRapp.route("/")
def helloWorld():
    return "<html>Hello says Project Athena</html>"


BRapp.register_blueprint(api_ind.blueprint)
BRapp.register_blueprint(api_dm.blueprint)
BRapp.register_blueprint(api_um.blueprint)
BRapp.register_blueprint(api_dc.blueprint)
BRapp.register_blueprint(api_da.blueprint)
BRapp.register_blueprint(api_dh.blueprint)
BRapp.register_blueprint(api_av.blueprint)
BRapp.register_blueprint(api_ed.blueprint)
BRapp.register_blueprint(api_dpm.blueprint)
BRapp.register_blueprint(api_aspct.blueprint)
BRapp.register_blueprint(api_kpi.blueprint)

if __name__ == "__main__":
    BRapp.run(host='127.0.0.1')
