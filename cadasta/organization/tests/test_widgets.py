from django.test import TestCase
from django.http.request import QueryDict
from django.forms import formset_factory

from ..forms import FORM_CHOICES, ContactsForm
from ..widgets import ProjectRoleWidget, PublicPrivateToggle, ContactsWidget

from accounts.tests.factories import UserFactory


class ProjectRoleWidgetTest(TestCase):
    def setUp(self):
        self.user = UserFactory.build(
            username='bob',
            email='me@example.com',
            full_name='Bob Smith'
        )
        self.widget = ProjectRoleWidget(user=self.user, choices=FORM_CHOICES)

    def test_render_with_admin(self):
        html = self.widget.render(self.user.username, 'A')

        expected = (
            '<tr>'
            '  <td>'
            '    <p>Bob Smith</p>'
            '    <p>bob</p>'
            '  </td>'
            '  <td class="hidden-xs hidden-sm">me@example.com</td>'
            '  <td>'
            '    Administrator'
            '  </td>'
            '</tr>'
        )
        assert expected == html

    def test_render_with_manager(self):
        html = self.widget.render(self.user.username, 'PM')

        expected = (
            '<tr>'
            '  <td>'
            '    <p>Bob Smith</p>'
            '    <p>bob</p>'
            '  </td>'
            '  <td class="hidden-xs hidden-sm">me@example.com</td>'
            '  <td>'
            '    <select name="bob">\n'
            '<option value="PU">Project User</option>\n'
            '<option value="DC">Data Collector</option>\n'
            '<option value="PM" selected="selected">Project Manager</option>\n'
            '<option value="Pb">Public User</option>\n'
            '</select>'
            '  </td>'
            '</tr>'
        )
        assert expected == html


class PublicPrivateToggleTest(TestCase):
    def test_render_none(self):
        widget = PublicPrivateToggle()
        html = widget.render('field-name', None)

        expected = (
            '<div class="public-private-widget">'
            '  <label for"field-name">Project visibility</label>'
            '  <div>'
            '    Public<br>'
            '    <span class="glyphicon glyphicon-eye-open"></span>'
            '  </div>'
            '  <div>'
            '    <input name="field-name"  type="checkbox"'
            '           data-toggle="toggle" data-onstyle="danger"'
            '           data-offstyle="success" data-on=" " data-off=" ">'
            '  </div>'
            '  <div>'
            '    Private<br>'
            '    <span class="glyphicon glyphicon-eye-close"></span>'
            '  </div>'
            '</div>'
        )

        assert expected == html

    def test_render_public(self):
        widget = PublicPrivateToggle()
        html = widget.render('field-name', 'public')

        expected = (
            '<div class="public-private-widget">'
            '  <label for"field-name">Project visibility</label>'
            '  <div>'
            '    Public<br>'
            '    <span class="glyphicon glyphicon-eye-open"></span>'
            '  </div>'
            '  <div>'
            '    <input name="field-name"  type="checkbox"'
            '           data-toggle="toggle" data-onstyle="danger"'
            '           data-offstyle="success" data-on=" " data-off=" ">'
            '  </div>'
            '  <div>'
            '    Private<br>'
            '    <span class="glyphicon glyphicon-eye-close"></span>'
            '  </div>'
            '</div>'
        )

        assert expected == html

    def test_render_private(self):
        widget = PublicPrivateToggle()
        html = widget.render('field-name', 'private')

        expected = (
            '<div class="public-private-widget">'
            '  <label for"field-name">Project visibility</label>'
            '  <div>'
            '    Public<br>'
            '    <span class="glyphicon glyphicon-eye-open"></span>'
            '  </div>'
            '  <div>'
            '    <input name="field-name" checked type="checkbox"'
            '           data-toggle="toggle" data-onstyle="danger"'
            '           data-offstyle="success" data-on=" " data-off=" ">'
            '  </div>'
            '  <div>'
            '    Private<br>'
            '    <span class="glyphicon glyphicon-eye-close"></span>'
            '  </div>'
            '</div>'
        )

        assert expected == html

    def test_render_on(self):
        widget = PublicPrivateToggle()
        html = widget.render('field-name', 'on')

        expected = (
            '<div class="public-private-widget">'
            '  <label for"field-name">Project visibility</label>'
            '  <div>'
            '    Public<br>'
            '    <span class="glyphicon glyphicon-eye-open"></span>'
            '  </div>'
            '  <div>'
            '    <input name="field-name" checked type="checkbox"'
            '           data-toggle="toggle" data-onstyle="danger"'
            '           data-offstyle="success" data-on=" " data-off=" ">'
            '  </div>'
            '  <div>'
            '    Private<br>'
            '    <span class="glyphicon glyphicon-eye-close"></span>'
            '  </div>'
            '</div>'
        )

        assert expected == html


class ContactsWidgetTest(TestCase):
    def test_value_from_datadict(self):
        formset = formset_factory(ContactsForm)
        widget = ContactsWidget(attrs={'formset': formset})
        data = {
            'contacts-TOTAL_FORMS': '2',
            'contacts-INITIAL_FORMS': '1',
            'contacts-MAX_NUM_FORMS': '0',
            'contacts-MAX_NUM_FORMS': '1000',
            'contacts-0-name': 'Ringo',
            'contacts-0-email': 'ringo@beatles.uk',
            'contacts-0-tel': '555-555',
            'contacts-1-name': '',
            'contacts-1-email': '',
            'contacts-1-tel': ''
        }
        q_dict = QueryDict('', mutable=True)
        q_dict.update(data)
        value = widget.value_from_datadict(q_dict, {}, 'contacts')
        assert isinstance(value, formset)

    def test_render_with_formset(self):
        value = [{
                    'name': 'Ringo',
                    'email': 'ringo@beatles.uk',
                    'tel': '555-555',
                }]
        formset = formset_factory(ContactsForm)
        value = formset(initial=value, prefix='contacts')

        for form in value.forms:
            for field in form:
                field.field.widget.attrs = {'some': 'attr'}

        widget = ContactsWidget(attrs={'formset': formset})
        html = widget.render('contacts', value, attrs={'class': 'some'})
        assert ('<table class="table contacts-form">'
                '  <thead>'
                '    <tr>'
                '      <th>Name</th>'
                '      <th>Email</th>'
                '      <th>Phone</th>'
                '      <th></th>'
                '    </tr>'
                '  </thead>' in html)
        assert ('  <tfoot>'
                '    <tr>'
                '      <td colspan="4">'
                '        <button data-prefix="contacts" type="button" '
                '                class="btn btn-default btn-sm" '
                '                id="add-contact"><span class="glyphicon '
                '                glyphicon-plus" aria-hidden="true"></span> '
                '                Add contact</button>'
                '      </td>'
                '    </tr>'
                '  </tfoot>'
                '</table>' in html)

        assert 'contacts-0-name' in html
        assert 'contacts-1-name' in html
