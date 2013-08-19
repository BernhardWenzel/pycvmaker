import StringIO
import os
import datetime
from django.conf import settings
import ho.pisa as pisa

import sys,os
sys.path.append(os.getcwd()+"/../..")

class Skill:
    title = ""
    content = ""
    def __init__(self, title, content):
        self.title = title
        self.content = content

def get_skills():
    skills = [
        Skill("Development languages", get("skills-lang"))
        ,Skill("Web development", get("skills-web"))
        ,Skill("Database development", get("skills-db"))
        ,Skill("Frameworks", get("skills-frame"))
        ,Skill("QA", get("skills-qa"))
        ,Skill("Tools", get("skills-tools"))
        ,Skill("Server administration", get("skills-server"))
        ,Skill("Operating systems", get("skills-os"))
        ,Skill("Methods", get("skills-methods"))
    ]
    return skills

def get(key):
    from apps.wenzelconsulting.models import Entry
    return Entry.objects.filter(target__exact="cv").get(name__exact=key).content


#            ,'skills-lang':
#        ,'skills-web': get("skills-web")
#        ,'skills-db': get("skills-db")
#        ,'skills-server': get("skills-server")
#        ,'skills-frame': get("skills-frame")
#        ,'skills-qa': get("skills-qa")
#        ,'skills-tools': get("skills-tools")
#        ,'skills-os': get("skills-os")
#        ,'skills-methods': get("skills-methods")


def render_cv_to_html():
    """
     template = get_template(template_src)
     context = Context(context_dict)
     html  = template.render(context)
     """

    settings.configure(
        DEBUG=True, TEMPLATE_DEBUG=True,
        DATABASE_ENGINE='django.db.backends.mysql',
        DATABASE_NAME='wenzelconsultingdb',
        DATABASE_USER='root',
        DATABASE_PASSWORD='Ebert110',
        DATABASE_HOST='localhost',
        DATABASE_PORT='3306',
        )

    # those import have to appear *after* settings definition!
    from django.template import Template, Context
    from apps.wenzelconsulting.models import Project


    t = Template(str(open("cv.html").read()))
    projects = Project.objects.filter(is_side_project=False).filter(cv_disabled=False).order_by("-start")
    founderprojects = Project.objects.filter(is_side_project=True).filter(cv_disabled=False).order_by("-start")

    skills = get_skills()

    years = datetime.datetime.now().year - 2004

    c = Context({
        'projects': projects
        ,'founderprojects': founderprojects
        ,'highlights': get("highlights")
        ,'address_1': get("address_1")
        ,'address_2': get("address_2")
        ,'education': get("education")
        ,'skills': skills
        ,'languages': get("languages")
        ,'hobbies': get("hobbies")
        ,'years': years
    })
    return t.render(c)

def render_html_to_pdf(html, filename):
    pisa.showLogging()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), file(filename, "wb"))

    if pdf.err:
        print "Error: " + pdf.err

#	if not pdf.err:
#		return HttpResponse(result.getvalue(), mimetype='application/pdf')
#	return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))

if __name__ == "__main__":
    cv = render_cv_to_html()
    path = "../../static/files/"
    f = open(path+"bernhard.wenzel.cv.html", "w")
    f.write(cv.encode("UTF-8"))
    title = "bernhard.wenzel.cv-2013.04.pdf"
    render_html_to_pdf(cv, path+title)
    print title + " created."