import os
import shutil
from jinja2 import Environment, FileSystemLoader
import ho.pisa as pisa
import StringIO
from datetime import date
from yaml import load, Loader


def render_html_to_pdf(html, filename):
    pisa.showLogging()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), file(filename, "wb"))
    if pdf.err:
        print "Error: " + pdf.err


if __name__ == "__main__":
    # setup yaml reader
    templates_folder = "../" + "templates" + "/"
    env = Environment(loader=FileSystemLoader(templates_folder))

    # load settings if available
    settings = {}
    if os.path.exists(templates_folder + "settings.yaml"):
        settings = load(open(templates_folder + "settings.yaml"), Loader=Loader)

    # load entries yaml
    data = load(open(templates_folder + "entries.yaml"), Loader=Loader)

    # create and render template
    cv_template = settings.get("cv_template", "cv.html")
    template = env.get_template(cv_template)
    cv = template.render(entries=data, templates_folder=templates_folder)

    # output
    output_folder = "../" + settings.get("output_folder", "out") + "/"

    # clean output folder
    shutil.rmtree(output_folder)
    os.mkdir(output_folder)

    # create pdf
    date_format = settings.get("file_name", "cv-%Y.%m")
    title = date.today().strftime(date_format) + ".pdf"
    render_html_to_pdf(cv, output_folder + title)

    # success
    print title + " created."