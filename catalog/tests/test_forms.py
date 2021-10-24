from django.test import TestCase
import datetime
from django.utils import timezone
from catalog.forms import RenewBookForm
from django.contrib.auth.models import User, Permission
from catalog.forms import RenewBookForm
from django.contrib.auth.decorators import permission_required
from catalog.models import Author, Genre, Language, Book, BookInstance



class RenewBookFormTest(TestCase):

    def test_renew_form_date_field_label(self):
        form = RenewBookForm()
        self.assertTrue(form.fields['renewal_date'].label == None or form.fields['renewal_date'].label == 'renewal date')

    def test_renew_form_date_field_help_text(self):
        form = RenewBookForm()
        self.assertEqual(form.fields['renewal_date'].help_text,'Введите дату между настоящим моментом и 4 неделями (по умолчанию 3).')

    def test_renew_form_date_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form_data = {'renewal_date': date}
        form = RenewBookForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_renew_form_date_too_far_in_future(self):
        date = datetime.date.today() + datetime.timedelta(weeks=4) + datetime.timedelta(days=1)
        form_data = {'renewal_date': date}
        form = RenewBookForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_renew_form_date_today(self):
        date = datetime.date.today()
        form_data = {'renewal_date': date}
        form = RenewBookForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_renew_form_date_max(self):
        date = timezone.now() + datetime.timedelta(weeks=4)
        form_data = {'renewal_date': date}
        form = RenewBookForm(data=form_data)
        self.assertTrue(form.is_valid())


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """
    Функция отображения обновления экземпляра BookInstance библиотекарем
    """
    book_inst=get_object_or_404(BookInstance, pk = pk)

    # Если это POST-запрос, тогда обработать данные формы
    if request.method == 'POST':

        # Создать объект формы и заполнить её данными из запроса (связывание/биндинг):
        form = RenewBookForm(request.POST)

        # Проверка валидности формы:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # переход по URL-адресу:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # Если это GET-запрос (или что-то ещё), то создаём форму по умолчанию
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})

