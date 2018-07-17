'''
Library/API Imports
'''
from flask import Flask, render_template, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
import sys


app = Flask(__name__)
pp = pprint.PrettyPrinter()


@app.route('/')
def index():
    return render_template('landing.html', showthediv=0)

'''
"/form" Routes
'''
@app.route("/form")
def form():
    method = request.args.get("method")

    ### 
    ### Initial page, no parameters
    ###
    if method is None:
        return render_template("form.html", showthediv=0)

    ### 
    ### Modified page, retrieve method values from parameters
    ###
    else:
        method  = str(method.decode("utf-8"))
        year    = request.args.get("year", type=int)
        country = str(request.args.get("country").decode('utf-8'))
        disease = str(request.args.get("disease").decode('utf-8'))
        company = str(request.args.get("company").decode('utf-8'))
        drug    = str(request.args.get("drug").decode('utf-8'))

        country_row = request.args.get("country_row", type=int)
        country_col = request.args.get("country_col", type=int)
        
        ## Authorize credentials
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("client_secret.json", scope)
        client = gspread.authorize(creds)

        ## Open spreadsheet to corresponding year
        if year == 2010:
            spreadsheet = client.open("ORS Global Burden of Disease 2013 (2010/2013)")
        elif year == 2013:
            spreadsheet = client.open("ORS Global Burden of Disease 2015 (2010/2015)")
        elif year == 2015:
            spreadsheet = client.open("ORS Global Burden of Disease 2015 (2010/2015)")


        ### Retrieve corresponding JSON data  ###

        # Retrieve countries
        if method == "getCountries":
            worksheet = spreadsheet.worksheet("DALY")
            country_cells = worksheet.range("A4:A220")
            pp.pprint(country_cells)
            return jsonify(
                countries=[
                    {
                        "country":country_cell.value,
                        "row":country_cell.row,
                        "col":country_cell.col
                    } 
                    for country_cell in country_cells
                ]
            )


        # Retrieve diseases
        if method == "getDiseases":
            worksheet = spreadsheet.worksheet("DALY")
            disease_cells = worksheet.range(country_row, country_col+1, country_row, country_col+1+9)
            pp.pprint(disease_cells)
            return jsonify(
                diseases=[
                    {
                        "disease": worksheet.cell(2, disease_cell.col).value
                    }
                    for disease_cell in disease_cells if disease_cell.value
                ]
            )


        # Retrieve companies
        if method == "getCompanies":
            worksheet = spreadsheet.worksheet("Company")
            #TODO fill out the rest of this block, populating company_cells and formatting JSON
            company_cells = []
            return jsonify(
                companies=[
                    {

                    }
                    for company_cell in company_cells
                ]
            )


        # Retrieve drugs
        if method == "getDrugs":
            worksheet = spreadsheet.worksheet("Company")
            #TODO fill out the rest of this block, populating drug_cells and formatting JSON
            drug_cells = []
            return jsonify(
                drug=[
                    {

                    }
                    for drug_cell in drug_cells
                ]
            )


    #TODO Return error status if method name is not matched
    return 

if __name__ == '__main__':
    app.run(debug=False)
