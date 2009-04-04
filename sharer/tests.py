from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client


class SharerTestCase(TestCase):
    def setUp(self):
        pass

    def testShareFormPageLoads(self):
        response = self.client.get(reverse("sharer_share"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "sharer/form.html")

    def testShareDonePageLoads(self):
        response = self.client.get(reverse("sharer_done"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "sharer/done.html")

    def testShareFormFails(self):
        response = self.client.post(reverse("sharer_share"), {
            "recipient": "",
            "sender": "",
            "message": "",
            "url": "",
            "title": "",
        })

        self.assertFormError(response, 'form', 'recipient', 'This field is required.')
        self.assertFormError(response, 'form', 'sender', 'This field is required.')

    def testShareFormSendsEmail(self):
        response = self.client.post(reverse("sharer_share"), {
            "recipient": "taylanpince@gmail.com",
            "sender": "taylan@orangeslices.net",
            "message": "This is a test!",
            "url": "http://www.dummy.com",
            "title": "Dummy Title",
        })

        self.assertRedirects(response, reverse("sharer_done"))
        self.assertEquals(len(mail.outbox), 1)
