import sys
import os
import datetime

from flask import Flask, request, abort
from flask.templating import render_template
from werkzeug.utils import redirect
from flask_mail import Mail, Message

from helpers.query import executeQuery
from helpers.views import (
    view_summary_daily,
    view_summary_monthly,
    view_summary_quarter1,
    view_summary_quarter2,
    view_summary_quarter3,
    view_summary_quarter4,
    view_distribute,
    view_distribute_expense,
    view_no_data,
)
from helpers.number_format import (
    qty_format,
    value_format,
    sales_value_percentage_format,
    sell_thru_rate_format,
)
from helpers.config import Config

from modules.distribute_daily_brand_share import distribute_daily_brand_share
from modules.distribute_monthly_brand import distribute_monthly_brand
from modules.distribute_monthly_gender import distribute_monthly_gender
from modules.distribute_monthly_category import distribute_monthly_category
from modules.summary_daily_store import summary_daily_store
from modules.summary_monthly import summary_monthly
from modules.summary_quarter1 import summary_quarter1
from modules.summary_quarter2 import summary_quarter2
from modules.summary_quarter3 import summary_quarter3
from modules.summary_quarter4 import summary_quarter4
from modules.distribute_account_expense import distribute_account_expense
from modules.distribute_daily_wholesale_customer import (
    distribute_daily_wholesale_customer,
)
from modules.distribute_daily_online_channel import distribute_daily_online_channel


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


app = Flask(__name__)
mail = Mail(app)
config = Config().get()

# MAIL CONFIG
app.config["MAIL_SERVER"] = config["mailServer"]
app.config["MAIL_PORT"] = config["mailPort"]
app.config["MAIL_USERNAME"] = config["mailUsername"]
app.config["MAIL_PASSWORD"] = config["mailPassword"]
app.config["MAIL_USE_TLS"] = config["mailTLS"]
app.config["MAIL_USE_SSL"] = config["mailSSL"]
mail = Mail(app)


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template("404.html"), 404


@app.route("/")
def index():
    return abort(404)


@app.route("/raven3")
@app.route("/raven3/<report_date>")
@app.route("/raven3/<report_date>/<int:top_limit>")
def raven3(report_date="0000-00-00", top_limit=config["topLimit"]):
    # fix on report_date always showing server boot time
    if report_date == "0000-00-00":
        report_date = datetime.datetime.now().strftime("%Y-%m-%d")
        report_year = datetime.datetime.strptime(report_date, "%Y-%m-%d").strftime("%Y")
        yint = int(report_year)
        yearA = str(yint) + "-01-01 00:00:00"
        yearB = str(yint) + "-04-01 00:00:00"
        yearC = str(yint) + "-04-01 00:00:00"
        yearD = str(yint) + "-07-01 00:00:00"
        yearE = str(yint) + "-07-01 00:00:00"
        yearF = str(yint) + "-10-01 00:00:00"
        yearG = str(yint) + "-10-01 00:00:00"
        yearH = str(yint + 1) + "-01-01 00:00:00"
        datetime1 = str(yint) + "-04-01 00:00:00"
        datetime2 = str(yint) + "-07-01 00:00:00"
        datetime3 = str(yint) + "-10-01 00:00:00"
        datetime4 = str(yint + 1) + "-01-01 00:00:00"
    # data prep
    report_year = datetime.datetime.strptime(report_date, "%Y-%m-%d").strftime("%Y")
    yint = int(report_year)
    yearA = str(yint) + "-01-01 00:00:00"
    yearB = str(yint) + "-04-01 00:00:00"
    yearC = str(yint) + "-04-01 00:00:00"
    yearD = str(yint) + "-07-01 00:00:00"
    yearE = str(yint) + "-07-01 00:00:00"
    yearF = str(yint) + "-10-01 00:00:00"
    yearG = str(yint) + "-10-01 00:00:00"
    yearH = str(yint + 1) + "-01-01 00:00:00"
    datetime1 = str(yint) + "-04-01 00:00:00"
    datetime2 = str(yint) + "-07-01 00:00:00"
    datetime3 = str(yint) + "-10-01 00:00:00"
    datetime4 = str(yint + 1) + "-01-01 00:00:00"
    data = {}
    data["company"] = config["company"]
    data["location"] = config["location"]
    # BENERIN PARAMETER DATENYA SUPAYA MUNCUL DI TEMPLATE
    data["date_report_data"] = datetime.datetime.strptime(
        report_date, "%Y-%m-%d"
    ).strftime("%A, %d %B %Y")
    # report creation date time
    now_human = datetime.datetime.now()
    data["date_report_creation"] = now_human.strftime("%d %B %Y %H:%M:%S")
    # widgets prep
    data["widgets"] = {}
    data["widgets"]["summary_daily_store"] = summary_daily_store(report_date)
    data["widgets"][
        "distribute_daily_online_channel"
    ] = distribute_daily_online_channel(report_date, top_limit)
    data["widgets"][
        "distribute_daily_wholesale_customer"
    ] = distribute_daily_wholesale_customer(report_date, top_limit)
    data["widgets"]["distribute_account_expense"] = distribute_account_expense(
        report_date
    )
    data["widgets"]["distribute_daily_brand_share"] = distribute_daily_brand_share(
        report_date, top_limit
    )
    data["widgets"]["summary_monthly"] = summary_monthly(report_date)
    data["widgets"]["summary_quarter1"] = summary_quarter1(yearA, yearB, datetime1)
    data["widgets"]["summary_quarter2"] = summary_quarter2(yearC, yearD, datetime2)
    data["widgets"]["summary_quarter3"] = summary_quarter3(yearE, yearF, datetime3)
    data["widgets"]["summary_quarter4"] = summary_quarter4(yearG, yearH, datetime4)
    data["widgets"]["distribute_monthly_brand"] = distribute_monthly_brand(
        report_date, top_limit
    )
    data["widgets"]["distribute_monthly_gender"] = distribute_monthly_gender(
        report_date, top_limit
    )
    data["widgets"]["distribute_monthly_category"] = distribute_monthly_category(
        report_date, top_limit
    )

    return render_template("raven3.html", data=data)


@app.route("/raven3/quarter")
@app.route("/raven3/quarter/<report_year>/<report_quarter>")
def quarter(report_year="", report_quarter=""):
    report_quarter = report_quarter.lower()
    data = {}
    data["company"] = config["company"]
    data["location"] = config["location"]
    now_human = datetime.datetime.now()
    data["date_report_creation"] = now_human.strftime("%d %B %Y %H:%M:%S")
    if report_year == "":
        report_year = datetime.datetime.now().strftime("%Y")
        yint = int(report_year)
        yearA = str(yint) + "-01-01 00:00:00"
        yearB = str(yint) + "-04-01 00:00:00"
        yearC = str(yint) + "-04-01 00:00:00"
        yearD = str(yint) + "-07-01 00:00:00"
        yearE = str(yint) + "-07-01 00:00:00"
        yearF = str(yint) + "-10-01 00:00:00"
        yearG = str(yint) + "-10-01 00:00:00"
        yearH = str(yint + 1) + "-01-01 00:00:00"
        datetime1 = str(yint) + "-04-01 00:00:00"
        datetime2 = str(yint) + "-07-01 00:00:00"
        datetime3 = str(yint) + "-10-01 00:00:00"
        datetime4 = str(yint + 1) + "-01-01 00:00:00"
        y = datetime.datetime.strptime(report_year, "%Y").strftime("%Y")
        data["date_report_data"] = y
        data["widgets"] = {}
        data["widgets"]["summary_quarter1"] = summary_quarter1(yearA, yearB, datetime1)
        data["widgets"]["summary_quarter2"] = summary_quarter2(yearC, yearD, datetime2)
        data["widgets"]["summary_quarter3"] = summary_quarter3(yearE, yearF, datetime3)
        data["widgets"]["summary_quarter4"] = summary_quarter4(yearG, yearH, datetime4)
    yint = int(report_year)
    yearA = str(yint) + "-01-01 00:00:00"
    yearB = str(yint) + "-04-01 00:00:00"
    yearC = str(yint) + "-04-01 00:00:00"
    yearD = str(yint) + "-07-01 00:00:00"
    yearE = str(yint) + "-07-01 00:00:00"
    yearF = str(yint) + "-10-01 00:00:00"
    yearG = str(yint) + "-10-01 00:00:00"
    yearH = str(yint + 1) + "-01-01 00:00:00"
    datetime1 = str(yint) + "-04-01 00:00:00"
    datetime2 = str(yint) + "-07-01 00:00:00"
    datetime3 = str(yint) + "-10-01 00:00:00"
    datetime4 = str(yint + 1) + "-01-01 00:00:00"
    if len(report_quarter) == 2:
        if report_quarter == "q1":
            string = "Januari, Februari, Maret "
            y = datetime.datetime.strptime(report_year, "%Y").strftime("%Y")
            data["date_report_data"] = string + y
            data["widgets"] = {}
            data["widgets"]["summary_quarter1"] = summary_quarter1(
                yearA, yearB, datetime1
            )
        elif report_quarter == "q2":
            string = "April, Mei, Juni "
            y = datetime.datetime.strptime(report_year, "%Y").strftime("%Y")
            data["date_report_data"] = string + y
            data["widgets"] = {}
            data["widgets"]["summary_quarter2"] = summary_quarter2(
                yearC, yearD, datetime2
            )
        elif report_quarter == "q3":
            string = "Juli, Agustus, September "
            y = datetime.datetime.strptime(report_year, "%Y").strftime("%Y")
            data["date_report_data"] = string + y
            data["widgets"] = {}
            data["widgets"]["summary_quarter3"] = summary_quarter3(
                yearE, yearF, datetime3
            )
        elif report_quarter == "q4":
            string = "Oktober, November, Desember "
            y = datetime.datetime.strptime(report_year, "%Y").strftime("%Y")
            data["date_report_data"] = string + y
            data["widgets"] = {}
            data["widgets"]["summary_quarter4"] = summary_quarter4(
                yearG, yearH, datetime4
            )
    else:
        if report_quarter == "q1-q2":
            string = "Januari - Juni "
            y = datetime.datetime.strptime(report_year, "%Y").strftime("%Y")
            data["date_report_data"] = string + y
            data["widgets"] = {}
            data["widgets"]["summary_quarter1"] = summary_quarter1(
                yearA, yearB, datetime1
            )
            data["widgets"]["summary_quarter2"] = summary_quarter2(
                yearC, yearD, datetime2
            )
        elif report_quarter == "q1-q3":
            string = "Januari - September "
            y = datetime.datetime.strptime(report_year, "%Y").strftime("%Y")
            data["date_report_data"] = string + y
            data["widgets"] = {}
            data["widgets"]["summary_quarter1"] = summary_quarter1(
                yearA, yearB, datetime1
            )
            data["widgets"]["summary_quarter2"] = summary_quarter2(
                yearC, yearD, datetime2
            )
            data["widgets"]["summary_quarter3"] = summary_quarter3(
                yearE, yearF, datetime3
            )
        elif report_quarter == "q1-q4":
            string = "Januari - Desember "
            y = datetime.datetime.strptime(report_year, "%Y").strftime("%Y")
            data["date_report_data"] = string + y
            data["widgets"] = {}
            data["widgets"]["summary_quarter1"] = summary_quarter1(
                yearA, yearB, datetime1
            )
            data["widgets"]["summary_quarter2"] = summary_quarter2(
                yearC, yearD, datetime2
            )
            data["widgets"]["summary_quarter3"] = summary_quarter3(
                yearE, yearF, datetime3
            )
            data["widgets"]["summary_quarter4"] = summary_quarter4(
                yearG, yearH, datetime4
            )
        elif report_quarter == "q2-q3":
            string = "April - September "
            y = datetime.datetime.strptime(report_year, "%Y").strftime("%Y")
            data["date_report_data"] = string + y
            data["widgets"] = {}
            data["widgets"]["summary_quarter2"] = summary_quarter2(
                yearC, yearD, datetime2
            )
            data["widgets"]["summary_quarter3"] = summary_quarter3(
                yearE, yearF, datetime3
            )
        elif report_quarter == "q2-q4":
            string = "April - Desember "
            y = datetime.datetime.strptime(report_year, "%Y").strftime("%Y")
            data["date_report_data"] = string + y
            data["widgets"] = {}
            data["widgets"]["summary_quarter2"] = summary_quarter2(
                yearC, yearD, datetime2
            )
            data["widgets"]["summary_quarter3"] = summary_quarter3(
                yearE, yearF, datetime3
            )
            data["widgets"]["summary_quarter4"] = summary_quarter4(
                yearG, yearH, datetime4
            )
        elif report_quarter == "q3-q4":
            string = "Juli - Desember "
            y = datetime.datetime.strptime(report_year, "%Y").strftime("%Y")
            data["date_report_data"] = string + y
            data["widgets"] = {}
            data["widgets"]["summary_quarter3"] = summary_quarter3(
                yearE, yearF, datetime3
            )
            data["widgets"]["summary_quarter4"] = summary_quarter4(
                yearG, yearH, datetime4
            )

    return render_template("raven3.html", data=data)


@app.route("/raven3/send")
@app.route("/raven3/send/<report_date>")
@app.route("/raven3/send/<report_date>/<int:top_limit>")
def send(report_date="0000-00-00", top_limit=config["topLimit"]):
    # fix on report_date always showing server boot time
    if report_date == "0000-00-00":
        report_date = datetime.datetime.now().strftime("%Y-%m-%d")
        report_year = datetime.datetime.strptime(report_date, "%Y-%m-%d").strftime("%Y")
        yint = int(report_year)
        yearA = str(yint) + "-01-01 00:00:00"
        yearB = str(yint) + "-04-01 00:00:00"
        yearC = str(yint) + "-04-01 00:00:00"
        yearD = str(yint) + "-07-01 00:00:00"
        yearE = str(yint) + "-07-01 00:00:00"
        yearF = str(yint) + "-10-01 00:00:00"
        yearG = str(yint) + "-10-01 00:00:00"
        yearH = str(yint + 1) + "-01-01 00:00:00"
        datetime1 = str(yint) + "-04-01 00:00:00"
        datetime2 = str(yint) + "-07-01 00:00:00"
        datetime3 = str(yint) + "-10-01 00:00:00"
        datetime4 = str(yint + 1) + "-01-01 00:00:00"
    # data prep
    report_year = datetime.datetime.strptime(report_date, "%Y-%m-%d").strftime("%Y")
    yint = int(report_year)
    yearA = str(yint) + "-01-01 00:00:00"
    yearB = str(yint) + "-04-01 00:00:00"
    yearC = str(yint) + "-04-01 00:00:00"
    yearD = str(yint) + "-07-01 00:00:00"
    yearE = str(yint) + "-07-01 00:00:00"
    yearF = str(yint) + "-10-01 00:00:00"
    yearG = str(yint) + "-10-01 00:00:00"
    yearH = str(yint + 1) + "-01-01 00:00:00"
    datetime1 = str(yint) + "-04-01 00:00:00"
    datetime2 = str(yint) + "-07-01 00:00:00"
    datetime3 = str(yint) + "-10-01 00:00:00"
    datetime4 = str(yint + 1) + "-01-01 00:00:00"
    data = {}
    data["company"] = config["company"]
    data["location"] = config["location"]
    # BENERIN PARAMETER DATENYA SUPAYA MUNCUL DI TEMPLATE
    data["date_report_data"] = datetime.datetime.strptime(
        report_date, "%Y-%m-%d"
    ).strftime("%A, %d %B %Y")
    # report creation date time
    now_human = datetime.datetime.now()
    data["date_report_creation"] = now_human.strftime("%d %B %Y %H:%M:%S")
    # widgets prep
    data["widgets"] = {}
    data["widgets"]["summary_daily_store"] = summary_daily_store(report_date)
    data["widgets"][
        "distribute_daily_online_channel"
    ] = distribute_daily_online_channel(report_date, top_limit)
    data["widgets"][
        "distribute_daily_wholesale_customer"
    ] = distribute_daily_wholesale_customer(report_date, top_limit)
    data["widgets"]["distribute_account_expense"] = distribute_account_expense(
        report_date
    )
    data["widgets"]["distribute_daily_brand_share"] = distribute_daily_brand_share(
        report_date, top_limit
    )
    data["widgets"]["summary_monthly"] = summary_monthly(report_date)
    data["widgets"]["summary_quarter1"] = summary_quarter1(yearA, yearB, datetime1)
    data["widgets"]["summary_quarter2"] = summary_quarter2(yearC, yearD, datetime2)
    data["widgets"]["summary_quarter3"] = summary_quarter3(yearE, yearF, datetime3)
    data["widgets"]["summary_quarter4"] = summary_quarter4(yearG, yearH, datetime4)
    data["widgets"]["distribute_monthly_brand"] = distribute_monthly_brand(
        report_date, top_limit
    )
    data["widgets"]["distribute_monthly_gender"] = distribute_monthly_gender(
        report_date, top_limit
    )
    data["widgets"]["distribute_monthly_category"] = distribute_monthly_category(
        report_date, top_limit
    )

    msg = Message(
        config["title"],
        sender=config["sender"],
        recipients=config["recipients"],
        html=render_template("raven3.html", data=data),
        cc=config["cc"],
        bcc=config["bcc"],
    )

    mail.send(msg)
    return "sent"


@app.route("/raven3/quarter/send")
@app.route("/raven3/quarter/send/<report_year>/<report_quarter>")
def quarter_send(report_year="", report_quarter=""):
    report_quarter = report_quarter.lower()
    data = {}
    data["company"] = config["company"]
    data["location"] = config["location"]
    now_human = datetime.datetime.now()
    data["date_report_creation"] = now_human.strftime("%d %B %Y %H:%M:%S")
    if report_year == "":
        report_year = datetime.datetime.now().strftime("%Y")
        yint = int(report_year)
        yearA = str(yint) + "-01-01 00:00:00"
        yearB = str(yint) + "-04-01 00:00:00"
        yearC = str(yint) + "-04-01 00:00:00"
        yearD = str(yint) + "-07-01 00:00:00"
        yearE = str(yint) + "-07-01 00:00:00"
        yearF = str(yint) + "-10-01 00:00:00"
        yearG = str(yint) + "-10-01 00:00:00"
        yearH = str(yint + 1) + "-01-01 00:00:00"
        datetime1 = str(yint) + "-04-01 00:00:00"
        datetime2 = str(yint) + "-07-01 00:00:00"
        datetime3 = str(yint) + "-10-01 00:00:00"
        datetime4 = str(yint + 1) + "-01-01 00:00:00"
        y = datetime.datetime.strptime(report_year, "%Y").strftime("%Y")
        data["date_report_data"] = y
        data["widgets"] = {}
        data["widgets"]["summary_quarter1"] = summary_quarter1(yearA, yearB, datetime1)
        data["widgets"]["summary_quarter2"] = summary_quarter2(yearC, yearD, datetime2)
        data["widgets"]["summary_quarter3"] = summary_quarter3(yearE, yearF, datetime3)
        data["widgets"]["summary_quarter4"] = summary_quarter4(yearG, yearH, datetime4)
    yint = int(report_year)
    yearA = str(yint) + "-01-01 00:00:00"
    yearB = str(yint) + "-04-01 00:00:00"
    yearC = str(yint) + "-04-01 00:00:00"
    yearD = str(yint) + "-07-01 00:00:00"
    yearE = str(yint) + "-07-01 00:00:00"
    yearF = str(yint) + "-10-01 00:00:00"
    yearG = str(yint) + "-10-01 00:00:00"
    yearH = str(yint + 1) + "-01-01 00:00:00"
    datetime1 = str(yint) + "-04-01 00:00:00"
    datetime2 = str(yint) + "-07-01 00:00:00"
    datetime3 = str(yint) + "-10-01 00:00:00"
    datetime4 = str(yint + 1) + "-01-01 00:00:00"
    if len(report_quarter) == 2:
        if report_quarter == "q1":
            string = "Januari, Februari, Maret "
            y = datetime.datetime.strptime(report_year, "%Y").strftime("%Y")
            data["date_report_data"] = string + y
            data["widgets"] = {}
            data["widgets"]["summary_quarter1"] = summary_quarter1(
                yearA, yearB, datetime1
            )
        elif report_quarter == "q2":
            string = "April, Mei, Juni "
            y = datetime.datetime.strptime(report_year, "%Y").strftime("%Y")
            data["date_report_data"] = string + y
            data["widgets"] = {}
            data["widgets"]["summary_quarter2"] = summary_quarter2(
                yearC, yearD, datetime2
            )
        elif report_quarter == "q3":
            string = "Juli, Agustus, September "
            y = datetime.datetime.strptime(report_year, "%Y").strftime("%Y")
            data["date_report_data"] = string + y
            data["widgets"] = {}
            data["widgets"]["summary_quarter3"] = summary_quarter3(
                yearE, yearF, datetime3
            )
        elif report_quarter == "q4":
            string = "Oktober, November, Desember "
            y = datetime.datetime.strptime(report_year, "%Y").strftime("%Y")
            data["date_report_data"] = string + y
            data["widgets"] = {}
            data["widgets"]["summary_quarter4"] = summary_quarter4(
                yearG, yearH, datetime4
            )
    else:
        if report_quarter == "q1-q2":
            string = "Januari - Juni "
            y = datetime.datetime.strptime(report_year, "%Y").strftime("%Y")
            data["date_report_data"] = string + y
            data["widgets"] = {}
            data["widgets"]["summary_quarter1"] = summary_quarter1(
                yearA, yearB, datetime1
            )
            data["widgets"]["summary_quarter2"] = summary_quarter2(
                yearC, yearD, datetime2
            )
        elif report_quarter == "q1-q3":
            string = "Januari - September "
            y = datetime.datetime.strptime(report_year, "%Y").strftime("%Y")
            data["date_report_data"] = string + y
            data["widgets"] = {}
            data["widgets"]["summary_quarter1"] = summary_quarter1(
                yearA, yearB, datetime1
            )
            data["widgets"]["summary_quarter2"] = summary_quarter2(
                yearC, yearD, datetime2
            )
            data["widgets"]["summary_quarter3"] = summary_quarter3(
                yearE, yearF, datetime3
            )
        elif report_quarter == "q1-q4":
            string = "Januari - Desember "
            y = datetime.datetime.strptime(report_year, "%Y").strftime("%Y")
            data["date_report_data"] = string + y
            data["widgets"] = {}
            data["widgets"]["summary_quarter1"] = summary_quarter1(
                yearA, yearB, datetime1
            )
            data["widgets"]["summary_quarter2"] = summary_quarter2(
                yearC, yearD, datetime2
            )
            data["widgets"]["summary_quarter3"] = summary_quarter3(
                yearE, yearF, datetime3
            )
            data["widgets"]["summary_quarter4"] = summary_quarter4(
                yearG, yearH, datetime4
            )
        elif report_quarter == "q2-q3":
            string = "April - September "
            y = datetime.datetime.strptime(report_year, "%Y").strftime("%Y")
            data["date_report_data"] = string + y
            data["widgets"] = {}
            data["widgets"]["summary_quarter2"] = summary_quarter2(
                yearC, yearD, datetime2
            )
            data["widgets"]["summary_quarter3"] = summary_quarter3(
                yearE, yearF, datetime3
            )
        elif report_quarter == "q2-q4":
            string = "April - Desember "
            y = datetime.datetime.strptime(report_year, "%Y").strftime("%Y")
            data["date_report_data"] = string + y
            data["widgets"] = {}
            data["widgets"]["summary_quarter2"] = summary_quarter2(
                yearC, yearD, datetime2
            )
            data["widgets"]["summary_quarter3"] = summary_quarter3(
                yearE, yearF, datetime3
            )
            data["widgets"]["summary_quarter4"] = summary_quarter4(
                yearG, yearH, datetime4
            )
        elif report_quarter == "q3-q4":
            string = "Juli - Desember "
            y = datetime.datetime.strptime(report_year, "%Y").strftime("%Y")
            data["date_report_data"] = string + y
            data["widgets"] = {}
            data["widgets"]["summary_quarter3"] = summary_quarter3(
                yearE, yearF, datetime3
            )
            data["widgets"]["summary_quarter4"] = summary_quarter4(
                yearG, yearH, datetime4
            )

    msg = Message(
        config["title"],
        sender=config["sender"],
        recipients=config["recipients"],
        html=render_template("raven3.html", data=data),
        cc=config["cc"],
        bcc=config["bcc"],
    )

    mail.send(msg)
    return "sent"


@app.route("/shutdown", methods=["GET"])
def shutdown():
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    func()
    return "Server shutting down..."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config["port"], debug=True)
