from django.contrib import admin

from .models import Question, Choise, Person
# Register your models here.

class ChoisInline(admin.TabularInline):
    model = Choise
    extra = 0

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
        ]

    list_display = ['question_text', 'pub_date', 'was_published_recently']
    inlines = [ChoisInline]
    list_filter = ['pub_date',]
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Person)
