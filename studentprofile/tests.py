from django.test import TestCase
from django.contrib.auth.models import User

from .models import Student

# Create your tests here.
class StudentModelCreationTests(TestCase):
    def test_profile_is_created_with_default_year(self):
        s1 = Student(name="s1")
        self.assertEqual(s1.year,1)
       
    def test_profile_is_created_with_default_major(self):
        s2 = Student(name="s1")
        self.assertEqual(s2.major,"None")
    
    def test_profile_is_created_with_name(self):
        s3 = Student(name="s1")
        self.assertEqual(s3.name,"s1")

    def test_profile_saved_with_year(self):
        s4 = Student(name="s2Name",year=2,major="Math")
        self.assertEqual(s4.year,2)

    def test_profile_saved_with_major(self):
        s5 = Student(name="s2Name",year=2,major="Math")
        self.assertEqual(s5.major,"Math")

    def test_profile_saved_with_name(self):
        s6 = Student(name="s2Name",year=2,major ="Math")
        self.assertEqual(s6.name,"s2Name")




