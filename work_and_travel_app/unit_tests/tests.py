from datetime import date, timedelta

import pytest
from django.contrib.auth.models import User
from django.db.models import Avg

from django.urls import reverse
from django.utils import timezone

from work_and_travel_app.models import Offer, BaseInformation, Category, Message, Answer, Grade


@pytest.fixture
def users(db):
    users = [
        User.objects.create_user(username='user1', password='testpassword1'),
        User.objects.create_user(username='user2', password='testpassword2'),
        User.objects.create_user(username='user3', password='testpassword3'),
    ]
    return users


@pytest.fixture
def base_info(db, users):
    base_info_1 = BaseInformation.objects.create(
        user=users[0],
        contact_number='123456789',
        date_of_birth=date(2000, 2, 29),
        are_you_traveling=False,
        native_origin='Poland',
        sex='male'
    )

    base_info_2 = BaseInformation.objects.create(
        user=users[1],
        contact_number='987654321',
        date_of_birth=date(1985, 5, 15),
        are_you_traveling=True,
        native_origin='Spain',
        sex='female'
    )

    base_info_3 = BaseInformation.objects.create(
        user=users[2],
        contact_number='555444333',
        date_of_birth=date(1992, 8, 20),
        are_you_traveling=False,
        native_origin='Japan',
        sex='other'
    )

    return base_info_1, base_info_2, base_info_3


@pytest.fixture
def create_categories(db):
    categories = [
        Category.objects.create(name='Technology'),
        Category.objects.create(name='Marketing'),
        Category.objects.create(name='Design')
    ]
    return categories


@pytest.fixture
def create_offers(db, users, create_categories):
    offer_1 = Offer.objects.create(
        name='Software Developer',
        country='Poland',
        city='Warsaw',
        description='Looking for a skilled developer.',
        offer_type='job offer',
        since_when=date(2023, 5, 1),
        until_when=date(2024, 5, 1),
        only_for_women=False,
        owner=users[0],
        is_active=True,
    )
    offer_1.category.add(create_categories[0])

    offer_2 = Offer.objects.create(
        name='Digital Marketer',
        country='Canada',
        city='Toronto',
        description='Expert in digital marketing.',
        offer_type='job offer',
        since_when=date(2024, 2, 29),
        until_when=date(2024, 5, 1),
        only_for_women=True,
        owner=users[1],
        is_active=True
    )
    offer_2.category.add(create_categories[1])

    offer_3 = Offer.objects.create(
        name='Graphic Designer',
        country='UK',
        city='London',
        description='Creative graphic designer wanted.',
        offer_type='job seekers',
        since_when=date(2023, 10, 30),
        until_when=date(2024, 2, 29),
        only_for_women=False,
        owner=users[2],
        is_active=False
    )
    offer_3.category.add(create_categories[2])

    return [offer_1, offer_2, offer_3]


@pytest.fixture
def create_base_info(db, create_user):
    return BaseInformation.objects.create(
        user=create_user,
        contact_number='123456789',
        date_of_birth=date(2000, 2, 29),
        are_you_traveling=False,
        native_origin='Example Country',
        sex='female',
    )


@pytest.fixture
def messages(db, users, create_offers):
    message_1 = Message.objects.create(
        message='Is this job still available?',
        receiver=users[1],
        sender=users[0],
        offer=create_offers[0]
    )

    message_2 = Message.objects.create(
        message='Can you provide more details?',
        receiver=users[2],
        sender=users[1],
        offer=create_offers[1]
    )

    message_3 = Message.objects.create(
        message='I am interested in this position.',
        receiver=users[0],
        sender=users[2],
        offer=create_offers[2]
    )

    return message_1, message_2, message_3


@pytest.fixture
def grade(db, users, messages):
    return Grade.objects.create(
        grade=5,
        user=users[0],
        description='Excellent experience!',
        message=messages[2]
    )


@pytest.fixture
def answer(db, grade):
    return Answer.objects.create(
        answer=grade,
        grade_answer=4,
        text='Thank you for your feedback!'
    )


"""testy do logowania uzytkownika"""


# czy URL sie zgadza i czy strona jest dostępna
@pytest.mark.django_db
def test_login_page_url(client):
    response = client.get(reverse('login_view'))
    assert 'Login' in response.content.decode()


# test wyswietlania formularza
@pytest.mark.django_db
def test_login_form(client):
    response = client.get(reverse('login_view'))
    assert 'username' in response.content.decode()
    assert 'password' in response.content.decode()


# test poprawności logowania, test validacji

@pytest.mark.django_db
@pytest.mark.parametrize('username, password, expected_redirect, expected_status_code, expected_content', [
    ('user1', 'testpassword1', True, 200, reverse('your_profile')),
    ('user1', 'wrongpassword', False, 200, 'Error'),
    ('nonexistent', 'noonehere', False, 200, 'Error'),
])
def test_login_loggin(client, users, username, password, expected_redirect, expected_status_code,
                      expected_content):
    user_credentials = {'username': username, 'password': password}
    response = client.post(reverse('login_view'), user_credentials, follow=True)

    if expected_redirect:
        assert response.redirect_chain[-1][0] == expected_content
    else:
        assert response.status_code == expected_status_code
        assert expected_content in response.content.decode() or 'login_form.html' in [t.name for t in
                                                                                      response.templates]


"""testy do widoku Register"""


# dostepności

@pytest.mark.django_db
def test_registration_page(client):
    response = client.get(reverse('register_view'))
    assert 'Registration' in response.content.decode()


# czy dziala rejestracja
@pytest.mark.django_db
def test_registration(client):
    new_user = {
        'username': 'newuser',
        'first_name': 'New',
        'last_name': 'User',
        'password': 'newpassword123',
        're_password': 'newpassword123',
    }
    response = client.post(reverse('register_view'), new_user, follow=True)
    assert response.redirect_chain[-1][0] == reverse('your_profile')  # przekierownie
    assert User.objects.filter(username='newuser').exists()  # czy istnieje
    assert '_auth_user_id' in client.session  # czy jest zaologowany po rejestracji


# nie poprawna rejestracja
@pytest.mark.django_db
@pytest.mark.parametrize('username, password, re_password, expected_error', [
    ('newuser', 'newpassword123', 'differentpassword123', 'Password must be the same'),
    ('user1', 'password123', 'password123', 'A user with that username already exists.'),
])
def test_registration_errors(client, users, username, password, re_password, expected_error):
    user = {
        'username': username,
        'first_name': 'Test',
        'last_name': 'User',
        'password': password,
        're_password': re_password,
    }
    response = client.post(reverse('register_view'), user)
    assert expected_error in response.content.decode()


"""Testy do widoku Logout"""


# dostępnopści, przekiwrowanie

@pytest.mark.django_db
def test_logout_page(client, users):
    client.force_login(users[0])
    response = client.get(reverse('logout_view'), follow=True)
    assert response.redirect_chain[-1][0] == reverse('login_view')


# czy naprawde wylogowuje

@pytest.mark.django_db
def test_user_logout(client, users):
    client.force_login(users[0])
    assert '_auth_user_id' in client.session  # spr czy uzytkownik w sesji jest zalogowany
    client.get(reverse('logout_view'))  # wchodzimy na widok metoda get
    assert '_auth_user_id' not in client.session  # spr czy uzytkownik w sesji jest wylogowany


"""testy do widoku Start"""


# czy strona startowa jest dostępna i czy nie wymaga logowania
@pytest.mark.django_db
def test_start_page(client):
    response = client.get(reverse('start'))
    assert 'Work, world & travel' in response.content.decode()


# czy wyszukiwanie w różnych wariantach działa
@pytest.mark.django_db
@pytest.mark.parametrize('search_query', ['Poland', 'poland', 'POLAND', 'PoLaNd'])
def test_search_country(client, create_offers, search_query):
    response = client.get(reverse('start'), {'search': search_query},
                          follow=True)  # automatycznie śledził przekierowania
    assert response.redirect_chain[-1][0].endswith(
        f"/offers_list/?search={search_query}")  # czy ostatnie przekierowanie w łańcuchu przekierowań ma koncówke url z offer_lit kończą się na search_query


# co jak nie ma ofert
@pytest.mark.django_db
def test_search_no_results(client, create_offers):
    response = client.get(reverse('start'), {'search': 'Atlantis'}, follow=True)
    assert 'No offers found' in response.content.decode() or len(
        response.context['offers']) == 0  # decode używa sie do dekodowania np. ciagu znaków


# co jak jest puste wyszukiwanie
def test_search_offers_empty(client, create_offers):
    response = client.get(reverse('start'), {'search': ''})
    assert 'start.html' in [t.name for t in response.templates]  # sprawdza czy uzyty jest poprawny szablon


"""testy do widoku YourProfile """


# dostępność
@pytest.mark.django_db
def test_your_profile(client, users):
    client.force_login(users[0])
    response = client.get(reverse('your_profile'))
    assert response.status_code == 200


# czy infromacje sie zgadzaja
@pytest.mark.django_db
def test_your_profile_data(client, users, base_info):
    client.force_login(users[0])
    response = client.get(reverse('your_profile'))
    content = response.content.decode()
    assert users[0].username in content
    assert str(base_info[0].contact_number) in content
    assert str(base_info[0].date_of_birth) in content
    assert base_info[0].native_origin in content
    assert base_info[0].get_sex_display() in content
    assert base_info[0].contact_number in content


# obliczenie sredniej

@pytest.mark.django_db
def test_average_grade_calculation(client, users, grade, answer):
    # Logowanie użytkownika, którego dotyczy grade i answer
    client.force_login(users[0])

    # Obliczanie oczekiwanej średniej
    grades_avg = Grade.objects.filter(user=users[0]).aggregate(Avg('grade'))['grade__avg'] or 0
    answers_avg = Answer.objects.filter(answer__user=users[0]).aggregate(Avg('grade_answer'))['grade_answer__avg'] or 0
    expected_avg = (grades_avg + answers_avg) / 2 if grades_avg and answers_avg else grades_avg or answers_avg

    # Pobieranie strony profilu
    response = client.get(reverse('your_profile'))
    content = response.content.decode()

    # Sprawdzanie, czy średnia ocena jest wyświetlana na stronie
    # Upewnij się, że formatowanie liczby jest zgodne z formatowaniem na stronie
    expected_avg_formatted = "{:.2f}".format(expected_avg)
    assert f"Your average grade is: {expected_avg_formatted}" in content


# test linku add base info
@pytest.mark.django_db
def test_your_profile_without_base_info(client, users):
    client.force_login(users[0])

    response = client.get(reverse('your_profile'))
    content = response.content.decode()

    assert 'Add Base Information' in content
    assert 'Edit Base Information' not in content


# test linku kiedy jest base info
@pytest.mark.django_db
def test_your_profile_with_base_info(client, users, base_info):
    client.force_login(users[0])

    response = client.get(reverse('your_profile'))
    content = response.content.decode()

    assert 'Edit Base Information' in content
    assert 'Add Base Information' not in content


"""testy do widoku AddBaseInfo"""


# dodawnie informacji poprawnych

@pytest.mark.django_db
def test_add_base_info_success(client, users):
    client.force_login(users[0])
    response = client.post(reverse('add_base_info'), {
        'contact_number': '123456789',
        'date_of_birth': '1990-01-01',
        'are_you_traveling': True,
        'native_origin': 'Testland',
        'sex': 'male'
    }, follow=True)
    assert BaseInformation.objects.filter(user=users[0]).exists()


# Test walidacji daty urodzenia i nie poprawnych dat
@pytest.mark.django_db
@pytest.mark.parametrize("date_of_birth, expected_valid, expected_error_message", [
    (date.today() - timedelta(days=365 * 25), True, ""),
    (date.today() + timedelta(days=1), False, "The given date of birth is in the future."),
    (date(2000, 2, 29), True, ""),
])
def test_add_base_info_form_validation(client, users, date_of_birth, expected_valid, expected_error_message):
    client.force_login(users[0])
    response = client.post(reverse('add_base_info'), {
        'contact_number': '1234567890',
        'date_of_birth': date_of_birth.strftime('%Y-%m-%d'),
        'are_you_traveling': False,
        'native_origin': 'Testland',
        'sex': 'male'
    }, follow=True)

    if expected_valid:  # jest prawidowy
        assert response.redirect_chain, "Expected redirect but got none"  # przekierowanie nastąpiło
    else:  # Formularz jest nieprawidłowy
        assert 'form' in response.context, "Form is missing in response context"
        form_errors = str(response.context['form'].errors)
        assert expected_error_message in form_errors, f"Expected error message '{expected_error_message}' not found in form errors"


# czy zalogowany ma dostep do edycji
@pytest.mark.django_db
def test_add_base_info_user_logged(client, users):
    client.force_login(users[0])
    response = client.get(reverse('add_base_info'))
    assert response.status_code == 200


# Czy nie zalogowany jest przekiwerowny
@pytest.mark.django_db
def test_add_base_info_stranger(client):
    response = client.get(reverse('add_base_info'))
    assert response.status_code == 302


"""testy do widoku EditBaseInfo"""


# czy zalogowany ma dostep do edycji
@pytest.mark.django_db
def test_edit_base_info_user_logged(client, users):
    client.force_login(users[0])
    response = client.get(reverse('edit_base_info'))
    assert response.status_code == 200


# Czy nie zalogowany jest przekiwerowny
@pytest.mark.django_db
def test_edit_base_info_stranger(client):
    response = client.get(reverse('edit_base_info'))
    assert response.status_code == 302


# czy wyswietla istniejace informacje
@pytest.mark.django_db
def test_edit_base_info_form_display(client, users, base_info):
    client.force_login(users[0])
    response = client.get(reverse('edit_base_info'))
    content = response.content.decode()
    assert str(base_info[0].contact_number) in content


# Czy udalo sie edytować
@pytest.mark.django_db
def test_edit_base_info_update(client, users, base_info):
    client.force_login(users[0])
    response = client.post(reverse('edit_base_info'), {
        'contact_number': '999888777',
        'date_of_birth': '1990-01-01',
        'are_you_traveling': False,
        'native_origin': 'Testland',
        'sex': 'other',
    }, follow=True)
    updated_info = BaseInformation.objects.get(user=users[0])
    assert updated_info.contact_number == '999888777'
    assert response.redirect_chain[-1][0] == reverse('your_profile')


# czy walidacja działa jak jest bład
@pytest.mark.django_db
def test_edit_base_info_form_validation(client, users, base_info):
    client.force_login(users[0])
    future_date = timezone.now().date() + timezone.timedelta(days=30)
    response = client.post(reverse('edit_base_info'), {
        'date_of_birth': future_date,
    })
    assert "The given date of birth is in the future." in response.context['form'].errors['date_of_birth']


# czy dobrze przekiwerywyje zapisz i czy dane sa zakutalizowane

@pytest.mark.django_db
def test_edit_base_info_success_redirect(client, users, base_info):
    client.force_login(users[0])
    updated_data = {
        'contact_number': '987654321',
        'date_of_birth': '1990-01-01',
        'are_you_traveling': True,
        'native_origin': 'UpdatedLand',
        'sex': 'female',
    }
    response = client.post(reverse('edit_base_info'), updated_data, follow=True)

    assert response.redirect_chain[-1][0] == reverse('your_profile')

    user_info = BaseInformation.objects.get(user=users[0])
    assert user_info.contact_number == updated_data['contact_number']
    assert str(user_info.date_of_birth) == updated_data['date_of_birth']
    assert user_info.are_you_traveling == updated_data['are_you_traveling']
    assert user_info.native_origin == updated_data['native_origin']
    assert user_info.sex == updated_data['sex']


"""testy do widku AddOffer """


# dostepnośc
@pytest.mark.django_db
def test_add_offer_logged(client, users):
    client.force_login(users[0])
    response = client.get(reverse('add_offer'))
    assert 'Add your offer' in response.content.decode()


# nie zaologowany czy działa
@pytest.mark.django_db
def test_add_offer_page_redirect_anonymous(client):
    response = client.get(reverse('add_offer'))
    assert '/login/' in response.url


# czy działa walidacja na blędnej dacie i dziwnych datach - dwa nie działaja :(
@pytest.mark.django_db
@pytest.mark.parametrize("since_when, until_when, is_valid, error_message", [
    (timezone.now().date() + timedelta(days=1), timezone.now().date() + timedelta(days=2), True, ""),
    (timezone.now().date().replace(year=2020, month=3, day=2), timezone.now().date().replace(year=2021, month=2, day=3),
     False, "None of the dates can be older than today."),
    (timezone.now().date().replace(year=2025, month=2, day=20),
     timezone.now().date().replace(year=2024, month=10, day=10), False,
     '"Since when" date must be later than the "until when" date.'),
    (
            timezone.now().date().replace(year=2024, month=2, day=29),
            timezone.now().date().replace(year=2024, month=3, day=1),
            True, ""),
])
def test_add_offer_validation(client, users, create_categories, since_when, until_when, is_valid, error_message):
    client.force_login(users[0])
    categories = create_categories
    category_ids = [str(category.id) for category in categories]

    response = client.post(reverse('add_offer'), {
        'name': 'Test Offer',
        'country': 'Test Country',
        'city': 'Test City',
        'description': 'Test Description',
        'offer_type': 'job offer',
        'category': category_ids,
        'since_when': since_when,
        'until_when': until_when,
        'only_for_woman': True,
        'owner': users[0],
        'is_active': True
    }, follow=True)

    if is_valid:
        assert 'form' not in response.context or not response.context['form'].errors
    else:
        assert error_message in response.content.decode() or 'category' in str(response.context['form'].errors)


# czy sie zapisuje czy włascicle sie zgadza i czy przekierowywuje
@pytest.mark.django_db
def test_add_offer_save(client, users, create_categories):
    client.force_login(users[0])
    categories = create_categories
    category_ids = [str(category.id) for category in categories]
    response = client.post(reverse('add_offer'), {
        'name': 'Test Offer',
        'country': 'Test Country',
        'city': 'Test City',
        'description': 'Test Description',
        'offer_type': 'job offer',
        'category': category_ids,
        'since_when': timezone.now().date() + timedelta(days=1),
        'until_when': timezone.now().date() + timedelta(days=2),
        'only_for_woman': True,
        'owner': users[0],
        'is_active': True
    })
    assert Offer.objects.filter(name='Test Offer').exists()
    assert Offer.objects.filter(owner=users[0]).exists()
    assert response.url == reverse('offers_list')


# Sprawdzenie, czy wszystkie kategorie są dostępne w formularzu.
@pytest.mark.django_db
def test_all_categories_in_form(client, users, create_categories):
    client.force_login(users[0])
    categories = create_categories
    response = client.get(reverse('add_offer'))

    for category in categories:
        assert category.name.encode() in response.content


"""testy do widoku EditOfferView"""


# jak jest z zalogowanym uzytkownukiem i włascicle ofrty
@pytest.mark.django_db
def test_edit_offer_view_logged(client, users):
    client.force_login(users[0])
    offer = Offer.objects.create(
        name='Test Offer',
        country='Test Country',
        city='Test City',
        description='Test Description',
        offer_type='job offer',
        since_when=timezone.now().date() + timedelta(days=1),
        until_when=timezone.now().date() + timedelta(days=2),
        only_for_women=True,
        owner=users[0],
        is_active=True
    )
    response = client.get(reverse('edit_offer', kwargs={'offer_id': offer.id}))
    assert 'Edit offer' in response.content.decode()

    assert response.context['offer'].name == offer.name


# nie zalogowany uzytkownik
@pytest.mark.django_db
def test_edit_offer_view_stranger(client):
    response = client.get(reverse('edit_offer', kwargs={'offer_id': 1}))
    assert '/login/' in response.url


# test edycji
@pytest.mark.django_db
def test_edit_offer_view(client, users, create_categories):
    client.force_login(users[0])
    offer = Offer.objects.create(
        name='Test Offer',
        country='Test Country',
        city='Test City',
        description='Test Description',
        offer_type='job offer',
        category=create_categories[0],
        since_when=timezone.now().date() + timedelta(days=1),
        until_when=timezone.now().date() + timedelta(days=2),
        only_for_women=True,
        owner=users[0],
        is_active=True
    )
    offer.category.add(create_categories[0])
    response = client.post(reverse('edit_offer', kwargs={'offer_id': offer.id}), {
        'name': 'Updated Test Offer',
        'country': 'Updated Test Country',
        'city': 'Updated Test City',
        'description': 'Updated Test Description',
        'offer_type': 'job seekers',
        'since_when': timezone.now().date() + timedelta(days=3),
        'until_when': timezone.now().date() + timedelta(days=4),
        'only_for_women': False,
        'owner': users[0].id,
        'is_active': False
    })
    updated_offer = Offer.objects.get(id=offer.id)
    assert updated_offer.name == 'Updated Test Offer'  # Sprawdź, czy nazwa oferty została zaktualizowana
    assert updated_offer.offer_type == 'job seekers'  # Sprawdź, czy typ oferty został zaktualizowany


# nieprawidłowe dane
@pytest.mark.django_db
def test_edit_offer_view_post(client, users):
    client.force_login(users[0])
    offer = Offer.objects.create(
        name='Test Offer',
        country='Test Country',
        city='Test City',
        description='Test Description',
        offer_type='job offer',
        since_when=timezone.now().date() + timedelta(days=1),
        until_when=timezone.now().date() + timedelta(days=2),
        only_for_women=True,
        owner=users[0],
        is_active=True
    )
    response = client.post(reverse('edit_offer', kwargs={'offer_id': offer.id}), {
        'name': '',
        'country': 'Updated Test Country',
        'city': 'Updated Test City',
        'description': 'Updated Test Description',
        'offer_type': 'job seekers',
        'since_when': timezone.now().date() + timedelta(days=3),
        'until_when': timezone.now().date() + timedelta(days=2),
        'only_for_women': False,
        'owner': users[0].id,
        'is_active': False
    })
    assert 'This field is required' in response.content.decode()
    assert Offer.objects.get(id=offer.id).name == 'Test Offer'


"""testy do widoku DeleteOfferView"""


# dostepnośc strony zalogowany

@pytest.mark.django_db
def test_delete_offer_page_logged_user(client, users, create_offers):
    client.force_login(users[0])
    offer = create_offers[0]
    response = client.get(reverse('delete_offer_ays', kwargs={'offer_id': offer.id}))
    assert 'Are you sure you want to delete the offer?' in response.content.decode()  # sprawdzanie czy ten napis konkretnie pojawi sie na stronie


# czy naprawde usuwa i czy przekierownie działa
@pytest.mark.django_db
def test_offer_deletion(client, users, create_offers):
    client.force_login(users[0])
    offer = create_offers[0]
    response = client.post(reverse('delete_offer', kwargs={'offer_id': offer.id}), follow=True)
    assert Offer.objects.filter(id=offer.id).count() == 0
    assert response.redirect_chain[-1][0] == reverse('offers_list')


# czy działa przekierowanie
@pytest.mark.django_db
def test_delete_offer_by_non_owner(client, users, create_offers):
    client.force_login(users[1])
    offer = create_offers[0]
    response = client.post(reverse('delete_offer_ays', kwargs={'offer_id': offer.id}))
    assert Offer.objects.filter(id=offer.id).exists()


# rezygnacje czyi klik w back to offers
@pytest.mark.django_db
def test_cancel_offer_deletion_redirect(client, users, create_offers):
    client.force_login(users[0])
    offer = create_offers[0]
    response = client.get(reverse('offers_list'), follow=True)  # udajemy że klik link
    assert response.status_code == 200  # czy przekierowanie działa
    assert Offer.objects.filter(id=offer.id).exists()  # spr czy oferta nadal jest
    assert 'Back to offers list' in response.content.decode() or 'offers_list.html' in [t.name for t in
                                                                                        response.templates]  # sprawdzanie obecnego szablonu


"""""testy do widoku  OfferListView"""


# zalogowany
@pytest.mark.django_db
def test_offers_list_logged(client, users, create_offers):
    client.force_login(users[0])
    response = client.get(reverse('offers_list'))
    assert 'Edit offer' in response.content.decode()
    assert 'Delete offer' in response.content.decode()


# nie zalogowany
@pytest.mark.django_db
def test_offers_list_stranger(client, create_offers):
    response = client.get(reverse('offers_list'))
    assert 'Edit offer' not in response.content.decode()
    assert 'Delete offer' not in response.content.decode()


# paginacja
@pytest.mark.django_db
def test_offers_list_pagination(client, create_offers):
    response = client.get(reverse('offers_list'))
    assert 'offers_list' in response.context
    offers_list = response.context['offers_list']
    assert offers_list.paginator.num_pages >= 1
    assert len(offers_list.object_list) <= 2


# różne wielkosci liter
@pytest.mark.django_db
@pytest.mark.parametrize("search_query,expected_count,expected_countries", [
    ('Poland', 1, ['Poland']),
    ('poland', 1, ['Poland']),
    ('', 2, ['Poland', 'Canada']),
    ('Germany', 0, []),
])
def test_offers_list_view_search(client, create_offers, search_query, expected_count, expected_countries):
    response = client.get(reverse('offers_list'), {'search': search_query})
    offers = response.context['offers_list'].object_list
    assert len(offers) == expected_count
    for offer, expected_country in zip(offers,
                                       expected_countries):  # dzieki zip interujemy po dwuch zmiennch jednoczenie twozy pary oferta i oczkiwany kraj
        assert offer.country == expected_country


"""testy do widoku YourOffersView"""


# nie zalogowany
def test_your_offers_starnger(client):
    response = client.get(reverse('your_offers'))
    assert '/login/' in response.url


# oferty dla zalogowanago i czy jest włascicielem
@pytest.mark.django_db
def test_your_offers_view_logged(client, users, create_offers):
    client.force_login(users[0])
    response = client.get(reverse('your_offers'))
    assert response.status_code == 200
    assert 'offers' in response.context
    user_offers = response.context['offers']
    assert all(offer.owner == users[0] for offer in user_offers)
    assert not any(offer.owner != users[0] for offer in user_offers)


# czy jest odpowiedznia kolejnosci
@pytest.mark.django_db
def test_your_offers_order(client, users, create_offers):
    client.force_login(users[0])
    response = client.get(reverse('your_offers'))
    user_offers = response.context['offers']
    assert list(user_offers) == sorted(user_offers, key=lambda
        x: x.until_when)  # dzieki anonimowej funcjki lambd sprawdzamy czy sortuje sie według `until_when`


"""testy do widoku OfferDetailsView"""


# dostepność
@pytest.mark.django_db
def test_offer_details_logged(client, create_offers):
    offer = create_offers[0]
    response = client.get(reverse('offer_details', kwargs={'offer_id': offer.id}))
    assert response.status_code == 200


# czy szczrgóły widac
@pytest.mark.django_db
def test_offer_details_view_content(client, create_offers):
    offer = create_offers[0]
    response = client.get(reverse('offer_details', kwargs={'offer_id': offer.id}))
    content = response.content.decode()
    assert offer.name in content
    assert offer.description in content
    assert offer.country in content
    for category in offer.category.all():
        assert category.name in content


# czy dziala jak zalogowny jest wlasciciel
def test_offer_details_owner(client, users, create_offers):
    client.force_login(users[0])
    offer = create_offers[0]
    response = client.get(reverse('offer_details', kwargs={'offer_id': offer.id}))
    assert 'Edit offer' in response.content.decode()
    assert 'Apply and send message' not in response.content.decode()


# czy dziala jak zalogowny nie jest wlasciciel

def test_offer_details_view_apply_option_for_non_owner(client, users, create_offers):
    client.force_login(users[1])
    offer = create_offers[0]
    response = client.get(reverse('offer_details', kwargs={'offer_id': offer.id}))
    assert 'Apply and send message' in response.content.decode()
    assert 'Edit offer' not in response.content.decode()


# nie zalogowany
@pytest.mark.django_db
def test_offer_details_view_for_anonymous_user(client, create_offers):
    offer = create_offers[0]
    response = client.get(reverse('offer_details', kwargs={'offer_id': offer.id}))
    content = response.content.decode()
    assert 'Apply and send message' not in content
    assert 'Edit offer' not in content
    assert offer.name in content
    assert offer.description in content


"""Testy do widoku MessageBoxView"""


# dostepnosc zalogowany
def test_message_box_logged(client):
    response = client.get(reverse('message_box'))
    assert response.status_code == 302


# zalogowany widok konwersacji
@pytest.mark.django_db
def test_message_box_view_logged(client, users, create_offers, messages):
    client.force_login(users[0])
    response = client.get(reverse('message_box'))
    assert response.status_code == 200
    assert 'conversations' in response.context
    conversations = response.context['conversations']
    for offer, msgs in conversations.items():
        assert any(message.sender == users[0] or message.receiver == users[0] for message in msgs)


# kolejnosc wiadomosci
@pytest.mark.django_db
def test_message_box_order(client, users, create_offers, messages):
    client.force_login(users[0])
    response = client.get(reverse('message_box'))
    conversations = response.context['conversations']
    for offer, msgs in conversations.items():
        sorted_messages = sorted(msgs, key=lambda message: message.time)
        assert list(msgs) == sorted_messages


# poprawnosc nadawcy i odbiorcy
@pytest.mark.django_db
def test_message_box_view_sender_receiver(client, users, create_offers, messages):
    client.force_login(users[0])

    response = client.get(reverse('message_box'))  # pobieram konwersacje
    conversations = response.context['conversations']

    for offer, conversation_messages in conversations.items():
        for message in conversation_messages:  # ide przez konwersaje
            assert message.sender == users[0] or message.receiver == users[0]


# nie zalogowany
def test_message_box_view_stranger(client):
    response = client.get(reverse('message_box'))
    assert '/login/' in response.url


"""testy do widoku MessagesViews"""


# nie zalogowany

def test_messages_view_stranger(client, create_offers):
    offer = create_offers[0]
    response = client.get(reverse('messages_view', kwargs={'offer_id': offer.id}))
    assert '/login/' in response.url


# zalogowany widok wiadomosci
@pytest.mark.django_db
def test_messages_view_for_logged_user(client, users, create_offers, messages):
    client.force_login(users[0])
    offer = create_offers[0]
    response = client.get(reverse('messages_view', kwargs={'offer_id': offer.id}))
    assert 'conversations' in response.context
    conversations = response.context['conversations']
    for conversation in conversations:
        assert any(message.sender == users[0] or message.receiver == users[0] for message in conversation['messages'])


# kolejnosc wiadomosci
@pytest.mark.django_db
def test_messages_order_in_conversation(client, users, create_offers, messages):
    client.force_login(users[0])
    offer = create_offers[0]
    response = client.get(reverse('messages_view', kwargs={'offer_id': offer.id}))
    conversations = response.context['conversations']
    for conversation in conversations:
        sorted_messages = sorted(conversation['messages'], key=lambda x: x.time, reverse=True)
        assert conversation['messages'] == sorted_messages


# sprawdzanie czy pary uzytkowników do wiadomosci działają
@pytest.mark.django_db
def test_messages_grouping_by_partner(client, users, create_offers, messages):
    client.force_login(users[0])
    offer = create_offers[0]
    response = client.get(reverse('messages_view', kwargs={'offer_id': offer.id}))
    conversations = response.context['conversations']
    for conversation in conversations:
        partner_ids = {messages.sender.id for messages in conversation['messages']}
        partner_ids.update(msg.receiver.id for msg in conversation['messages'])
        partner_ids.discard(users[0].id)  # Usuwam zalogowanego użytkownika zeby spr czy została tylko jedna para
        assert len(partner_ids) == 1  # czy jest 1 unikalny partner


"""testowanie widoku TopicView"""


# Widadomosci dla zaogowanego i czy dane sa poprawne
@pytest.mark.django_db
def test_topic_view_msg_logged(client, users, create_offers, messages):
    client.force_login(users[0])

    response = client.get(reverse('topic_view', kwargs={'offer_id': 1, 'sender_id': 2}))
    assert 'topic_view.html' in [t.name for t in response.templates]
    assert 'messages' in response.context
    assert 'message_form' in response.context
    assert 'offer' in response.context
    assert 'sender_id' in response.context


# nie zalogowany
@pytest.mark.django_db
def test_topic_view_stranger(client, users, create_offers):
    response = client.get(reverse('topic_view', kwargs={'offer_id': 1, 'sender_id': 2}))
    assert '/login/' in response.url


# czy formularz działa
@pytest.mark.django_db
def test_topic_view_message_form(client, users, create_offers):
    client.force_login(users[0])
    response = client.post(reverse('topic_view', kwargs={'offer_id': 1, 'sender_id': 2}),
                           data={'message': 'Test message'})
    assert response.url == reverse('topic_view', kwargs={'offer_id': 1, 'sender_id': 2})
    assert Message.objects.filter(message='Test message').exists()


# walidacj czy działa
@pytest.mark.django_db
def test_topic_view_form_validation(client, users, create_offers):
    client.force_login(users[0])
    response = client.post(reverse('topic_view', kwargs={'offer_id': 1, 'sender_id': 2}), data={'message': ''})
    assert 'This field is required.' in response.content.decode()


# Link do dawania oceny
@pytest.mark.django_db
def test_topic_view_rating_link(client, users, create_offers):
    client.force_login(users[0])
    response = client.get(reverse('topic_view', kwargs={'offer_id': 1, 'sender_id': 2}))
    assert 'Give a rating' in response.content.decode()


# brak linku dla nie własciciela
@pytest.mark.django_db
def test_topic_view_not_see_rating_link(client, users, create_offers):
    client.force_login(users[1])
    response = client.get(reverse('topic_view', kwargs={'offer_id': 1, 'sender_id': 2}))

    assert 'Give a rating' not in response.content.decode()


"""testy do GradeViews"""


# zalogowany własciciel
@pytest.mark.django_db
def test_grade_view_logged_owner(client, users, create_offers, messages):
    client.force_login(users[0])
    response = client.get(reverse('grade_view', kwargs={'offer_id': 1, 'sender_id': 2}))
    assert 'grade.html' in [t.name for t in response.templates]

    # Spr dane w szablonie czy dobrze widac
    assert 'form' in response.context
    assert 'message' in response.context
    assert 'offer' in response.context
    assert 'first_message_sender' in response.context
    assert 'answer' in response.context
    assert 'Give a rating' not in response.content.decode()


# zalogowany sender
@pytest.mark.django_db
def test_grade_view_logged_sender(client, users, create_offers, messages):
    client.force_login(users[1])
    response = client.get(reverse('grade_view', kwargs={'offer_id': 1, 'sender_id': 2}))
    assert '/login/' in response.url


# nie zalogowany
@pytest.mark.django_db
def test_grade_view_stranger(client, users, create_offers, messages):
    response = client.get(reverse('grade_view', kwargs={'offer_id': 1, 'sender_id': 2}))
    assert '/login/' in response.url


"""testy do widoku YourGrade"""


# zalogowany
@pytest.mark.django_db
def test_your_grades_view_logged(client, users, create_offers, messages, grade):
    client.force_login(users[0])
    response = client.get(reverse('your_grades'))
    assert 'your_grades.html' in [t.name for t in response.templates]
    assert 'grades_list' in response.context


# nie zalogowany
@pytest.mark.django_db
def test_your_grades_view_stranger(client):
    response = client.get(reverse('your_grades'))
    assert '/login/' in response.url


@pytest.mark.django_db
def test_your_grades_view_grades(client, users, create_offers, messages, grade):
    client.force_login(users[0])
    response = client.get(reverse('your_grades'))
    assert 'grades_list' in response.context
    grades_list = response.context['grades_list']
    assert len(grades_list) == 1  # czy lista ma odpowiednia długość
    grade_info = grades_list[0]
    assert grade_info['offer_names'] == 'Graphic Designer'  # czy nazwa oferty jest ok
    assert grade_info['owner_names'] == 'user3'
    assert grade_info['grade_value'] == 5


"""testy do widoku AnswerGradeView"""


# czy widok dział
@pytest.mark.django_db
def test_get_answer_view_logged(client, users, create_offers, messages, grade):
    client.force_login(users[0])
    response = client.get(reverse('answer_view', kwargs={'grade_id': grade.id}))
    assert 'answer.html' in [t.name for t in response.templates]


# nie zalogowany
@pytest.mark.django_db
def test_get_answer_view_stranger(client, grade):
    response = client.get(reverse('answer_view', kwargs={'grade_id': grade.id}))
    assert '/login/' in response.url


# czy wysyłanie odp działa
@pytest.mark.django_db
def test_post_answer_view_logged(client, users, create_offers, messages, grade):
    client.force_login(users[0])
    response = client.post(reverse('answer_view', kwargs={'grade_id': grade.id}),
                           {'text': 'Thank you!', 'grade_answer': 5})
    assert response.status_code == 302


# walidacja
@pytest.mark.django_db
def test_post_answer_view_form(client, users, create_offers, messages, grade):
    client.force_login(users[0])
    response = client.post(reverse('answer_view', kwargs={'grade_id': grade.id}), {})
    assert 'answer.html' in [t.name for t in response.templates]

#czy dziala zabespieczenie przed niechciacynmi
@pytest.mark.django_db
def test_get_answer_view_wrong_user(client, users, create_offers, messages, grade):
    client.force_login(users[1])
    response = client.get(reverse('answer_view', kwargs={'grade_id': grade.id}))
    assert response.url == reverse('your_grades')

