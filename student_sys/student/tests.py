from django.test import TestCase
from .models import Student

class StudentTestCase(TestCase):
    def setUp(self):
        Student.objects.create(
            name="zhouxr",
            sex = 1,
            email = "1343932126@qq.com",
            profession="程序员",
            qq='111',
            phone='1111',
        )

    def test_create_and_sex_show(self):
        student=Student.objects.create(
            name="zhouxr",
            sex=1,
            email="1343932126@qq.com",
            profession="程序员",
            qq='111',
            phone='1111',
        )
        self.assertEqual(Student.sex_show,'男','性别字段内容展示不一致')
