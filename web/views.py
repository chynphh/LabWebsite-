from django.shortcuts import render
from web.models import About, Publictaion, Student, Research, News, Carousel


def forFooter():
    footerData = {}
    researches = Research.objects.order_by('-date')[:3]
    footerData['researches'] = researches
    return footerData


def home(request):
    news = News.objects.order_by('-date')[:6]
    carousels = Carousel.objects.order_by('-pk')
    publications = Publictaion.objects.order_by('-year', '-pk')[:6]
    students = Student.objects.order_by('year', '-pk')
    footerData = forFooter()
    return render(request, 'web/home.html', {'news': news, 'carousels': carousels, 'footerData': footerData, 'publications': publications, 'students': students})


def news(request):
    news = News.objects.order_by('-date')

    footerData = forFooter()
    return render(request, 'web/news.html', {'news': news, 'footerData': footerData})


def about(request):
    intro = About.objects.last().about

    footerData = forFooter()
    return render(request, 'web/about.html', {'intro': intro, 'footerData': footerData})


def publication(request):
    papers = Publictaion.objects.all()
    paper_dict = {}
    for paper in papers:
        if paper.year not in paper_dict:
            paper_dict[paper.year] = []
        paper_dict[paper.year].append(paper)
    for key, values in paper_dict.items():
        values.reverse()
    paper_list = sorted(paper_dict.items(), key=lambda d: d[0], reverse=True)

    footerData = forFooter()
    return render(request, 'web/publication.html', {'paper_list': paper_list, 'footerData': footerData})


def team(request):
    students = Student.objects.all()
    phd = []
    ms = []
    undergraduate = []
    alumni = []
    postdoc = []
    for stu in students:
        if stu.status is False:
            alumni.append(stu)
        elif stu.student_type == 'Ph.D.':
            phd.append(stu)
        elif stu.student_type == 'M.S.':
            ms.append(stu)
        elif stu.student_type == 'Undergraduates':
            undergraduate.append(stu)
        elif stu.student_type == 'Postdoc.':
            postdoc.append(stu)

    alumni = sorted(alumni, key=lambda d: d.year, reverse=True)
    phd = sorted(phd, key=lambda d: d.year)
    ms = sorted(ms, key=lambda d: d.year)
    undergraduate = sorted(undergraduate, key=lambda d: d.year)
    postdoc = sorted(postdoc, key=lambda d: d.year)

    footerData = forFooter()
    return render(request, 'web/team.html', {'current': [('Postdoc.',postdoc), ('Ph.D.', phd), ('M.S.', ms), ('Undergraduates', undergraduate)], 'alumni': alumni, 'footerData': footerData})


def research(request):
    researches = Research.objects.all()
    labels = set()
    for research in researches:
        if research.tag1 != '':
            labels.add(research.tag1)
        if research.tag2 != '':
            labels.add(research.tag2)
        if research.tag3 != '':
            labels.add(research.tag3)

    footerData = forFooter()
    return render(request, 'web/research.html', {'researches': researches, 'labels': labels, 'footerData': footerData})


def detail(request, detailtype, pk):
    if detailtype == 'news':
        obj = News.objects.get(pk=int(pk))
    elif detailtype == 'research':
        obj = Research.objects.get(pk=int(pk))
    obj.increase_views()

    footerData = forFooter()
    return render(request, 'web/detail.html', {'obj': obj, 'footerData': footerData})
