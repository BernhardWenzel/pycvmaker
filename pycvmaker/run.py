import os
import shutil
from jinja2 import Environment, PackageLoader
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
    templates_folder = "../" + "templates" + "/"
    env = Environment(loader=PackageLoader('pycvmaker', templates_folder))

    # load entries yaml
    data = load(open(templates_folder + "entries.yaml"), Loader=Loader)

    # create and render template
    cv_template = "cv.html"
    template = env.get_template(cv_template)
    cv = template.render(entries=data)

    # output
    output_folder = "../" + "out" + "/"

    # mkdir
    os.mkdir(output_folder)

    # copy style.css
    shutil.copyfile(templates_folder + "style.css", output_folder + "style.css")

    # write html
    f = open(output_folder + "cv.html", "w")
    f.write(cv.encode("UTF-8"))

    # create pdf
    date_format = "bernhard.wenzel.cv-%Y.%m"
    title = date.today().strftime(date_format) + ".pdf"
    render_html_to_pdf(cv, output_folder + title)

    # success
    print title + " created."