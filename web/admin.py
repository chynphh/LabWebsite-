from django.contrib import admin
from .models import Student, Publictaion, About, Research, News, Carousel

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'student_type', 'status',)


class PublictaionAdmin(admin.ModelAdmin):
    list_display = ('title',)


class ResearchAdmin(admin.ModelAdmin):
    list_display = ('title',)


class AboutAdmin(admin.ModelAdmin):
    list_display = ('about',)


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'date',)

class CarouselAdmin(admin.ModelAdmin):
    list_display = ('title',)

admin.site.register(Student, StudentAdmin)
admin.site.register(Publictaion, PublictaionAdmin)
admin.site.register(Research, ResearchAdmin)
admin.site.register(About, AboutAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Carousel, CarouselAdmin)
